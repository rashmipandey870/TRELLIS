"""Automated Query Budget Verification Test.

Enforces SQL statement limits per endpoint under realistic learner caseload:
- Dashboards <= 8 queries
- List endpoints <= 10 queries
- Detail/analysis endpoints <= 15 queries
"""

from __future__ import annotations

from typing import Any
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.v1.admin import get_department_dashboard, get_learner_detail, list_learners
from app.api.v1.learner import get_learner_dashboard, list_learner_results
from app.api.v1.mentor import (
    get_assessment_analysis,
    get_assigned_learners,
    get_mentor_dashboard,
    list_mentor_assessments,
)
from app.core.security import hash_password
from app.models import (
    Assessment,
    AssessmentAttempt,
    AssessmentQuestion,
    Base,
    Batch,
    Meeting,
    MeetingAudience,
    MentorLearnerAssignment,
    MentorRemark,
    Organisation,
    QuestionBank,
    Submission,
    TalentAlert,
    User,
)


@pytest.fixture(scope="module")
def query_budget_env():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    org = Organisation(name="CSM Technologies", code="CSM-BUDGET")
    db.add(org)
    db.flush()

    pwd_hash = hash_password("budgetpass123")
    admin = User(
        org_id=org.id,
        email="budget_admin@csmtech.internal",
        password_hash=pwd_hash,
        full_name="Budget Admin",
        role="ADMIN",
        is_active=True,
    )
    mentor = User(
        org_id=org.id,
        email="budget_mentor@csmtech.internal",
        password_hash=pwd_hash,
        full_name="Budget Mentor",
        role="MENTOR",
        is_active=True,
    )
    db.add_all([admin, mentor])
    db.flush()

    batch = Batch(name="Budget Batch 1", code="BB1", max_learners=250)
    db.add(batch)
    db.flush()

    learners = []
    for i in range(50):
        u = User(
            org_id=org.id,
            email=f"budget_learner_{i}@csmtech.internal",
            password_hash=pwd_hash,
            full_name=f"Budget Learner {i}",
            role="LEARNER",
            is_active=True,
            streak_days=5 + (i % 10),
        )
        learners.append(u)
    db.add_all(learners)
    db.flush()

    for l in learners:
        assign = MentorLearnerAssignment(
            mentor_id=mentor.id,
            learner_id=l.id,
            batch_id=batch.id,
        )
        db.add(assign)

    qb = QuestionBank(
        author_id=mentor.id,
        title="Query Budget MCQ",
        question_text="What is 2+2?",
        question_type="MCQ",
        field="Python",
        topic="Math",
        category="TECHNICAL",
        difficulty="EASY",
    )
    db.add(qb)
    db.flush()

    assessment = Assessment(
        mentor_id=mentor.id,
        batch_id=batch.id,
        title="Budget Assessment 1",
        field="FullStack",
        duration_minutes=30,
        passing_score=60,
        status="PUBLISHED",
    )
    db.add(assessment)
    db.flush()

    aq = AssessmentQuestion(
        assessment_id=assessment.id,
        bank_question_id=qb.id,
        marks=10,
        sequence_order=1,
    )
    db.add(aq)

    for l in learners[:25]:
        att = AssessmentAttempt(
            assessment_id=assessment.id,
            learner_id=l.id,
            score=75.0,
            total_marks=100.0,
            passed=True,
            status="SUBMITTED",
        )
        db.add(att)

    remark = MentorRemark(
        mentor_id=mentor.id,
        learner_id=learners[0].id,
        remark_text="Great performance",
        visibility="LEARNER_AND_ADMIN",
    )
    db.add(remark)

    alert = TalentAlert(
        mentor_id=mentor.id,
        learner_id=learners[0].id,
        field="FullStack",
        status="PENDING",
        evidence_json={"note": "Consistently high scores"},
    )
    db.add(alert)
    db.commit()

    class QueryCounter:
        def __init__(self):
            self.count = 0
            self.statements = []

        def __enter__(self):
            self.count = 0
            self.statements = []
            event.listen(engine, "before_cursor_execute", self._callback)
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            event.remove(engine, "before_cursor_execute", self._callback)

        def _callback(self, conn, cursor, statement, parameters, context, executemany):
            self.count += 1
            self.statements.append(statement)

    yield {
        "db": db,
        "counter_factory": QueryCounter,
        "admin": admin,
        "mentor": mentor,
        "learner": learners[0],
        "assessment": assessment,
    }

    db.close()


