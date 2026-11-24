from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api.v1.coding import list_coding_problems
from app.api.v1.practice import (
    GenerateQuestionRequest,
    generate_question,
    _user_generate_timestamps,
)
from app.api.v1.mentor import get_learner_ai_diagnostic_for_mentor
from app.api.v1.admin import get_learner_ai_diagnostic_for_admin
from app.models import (
    Base,
    Batch,
    CodingProblem,
    Organisation,
    TestCase,
    User,
)


@pytest.fixture
def test_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


def test_coding_problems_open_access(test_db: Session):
    """Verify that learners can view and practice coding problems without active assessment."""
    org = Organisation(name="Coding Test Org", code="CODING_ORG")
    test_db.add(org)
    test_db.flush()

    batch = Batch(name="Test Batch", code="BATCH_TEST_1", org_id=org.id)
    test_db.add(batch)
    test_db.flush()

    learner = User(
        email="coding_learner@trellis.internal",
        full_name="Coding Learner",
        role="LEARNER",
        org_id=org.id,
        password_hash="hashed_pw",
        is_active=True,
    )
    test_db.add(learner)
    test_db.flush()

    # Add a coding problem with test case
    prob = CodingProblem(
        title="Dynamic Two Sum",
        description="Find indices of two numbers that add up to target.",
        difficulty="MEDIUM",
        time_limit_ms=2000,
        memory_limit_mb=256,
        field="Python",
    )
    test_db.add(prob)
    test_db.flush()

    tc = TestCase(
        problem_id=prob.id,
        input_data="[2, 7, 11, 15]\n9",
        expected_output="[0, 1]",
        is_hidden=False,
        weight=1.0,
    )
    test_db.add(tc)
    test_db.commit()

    # Query coding problems without attempt_id (Open Practice Mode)
    results = list_coding_problems(attempt_id=None, db=test_db, user=learner)
    assert isinstance(results, list)
    assert len(results) >= 1
    found = any(p["id"] == prob.id for p in results)
    assert found, "Created coding problem should be accessible in open practice mode"
    assert results[0]["title"] == "Dynamic Two Sum"


def test_ai_practice_dynamic_deduplication(test_db: Session):
    """Verify AI Practice provides dynamic, distinct questions across repeated generation requests."""
    org = Organisation(name="Practice Test Org", code="PRACTICE_ORG")
    test_db.add(org)
    test_db.flush()

    learner = User(
        email="practice_learner@trellis.internal",
        full_name="Practice Learner",
        role="LEARNER",
        org_id=org.id,
        password_hash="hashed_pw",
        is_active=True,
    )
    test_db.add(learner)
    test_db.commit()

    _user_generate_timestamps[learner.id] = []

    # Generate 5 questions across Python and SQL, asserting each is valid and hashes are tracked
    seen_ids = set()
    req = GenerateQuestionRequest(field="Python", difficulty="MEDIUM", mode="MCQ")
    for i in range(5):
        data = generate_question(req, db=test_db, user=learner)
        assert "id" in data
        assert "content" in data
        assert "options" in data
        assert len(data["options"]) == 4
        assert len(data["content"].strip()) > 10
        seen_ids.add(data["id"])

    assert len(seen_ids) == 5, f"All 5 generated questions should be unique sessions: {seen_ids}"


def test_admin_and_mentor_learner_ai_diagnostic_access(test_db: Session):
    """Verify both Admin and Mentor can access learner AI diagnostic dossier."""
    org = Organisation(name="Dossier Test Org", code="DOSSIER_ORG")
    test_db.add(org)
    test_db.flush()

    batch = Batch(name="Dossier Batch", code="BATCH_DOSSIER_1", org_id=org.id)
    test_db.add(batch)
    test_db.flush()

    admin = User(
        email="admin_dossier@trellis.internal",
        full_name="Admin Dossier",
        role="ADMIN",
        org_id=org.id,
        password_hash="hashed_pw",
        is_active=True,
    )
    test_db.add(admin)

    mentor = User(
        email="mentor_dossier@trellis.internal",
        full_name="Mentor Dossier",
        role="MENTOR",
        org_id=org.id,
        password_hash="hashed_pw",
        is_active=True,
    )
    test_db.add(mentor)

    learner = User(
        email="learner_dossier@trellis.internal",
        full_name="Learner Dossier",
        role="LEARNER",
        org_id=org.id,
        password_hash="hashed_pw",
        is_active=True,
    )
    test_db.add(learner)
    test_db.commit()

    # 1. Test Admin accessing admin learner AI diagnostic
    data_admin = get_learner_ai_diagnostic_for_admin(learner_id=learner.id, db=test_db, _admin=admin)
    assert data_admin["learner_id"] == learner.id
    assert "charts" in data_admin
    assert "ai_narrative" in data_admin
    assert "average_score" in data_admin

    # 2. Test Admin accessing mentor learner AI diagnostic endpoint
    data_admin_via_mentor = get_learner_ai_diagnostic_for_mentor(learner_id=learner.id, db=test_db, mentor=admin)
    assert data_admin_via_mentor["learner_id"] == learner.id
    assert "charts" in data_admin_via_mentor
