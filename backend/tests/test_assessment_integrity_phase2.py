"""TRELLIS Phase 2 Assessment Integrity Tests.

Validates:
1. Cross-batch start returns 404 (learner cannot access an assessment outside their batch/audience).
2. Explicit audience grants access across batches.
3. Server-side timer: Late submit / autosave rejected with 400 and marks attempt EXPIRED.
4. Coding questions are graded in assessments using best stored Submission, computing earned percentage.
5. Learner with no attempts gets [] not 500 (fixing 'true' NameError and deleting fake 'res1').
6. Mentor target validation: unassigned batch or learner returns 403 on create/edit.
7. Publish idempotency: publishing an already published assessment is a no-op with no duplicate notifications.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from fastapi import HTTPException, status
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api.v1.learner import (
    AutosaveRequest,
    SubmitAssessmentRequest,
    autosave_assessment,
    list_learner_assessments,
    list_learner_results,
    start_assessment,
    submit_assessment,
)
from app.api.v1.mentor import (
    AssessmentCreateRequest,
    MeetingCreateRequest,
    create_assessment,
    publish_assessment,
    schedule_meeting,
)
from app.models import (
    Answer,
    Assessment,
    AssessmentAttempt,
    AssessmentAudience,
    AssessmentQuestion,
    Base,
    Batch,
    CodingProblem,
    McqOption,
    Meeting,
    MeetingAudience,
    MentorLearnerAssignment,
    Notification,
    Organisation,
    QuestionBank,
    Submission,
    User,
)


@pytest.fixture
def p2_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        org = Organisation(name="CSM Technology", code="CSM_P2")
        session.add(org)
        session.flush()

        mentor1 = User(
            id="mentor_p2_1",
            org_id=org.id,
            email="mentor1@example.com",
            password_hash="hashed_pw",
            full_name="Mentor One",
            role="MENTOR",
            is_active=True,
        )
        learner1 = User(
            id="learner_p2_1",
            org_id=org.id,
            email="learner1@example.com",
            password_hash="hashed_pw",
            full_name="Learner One",
            role="LEARNER",
            is_active=True,
        )
        learner2 = User(
            id="learner_p2_2",
            org_id=org.id,
            email="learner2@example.com",
            password_hash="hashed_pw",
            full_name="Learner Two",
            role="LEARNER",
            is_active=True,
        )
        session.add_all([mentor1, learner1, learner2])

        batch_a = Batch(id="batch_a", name="Batch Alpha", code="BATCH_A", org_id=org.id)
        batch_b = Batch(id="batch_b", name="Batch Beta", code="BATCH_B", org_id=org.id)
        session.add_all([batch_a, batch_b])

        # Assign mentor1 to batch_a and learner1
        asgn1 = MentorLearnerAssignment(
            mentor_id=mentor1.id,
            learner_id=learner1.id,
            batch_id=batch_a.id,
        )
        session.add(asgn1)

        # learner2 belongs to batch_b (assigned to someone else)
        asgn2 = MentorLearnerAssignment(
            mentor_id="other_mentor",
            learner_id=learner2.id,
            batch_id=batch_b.id,
        )
        session.add(asgn2)

        session.commit()
        yield session


def test_learner_with_no_attempts_gets_empty_list_not_500(p2_db: Session):
    learner1 = p2_db.get(User, "learner_p2_1")
    results = list_learner_results(db=p2_db, learner=learner1)
    assert results == []

    assessments = list_learner_assessments(db=p2_db, learner=learner1)
    assert assessments == []


def test_cross_batch_start_returns_404(p2_db: Session):
    mentor1 = p2_db.get(User, "mentor_p2_1")
    learner1 = p2_db.get(User, "learner_p2_1")

    # Assessment published for batch_b (learner1 is in batch_a)
    assessment = Assessment(
        mentor_id=mentor1.id,
        batch_id="batch_b",
        title="Batch B Exclusive Assessment",
        field="Python",
        duration_minutes=30,
        passing_score=70,
        status="PUBLISHED",
        version=1,
    )
    p2_db.add(assessment)
    p2_db.commit()

    with pytest.raises(HTTPException) as exc_info:
        start_assessment(
            assessment_id=assessment.id,
            db=p2_db,
            learner=learner1,
            _uow=None,
        )
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert "not assigned" in exc_info.value.detail.lower()


def test_explicit_audience_allows_access(p2_db: Session):
    mentor1 = p2_db.get(User, "mentor_p2_1")
    learner1 = p2_db.get(User, "learner_p2_1")

    # Assessment created for batch_b, but learner1 is in explicit audience
    assessment = Assessment(
        mentor_id=mentor1.id,
        batch_id="batch_b",
        title="Invited Assessment",
        field="Python",
        duration_minutes=30,
        passing_score=70,
        status="PUBLISHED",
        version=1,
    )
    p2_db.add(assessment)
    p2_db.flush()

    p2_db.add(AssessmentAudience(assessment_id=assessment.id, learner_id=learner1.id))
    p2_db.commit()

    # learner1 can now access and start it
    res = start_assessment(
        assessment_id=assessment.id,
        db=p2_db,
        learner=learner1,
        _uow=None,
    )
    assert res["assessment_id"] == assessment.id
    assert res["remaining_seconds"] > 0


def test_late_submit_and_autosave_rejected(p2_db: Session):
    mentor1 = p2_db.get(User, "mentor_p2_1")
    learner1 = p2_db.get(User, "learner_p2_1")

    assessment = Assessment(
        mentor_id=mentor1.id,
        batch_id="batch_a",
        title="Timed Assessment",
        field="Python",
        duration_minutes=5,
        passing_score=60,
        status="PUBLISHED",
        version=1,
    )
    p2_db.add(assessment)
    p2_db.flush()

    attempt = AssessmentAttempt(
        assessment_id=assessment.id,
        learner_id=learner1.id,
        start_time=datetime.now(UTC) - timedelta(minutes=10),  # 10 mins ago for 5 min test
        total_marks=100.0,
        status="IN_PROGRESS",
    )
    p2_db.add(attempt)
    p2_db.commit()

    # Autosave must be rejected
    with pytest.raises(HTTPException) as exc_info:
        autosave_assessment(
            assessment_id=assessment.id,
            payload=AutosaveRequest(answers={"q1": "val"}),
            db=p2_db,
            learner=learner1,
            _uow=None,
        )
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "expired" in exc_info.value.detail.lower()

    # Attempt status should now be EXPIRED
    p2_db.refresh(attempt)
    assert attempt.status == "EXPIRED"

    # Submit must also be rejected
    with pytest.raises(HTTPException) as exc_info2:
        submit_assessment(
            assessment_id=assessment.id,
            payload=SubmitAssessmentRequest(answers={}),
            db=p2_db,
            learner=learner1,
            _uow=None,
        )
    assert exc_info2.value.status_code == status.HTTP_400_BAD_REQUEST


def test_coding_score_counted_in_assessment(p2_db: Session):
    mentor1 = p2_db.get(User, "mentor_p2_1")
    learner1 = p2_db.get(User, "learner_p2_1")

    assessment = Assessment(
        mentor_id=mentor1.id,
        batch_id="batch_a",
        title="Comprehensive Assessment",
        field="Python",
        duration_minutes=60,
        passing_score=75.0,  # 75%
        status="PUBLISHED",
        version=1,
    )
    p2_db.add(assessment)
    p2_db.flush()

    # Add 1 MCQ Question (40 marks)
    mcq = QuestionBank(
        author_id=mentor1.id,
        title="Python Dict Time Complexity",
        question_text="What is the average lookup complexity?",
        field="Python",
        topic="Data Structures",
        difficulty="EASY",
        question_type="MCQ",
    )
    p2_db.add(mcq)
    p2_db.flush()

    opt_correct = McqOption(question_id=mcq.id, option_text="O(1)", is_correct=True, sequence_order=1)
    opt_wrong = McqOption(question_id=mcq.id, option_text="O(n)", is_correct=False, sequence_order=2)
    p2_db.add_all([opt_correct, opt_wrong])
    p2_db.flush()

    aq_mcq = AssessmentQuestion(
        assessment_id=assessment.id,
        bank_question_id=mcq.id,
        marks=40.0,
        sequence_order=1,
    )
    p2_db.add(aq_mcq)

    # Add 1 Coding Question (60 marks)
    code_q = QuestionBank(
        author_id=mentor1.id,
        title="Reverse List",
        question_text="Reverse given list",
        field="Python",
        topic="Algorithms",
        difficulty="MEDIUM",
        question_type="CODING",
    )
    p2_db.add(code_q)
    p2_db.flush()

    cp = CodingProblem(
        bank_id=code_q.id,
        title="Reverse List",
        description="Reverse list",
        field="Python",
    )
    p2_db.add(cp)
    p2_db.flush()

    aq_code = AssessmentQuestion(
        assessment_id=assessment.id,
        bank_question_id=code_q.id,
        marks=60.0,
        sequence_order=2,
    )
    p2_db.add(aq_code)

    attempt = AssessmentAttempt(
        assessment_id=assessment.id,
        learner_id=learner1.id,
        start_time=datetime.now(UTC),
        total_marks=100.0,
        status="IN_PROGRESS",
    )
    p2_db.add(attempt)
    p2_db.flush()

    # Simulate a stored submission for coding problem: score = 50.0 (50% test cases pass -> (50/100)*60 = 30 marks)
    sub = Submission(
        attempt_id=attempt.id,
        coding_problem_id=cp.id,
        learner_id=learner1.id,
        code="def reverse(l): return l[::-1]",
        language="python",
        verdict="WRONG_ANSWER",
        score=50.0,
        total_cases=2,
        passed_cases=1,
    )
    p2_db.add(sub)
    p2_db.commit()

    # Submit: MCQ is correct (40 marks) + Coding gets 30 marks = 70 marks total (70%)
    # Since passing_score is 75%, 70% is NOT passed.
    res = submit_assessment(
        assessment_id=assessment.id,
        payload=SubmitAssessmentRequest(
            answers={
                mcq.id: {"selected_options": [opt_correct.id]},
                code_q.id: {},
            }
        ),
        db=p2_db,
        learner=learner1,
        _uow=None,
    )
    assert res["score"] == 70.0
    assert res["passed"] is False

    # Now test with 100% coding score (60 marks) -> 40 + 60 = 100 marks -> Passed
    p2_db.execute(
        select(AssessmentAttempt).where(AssessmentAttempt.id == attempt.id)
    )
    sub.score = 100.0
    attempt.status = "IN_PROGRESS"
    p2_db.commit()

    res2 = submit_assessment(
        assessment_id=assessment.id,
        payload=SubmitAssessmentRequest(
            answers={
                mcq.id: {"selected_options": [opt_correct.id]},
                code_q.id: {},
            }
        ),
        db=p2_db,
        learner=learner1,
        _uow=None,
    )
    assert res2["score"] == 100.0
    assert res2["passed"] is True


def test_mentor_unassigned_batch_or_learner_returns_403(p2_db: Session):
    mentor1 = p2_db.get(User, "mentor_p2_1")

    # mentor1 is only assigned to batch_a and learner1.
    # Trying to schedule meeting for batch_b should return 403.
    with pytest.raises(HTTPException) as exc_info:
        schedule_meeting(
            payload=MeetingCreateRequest(
                title="Invalid Batch Meeting",
                meeting_date=datetime.now(UTC).date().isoformat(),
                start_time="10:00",
                end_time="11:00",
                duration_minutes=60,
                meeting_link="https://meet.google.com/abc-defg-hij",
                batch_id="batch_b",
            ),
            db=p2_db,
            mentor=mentor1,
            _uow=None,
        )
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN

    # Trying to create assessment for unassigned learner2 should return 403.
    with pytest.raises(HTTPException) as exc_info2:
        create_assessment(
            payload=AssessmentCreateRequest(
                title="Unauthorized Target Assessment",
                field="Python",
                duration_minutes=30,
                passing_score=70,
                learner_ids=["learner_p2_2"],
            ),
            db=p2_db,
            mentor=mentor1,
            _uow=None,
        )
    assert exc_info2.value.status_code == status.HTTP_403_FORBIDDEN


def test_publish_already_published_is_noop(p2_db: Session):
    mentor1 = p2_db.get(User, "mentor_p2_1")

    assessment = Assessment(
        mentor_id=mentor1.id,
        batch_id="batch_a",
        title="Idempotent Publish Assessment",
        field="Python",
        duration_minutes=30,
        passing_score=70,
        status="DRAFT",
        version=1,
    )
    p2_db.add(assessment)
    p2_db.flush()

    # Add a dummy question so publish is allowed
    q = QuestionBank(
        author_id=mentor1.id,
        title="Dummy Q",
        question_text="Q text",
        field="Python",
        topic="General",
        question_type="MCQ",
    )
    p2_db.add(q)
    p2_db.flush()
    p2_db.add(AssessmentQuestion(assessment_id=assessment.id, bank_question_id=q.id, marks=10.0))
    p2_db.commit()

    # First publish
    res1 = publish_assessment(assessment_id=assessment.id, db=p2_db, mentor=mentor1, _uow=None)
    assert res1["status"] == "PUBLISHED"

    notif_count_1 = len(
        p2_db.execute(select(Notification).where(Notification.title.contains("Idempotent Publish"))).scalars().all()
    )
    assert notif_count_1 >= 1

    # Second publish must be no-op with no additional notifications
    res2 = publish_assessment(assessment_id=assessment.id, db=p2_db, mentor=mentor1, _uow=None)
    assert res2["status"] == "PUBLISHED"
    assert "already published" in res2["message"]

    notif_count_2 = len(
        p2_db.execute(select(Notification).where(Notification.title.contains("Idempotent Publish"))).scalars().all()
    )
    assert notif_count_2 == notif_count_1
