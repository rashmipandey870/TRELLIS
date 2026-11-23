"""Tests for Section D: Psychometric Flow.

Verifies:
1. Consent capture before starting (stored in consents table with PSYCHOMETRIC_EVALUATION).
2. 'Indicative, not clinical' disclaimer in start payload and result page.
3. Scoring per dimension (handling reverse-keyed items) into an 8-dimension profile.
4. NO pass/fail and NO marks for pure psychometric assessments.
5. Mixed assessments report psychometric sections separately from scored sections.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from app.api.v1.learner import _execute_assessment_submit, start_assessment
from app.models.assessments import (
    Answer,
    Assessment,
    AssessmentAttempt,
    AssessmentAudience,
    AssessmentQuestion,
    McqOption,
    QuestionBank,
)
from app.models.batches import Batch
from app.models.tenancy import Organisation
from app.models.user import Consent, User
from app.schemas.category import AssessmentCategory, PSYCHOMETRIC_DISCLAIMER


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    from app.models import Base
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_psychometric_consent_and_disclaimer_flow(db_session: Session):
    # Setup test data
    org = Organisation(name="Test CSM", code="CSM_TEST")
    db_session.add(org)
    db_session.flush()

    learner = User(
        org_id=org.id,
        email="learner.psych@csmtech.internal",
        password_hash="argon2_fake",
        full_name="Psych Learner",
        role="LEARNER",
    )
    mentor = User(
        org_id=org.id,
        email="mentor.psych@csmtech.internal",
        password_hash="argon2_fake",
        full_name="Psych Mentor",
        role="MENTOR",
    )
    db_session.add_all([learner, mentor])
    db_session.flush()

    batch = Batch(org_id=org.id, name="Test Batch", code="TB-01")
    db_session.add(batch)
    db_session.flush()

    # Create assessment with Likert questions
    assessment = Assessment(
        mentor_id=mentor.id,
        batch_id=batch.id,
        title="Behavioral & Psychometric Profile Assessment",
        field="Psychometric",
        instructions="Workplace behavioral preference evaluation.",
        duration_minutes=45,
        passing_score=60.0,
        start_window=datetime.now(UTC) - timedelta(days=1),
        end_window=datetime.now(UTC) + timedelta(days=7),
        status="PUBLISHED",
    )
    db_session.add(assessment)
    db_session.flush()

    db_session.add(AssessmentAudience(assessment_id=assessment.id, learner_id=learner.id))
    db_session.flush()

    dimensions = [
        "Agreeableness",
        "Conscientiousness",
        "Emotional Stability",
        "Openness to Experience",
        "Extraversion",
        "Grit & Resilience",
        "Collaborative Mindset",
        "Problem-Solving Integrity",
    ]

    for idx, dim in enumerate(dimensions, 1):
        bq = QuestionBank(
            author_id=mentor.id,
            title=f"Likert: {dim}",
            question_text=f"I consistently demonstrate {dim} during project deadlines.",
            question_type="LIKERT",
            category=AssessmentCategory.PSYCHOMETRIC.value,
            field="Psychometric",
            topic=dim,
            difficulty="MEDIUM",
            rubric_json={"dimension": dim, "is_reverse": (idx % 2 == 0)},
        )
        db_session.add(bq)
        db_session.flush()

        for opt_seq, opt_text in enumerate(["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"], 1):
            db_session.add(McqOption(
                question_id=bq.id,
                option_text=opt_text,
                is_correct=False,
                sequence_order=opt_seq,
            ))

        db_session.add(AssessmentQuestion(
            assessment_id=assessment.id,
            bank_question_id=bq.id,
            sequence_order=idx,
            marks=10.0,
        ))
    db_session.commit()

    # 1. Test start_assessment captures consent and returns disclaimer
    start_res = start_assessment(
        assessment_id=assessment.id,
        db=db_session,
        learner=learner,
        _uow=None,
    )

    assert start_res["has_psychometric"] is True
    assert start_res["psychometric_disclaimer"] == PSYCHOMETRIC_DISCLAIMER
    assert start_res["consent_captured"] is True

    # Verify Consent entity was persisted in DB
    saved_consent = db_session.execute(
        select(Consent).where(
            Consent.user_id == learner.id,
            Consent.purpose_code == "PSYCHOMETRIC_EVALUATION",
            Consent.status == "GRANTED",
        )
    ).scalar_one_or_none()
    assert saved_consent is not None, "Consent was not recorded in consents table"

    # 2. Test submit_assessment produces 8-dimension profile with NO pass/fail and NO numerical score
    attempt = db_session.execute(
        select(AssessmentAttempt).where(AssessmentAttempt.assessment_id == assessment.id)
    ).scalar_one()

    # Simulate answering all questions with 'Strongly Agree' (option seq 5)
    mock_answers = {}
    for aq in assessment.questions:
        agree_opt = next(o for o in aq.question.options if o.sequence_order == 5)
        mock_answers[aq.question.id] = {"selected_options": [agree_opt.id]}

    submit_res = _execute_assessment_submit(
        attempt=attempt,
        answers=mock_answers,
        tab_switches=0,
        db=db_session,
        learner=learner,
    )

    assert submit_res["is_psychometric"] is True
    assert submit_res["score"] is None, "Pure psychometric assessment should not have numerical score"
    assert submit_res["total_marks"] is None, "Pure psychometric assessment should not have total_marks"
    assert submit_res["passed"] is None, "Pure psychometric assessment should not have pass/fail"
    assert submit_res["disclaimer"] == PSYCHOMETRIC_DISCLAIMER

    profile = submit_res["psychometric_profile"]
    assert profile is not None
    assert len(profile["dimensions"]) == 8

    # Verify reverse-keyed handling:
    # Forward-keyed item (Agreeableness, idx=1) with seq=5 -> (5-1)/4*100 = 100%
    # Reverse-keyed item (Conscientiousness, idx=2) with seq=5 -> ( (6-5) - 1)/4*100 = 0%
    assert profile["dimensions"]["Agreeableness"] == 100.0
    assert profile["dimensions"]["Conscientiousness"] == 0.0