def test_dashboard_query_budgets(query_budget_env):
    """Dashboards query budget <= 8 queries."""
    db = query_budget_env["db"]
    counter_factory = query_budget_env["counter_factory"]
    admin = query_budget_env["admin"]
    mentor = query_budget_env["mentor"]
    learner = query_budget_env["learner"]

    # 1. Admin Dashboard
    _ = admin.id
    with counter_factory() as c:
        res = get_department_dashboard(db=db, _admin=admin)
    assert res is not None
    assert c.count <= 8, f"Admin dashboard exceeded query budget (8): used {c.count}"

    # 2. Mentor Dashboard
    _ = mentor.id
    with counter_factory() as c:
        res = get_mentor_dashboard(db=db, mentor=mentor)
    assert res is not None
    assert c.count <= 8, f"Mentor dashboard exceeded query budget (8): used {c.count}\nStatements:\n" + "\n".join(c.statements)

    # 3. Learner Dashboard
    _ = learner.id
    with counter_factory() as c:
        res = get_learner_dashboard(db=db, learner=learner)
    assert res is not None
    assert c.count <= 8, f"Learner dashboard exceeded query budget (8): used {c.count}"


def test_list_endpoints_query_budgets(query_budget_env):
    """List endpoints query budget <= 10 queries."""
    db = query_budget_env["db"]
    counter_factory = query_budget_env["counter_factory"]
    admin = query_budget_env["admin"]
    mentor = query_budget_env["mentor"]
    learner = query_budget_env["learner"]

    # 1. Admin Learners List
    with counter_factory() as c:
        res = list_learners(db=db, _admin=admin)
    assert len(res) > 0
    assert c.count <= 10, f"Admin learners list exceeded query budget (10): used {c.count}"

    # 2. Mentor Learners List
    with counter_factory() as c:
        res = get_assigned_learners(db=db, mentor=mentor)
    assert len(res) > 0
    assert c.count <= 10, f"Mentor learners list exceeded query budget (10): used {c.count}"

    # 3. Mentor Assessments List
    with counter_factory() as c:
        res = list_mentor_assessments(db=db, mentor=mentor)
    assert len(res) > 0
    assert c.count <= 10, f"Mentor assessments list exceeded query budget (10): used {c.count}"

    # 4. Learner Results List
    with counter_factory() as c:
        res = list_learner_results(db=db, learner=learner)
    assert isinstance(res, list)
    assert c.count <= 10, f"Learner results list exceeded query budget (10): used {c.count}"


def test_detail_analysis_query_budgets(query_budget_env):
    """Detail / analysis endpoints query budget <= 15 queries."""
    db = query_budget_env["db"]
    counter_factory = query_budget_env["counter_factory"]
    admin = query_budget_env["admin"]
    mentor = query_budget_env["mentor"]
    learner = query_budget_env["learner"]
    assessment = query_budget_env["assessment"]

    # 1. Admin Learner Detail
    with counter_factory() as c:
        res = get_learner_detail(learner_id=learner.id, db=db, _admin=admin)
    assert res is not None
    assert c.count <= 15, f"Admin learner detail exceeded query budget (15): used {c.count}"

    # 2. Mentor Assessment Analysis
    with counter_factory() as c:
        res = get_assessment_analysis(assessment_id=assessment.id, export=False, db=db, mentor=mentor)
    assert res is not None
    assert c.count <= 15, f"Mentor assessment analysis exceeded query budget (15): used {c.count}"
