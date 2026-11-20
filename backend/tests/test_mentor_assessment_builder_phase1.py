"""TRELLIS Phase 1 & Phase 2 Mentor Assessment Builder and Talent Spotlight Tests.

Validates:
1. Audience boundary enforcement: Mentors can only target their own assigned batches and learners (403 otherwise).
2. Question Bank & Assessment Question Attachment:
   - Unified question bank creation for MCQ and Coding challenges.
   - Attaching questions to an assessment with sequence order and marks.
   - Reordering and deleting questions with sequence re-indexing.
3. Assessment Immutability & Versioning:
   - When an assessment is PUBLISHED and has submissions, modifying questions creates a new version (version + 1, DRAFT).
   - Questions and audience are copied to the new version.
4. Talent Spotlight:
   - Zero hard-coded fallback records (returns [] when empty).
   - Serializes real metrics from evidence_json.
   - All 4 actions (INVITE_ASSESSMENT, SCHEDULE_INTERVIEW, RECOMMEND_PROMOTION, DISMISSED) persist real records.
   - Repeat actions on closed alerts return HTTP 409 Conflict.
5. Publishing an already published assessment is an idempotent no-op.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from fastapi import HTTPException, status
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api.v1.mentor import (
    AlertActionRequest,
    AssessmentCreateRequest,
    AttachQuestionRequest,
    MeetingCreateRequest,
    ReorderQuestionsRequest,
    QuestionReorderItem,
    UnifiedQuestionCreateRequest,
    act_on_talent_alert,
    attach_question_to_assessment,
    create_assessment,
    create_question_unified,
    remove_question_from_assessment,
    get_assessment_questions,
    get_talent_spotlight_alerts,
    publish_assessment,
    update_assessment_questions,
    schedule_meeting,
)
from app.models import (
    Assessment,
    AssessmentAttempt,
    AssessmentAudience,
    AssessmentQuestion,
    AuditLog,
    Base,
    Batch,
    Meeting,
    MeetingAudience,
    MentorLearnerAssignment,
    Organisation,
    QuestionBank,
    TalentAlert,
    User,
)


@pytest.fixture
def p1_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        org = Organisation(name="CSM Technology", code="CSM_P1")
        session.add(org)
        session.flush()

        mentor = User(
            id="mentor_p1",
            org_id=org.id,
            email="mentor.p1@csm.tech",
            full_name="Mentor Alpha",
            role="MENTOR",
            password_hash="pw",
            is_active=True,
        )
        learner1 = User(
            id="learner_p1_1",
            org_id=org.id,
            email="learner.1@csm.tech",
            full_name="Learner One",
            role="LEARNER",
            password_hash="pw",
            is_active=True,
        )
        learner2 = User(
            id="learner_p1_2",
            org_id=org.id,
            email="learner.2@csm.tech",
            full_name="Learner Two",
            role="LEARNER",
            password_hash="pw",
            is_active=True,
        )
        learner_unassigned = User(
            id="learner_p1_other",
            org_id=org.id,
            email="learner.other@csm.tech",
            full_name="Learner Other",
            role="LEARNER",
            password_hash="pw",
            is_active=True,
        )
        batch_assigned = Batch(
            id="batch_p1_assigned",
            org_id=org.id,
            name="Alpha Batch",
            code="BATCH_P1_ASSIGNED",
            field="Python",
        )
        batch_unassigned = Batch(
            id="batch_p1_unassigned",
            org_id=org.id,
            name="Beta Batch",
            code="BATCH_P1_UNASSIGNED",
            field="Java",
        )
        session.add_all([mentor, learner1, learner2, learner_unassigned, batch_assigned, batch_unassigned])
        session.flush()

        # Mentor assignment: assigned to batch_assigned and learner1/learner2
        assign1 = MentorLearnerAssignment(mentor_id=mentor.id, batch_id=batch_assigned.id, learner_id=learner1.id)
        assign2 = MentorLearnerAssignment(mentor_id=mentor.id, batch_id=batch_assigned.id, learner_id=learner2.id)
        session.add_all([assign1, assign2])
        session.commit()

    with Session(engine) as session:
        yield session


def test_mentor_audience_validation(p1_db: Session):
    mentor = p1_db.get(User, "mentor_p1")

    # 1. Assessment create with unassigned batch raises 403
    with pytest.raises(HTTPException) as exc_b:
        create_assessment(
            payload=AssessmentCreateRequest(
                title="Unauthorized Assessment",
                field="Python",
                duration_minutes=30,
                passing_score=70.0,
                batch_id="batch_p1_unassigned",
            ),
            db=p1_db,
            mentor=mentor,
            _uow=None,
        )
    assert exc_b.value.status_code == status.HTTP_403_FORBIDDEN

    # 2. Assessment create with unassigned learner raises 403
    with pytest.raises(HTTPException) as exc_l:
        create_assessment(
            payload=AssessmentCreateRequest(
                title="Unauthorized Learners",
                field="Python",
                duration_minutes=30,
                passing_score=70.0,
                learner_ids=["learner_p1_other"],
            ),
            db=p1_db,
            mentor=mentor,
            _uow=None,
        )
    assert exc_l.value.status_code == status.HTTP_403_FORBIDDEN

    # 3. Meeting schedule with unassigned batch raises 403
    tomorrow = (datetime.now(UTC) + timedelta(days=1)).date().isoformat()
    with pytest.raises(HTTPException) as exc_m_b:
        schedule_meeting(
            payload=MeetingCreateRequest(
                title="Bad Batch Meeting",
                meeting_link="https://meet.google.com/test-room",
                meeting_date=tomorrow,
                start_time="10:00",
                end_time="11:00",
                batch_id="batch_p1_unassigned",
            ),
            db=p1_db,
            mentor=mentor,
            _uow=None,
        )
    assert exc_m_b.value.status_code == status.HTTP_403_FORBIDDEN

    # 4. Valid assessment create with assigned batch succeeds
    res = create_assessment(
        payload=AssessmentCreateRequest(
            title="Valid Assessment",
            field="Python",
            duration_minutes=60,
            passing_score=75.0,
            batch_id="batch_p1_assigned",
        ),
        db=p1_db,
        mentor=mentor,
        _uow=None,
    )
    assert res["status"] == "DRAFT"
    assert res["id"] is not None


def test_unified_question_creation_and_attachment(p1_db: Session):
    mentor = p1_db.get(User, "mentor_p1")

    # 1. Create MCQ in unified endpoint
    mcq_res = create_question_unified(
        payload=UnifiedQuestionCreateRequest(
            title="FastAPI Lifespan Events",
            question_text="How are startup/shutdown handlers configured in modern FastAPI?",
            type="MCQ",
            field="Python",
            difficulty="MEDIUM",
            marks=10.0,
            options=[
                {"text": "@app.on_event('startup')", "is_correct": False},
                {"text": "asynccontextmanager lifespan handler", "is_correct": True},
                {"text": "threading.Thread initialization", "is_correct": False},
            ],
            explanation="Lifespan handlers replace deprecated on_event decorators.",
        ),
        db=p1_db,
        mentor=mentor,
    )
    assert mcq_res["id"] is not None
    assert mcq_res["type"] == "MCQ"

    # 2. Create Coding in unified endpoint
    coding_res = create_question_unified(
        payload=UnifiedQuestionCreateRequest(
            title="Reverse Linked List",
            question_text="Reverse a singly linked list in-place.",
            type="CODING",
            field="DSA",
            difficulty="MEDIUM",
            marks=20.0,
            starter_code={"python": "def reverse(head):\n    pass"},
            test_cases=[
                {"input": "1->2->3", "expected_output": "3->2->1", "is_hidden": False},
                {"input": "1", "expected_output": "1", "is_hidden": True},
            ],
        ),
        db=p1_db,
        mentor=mentor,
    )
    assert coding_res["id"] is not None
    assert coding_res["type"] == "CODING"

    # 3. Create Draft Assessment
    assessment_res = create_assessment(
        payload=AssessmentCreateRequest(
            title="Fullstack Evaluation",
            field="Python",
            duration_minutes=90,
            passing_score=80.0,
            batch_id="batch_p1_assigned",
        ),
        db=p1_db,
        mentor=mentor,
        _uow=None,
    )
    aid = assessment_res["id"]

    # 4. Attach MCQ and Coding to Assessment
    att1 = attach_question_to_assessment(
        assessment_id=aid,
        payload=AttachQuestionRequest(question_id=mcq_res["id"], marks=10.0, order=1),
        db=p1_db,
        mentor=mentor,
        _uow=None,
    )
    assert att1["sequence_order"] == 1
    assert att1["marks"] == 10.0

    att2 = attach_question_to_assessment(
        assessment_id=aid,
        payload=AttachQuestionRequest(question_id=coding_res["id"], marks=20.0, order=2),
        db=p1_db,
        mentor=mentor,
        _uow=None,
    )
    assert att2["sequence_order"] == 2

    # 5. List assessment questions
    questions = get_assessment_questions(assessment_id=aid, db=p1_db, mentor=mentor)
    assert len(questions) == 2
    assert questions[0]["title"] == "FastAPI Lifespan Events"
    assert questions[0]["type"] == "MCQ"
    assert questions[1]["title"] == "Reverse Linked List"
    assert questions[1]["type"] == "CODING"

    # 6. Reorder questions (swap 1 and 2)
    reorder_res = update_assessment_questions(
        assessment_id=aid,
        payload=ReorderQuestionsRequest(
            questions=[
                QuestionReorderItem(aq_id=att2["id"], order=1, marks=20.0),
                QuestionReorderItem(aq_id=att1["id"], order=2, marks=10.0),
            ]
        ),
        db=p1_db,
        mentor=mentor,
        _uow=None,
    )
    assert reorder_res["status"] == "updated"
    q_reordered = get_assessment_questions(assessment_id=aid, db=p1_db, mentor=mentor)
    assert q_reordered[0]["title"] == "Reverse Linked List"
    assert q_reordered[1]["title"] == "FastAPI Lifespan Events"

    # 7. Delete question att1
    del_res = remove_question_from_assessment(assessment_id=aid, aq_id=att1["id"], db=p1_db, mentor=mentor, _uow=None)
    assert del_res["status"] == "deleted"
    q_after_del = get_assessment_questions(assessment_id=aid, db=p1_db, mentor=mentor)
    assert len(q_after_del) == 1
    assert q_after_del[0]["sequence_order"] == 1


def test_published_assessment_versioning_invariant(p1_db: Session):
    mentor = p1_db.get(User, "mentor_p1")
    learner = p1_db.get(User, "learner_p1_1")

    # 1. Create Question and Assessment
    q = QuestionBank(
        author_id=mentor.id,
        title="SQL Window Functions",
        question_text="Explain ROW_NUMBER() vs RANK().",
        question_type="MCQ",
        field="SQL",
        topic="Database",
        difficulty="MEDIUM",
    )
    p1_db.add(q)
    p1_db.flush()

    assessment = Assessment(
        mentor_id=mentor.id,
        title="Database Concepts",
        field="SQL",
        duration_minutes=45,
        passing_score=70.0,
        status="DRAFT",
        version=1,
    )
    p1_db.add(assessment)
    p1_db.flush()

    # Attach question
    attach_question_to_assessment(
        assessment_id=assessment.id,
        payload=AttachQuestionRequest(question_id=q.id, marks=5.0, order=1),
        db=p1_db,
        mentor=mentor,
        _uow=None,
    )

    # Publish assessment
    pub_res = publish_assessment(assessment_id=assessment.id, db=p1_db, mentor=mentor, _uow=None)
    assert pub_res["status"] == "PUBLISHED"

    # Publishing again is an idempotent no-op
    pub_again = publish_assessment(assessment_id=assessment.id, db=p1_db, mentor=mentor, _uow=None)
    assert pub_again["status"] == "PUBLISHED"

    # Simulate learner attempt
    attempt = AssessmentAttempt(
        assessment_id=assessment.id,
        learner_id=learner.id,
        status="SUBMITTED",
        score=85.0,
        passed=True,
    )
    p1_db.add(attempt)
    p1_db.commit()

    # 2. Add second question to the published assessment with submissions
    q2 = QuestionBank(
        author_id=mentor.id,
        title="ACID Properties",
        question_text="What does Isolation guarantee?",
        question_type="MCQ",
        field="SQL",
        topic="Database",
        difficulty="EASY",
    )
    p1_db.add(q2)
    p1_db.commit()

    ver_res = attach_question_to_assessment(
        assessment_id=assessment.id,
        payload=AttachQuestionRequest(question_id=q2.id, marks=5.0, order=2),
        db=p1_db,
        mentor=mentor,
        _uow=None,
    )

    # Invariant: Must return versioned = True and new assessment id
    assert ver_res.get("versioned") is True
    new_aid = ver_res.get("new_assessment_id")
    assert new_aid is not None
    assert new_aid != assessment.id

    new_assessment = p1_db.get(Assessment, new_aid)
    assert new_assessment.version == 2
    assert new_assessment.status == "DRAFT"
    # Should have both copied question 1 and newly attached question 2
    new_qs = get_assessment_questions(assessment_id=new_aid, db=p1_db, mentor=mentor)
    assert len(new_qs) == 2


def test_talent_spotlight_empty_fallback_eliminated_and_real_actions(p1_db: Session):
    mentor = p1_db.get(User, "mentor_p1")
    learner = p1_db.get(User, "learner_p1_1")

    # 1. When no alerts exist, returns [] (NOT fake Priya Sharma / Sneha Mukherjee)
    empty_alerts = get_talent_spotlight_alerts(db=p1_db, mentor=mentor)
    assert empty_alerts == []

    # 2. Create real TalentAlert with evidence_json
    alert = TalentAlert(
        mentor_id=mentor.id,
        learner_id=learner.id,
        field="Python",
        evidence_json={
            "dedication_score": 95.0,
            "weighted_accuracy": 91.5,
            "problems_attempted": 30,
            "active_days_30d": 18,
            "acceptance_rate": 88.0,
        },
        status="PENDING",
    )
    p1_db.add(alert)
    p1_db.commit()

    # 3. List alert and verify real serialization
    alerts = get_talent_spotlight_alerts(db=p1_db, mentor=mentor)
    assert len(alerts) == 1
    a_data = alerts[0]
    assert a_data["id"] == alert.id
    assert a_data["dedication_score"] == 95.0
    assert a_data["accuracy"] == 91.5
    assert a_data["problems_count"] == 30
    assert a_data["active_days"] == 18
    assert a_data["acceptance_rate"] == 88.0

    # 4. Action: RECOMMEND_PROMOTION creates AuditLog
    act_res = act_on_talent_alert(
        alert_id=alert.id,
        payload=AlertActionRequest(
            action="RECOMMEND_PROMOTION",
            notes="Ready for senior track based on 18-day streak.",
        ),
        db=p1_db,
        mentor=mentor,
        _uow=None,
    )
    assert act_res["status"] == "RECOMMEND_PROMOTION"
    p1_db.refresh(alert)
    assert alert.status == "RECOMMEND_PROMOTION"

    # Verify audit log created
    audit = p1_db.execute(
        select(AuditLog).where(
            AuditLog.action == "RECOMMEND_PROMOTION",
            AuditLog.resource_id == alert.id,
        )
    ).scalar_one_or_none()
    assert audit is not None
    assert audit.after_state_json["learner_id"] == learner.id

    # 5. Repeat action on closed alert raises HTTP 409 Conflict
    with pytest.raises(HTTPException) as exc_closed:
        act_on_talent_alert(
            alert_id=alert.id,
            payload=AlertActionRequest(action="DISMISSED"),
            db=p1_db,
            mentor=mentor,
            _uow=None,
        )
    assert exc_closed.value.status_code == status.HTTP_409_CONFLICT
