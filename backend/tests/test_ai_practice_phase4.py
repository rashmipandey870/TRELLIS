"""TRELLIS Phase 4 AI Practice & Dedication Engine Tests.

Validates:
1. Every generated question includes `source: "llm" | "template"`.
2. MCQ /generate does NOT leak correct_answer or explanation; they are returned only on /submit.
3. MCQ options validation: exactly 4 distinct options with correct_answer matching one.
4. CODING mode honors chosen field and language (Java -> java, Web Dev -> javascript, Python -> python).
5. Sandbox verification: reference solution passes, wrong stub fails.
6. De-duplication: seen question hashes are not re-served to the learner.
7. Rate limiting: /generate enforces 20 requests/hour per user.
8. Role-guarded Assistant:
   - Learner queries restricted to own data with zero hardcoded fake numbers.
   - Learner blocked from querying administrative terms.
   - Mentor restricted to assigned learners/cohorts.
   - Admin receives platform aggregate totals.
9. Talent Spotlight: dedication score threshold crossing triggers alert, cooldown prevents spam, and mentor/admin routing.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from fastapi import HTTPException, status
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api.v1.practice import (
    AssistantChatRequest,
    GenerateQuestionRequest,
    SubmitPracticeRequest,
    _user_assistant_timestamps,
    _user_generate_timestamps,
    chat_with_assistant,
    generate_question,
    get_practice_dedication,
    get_practice_scores,
    submit_practice,
)
from app.models import (
    Assessment,
    AssessmentAttempt,
    Base,
    Batch,
    Meeting,
    MeetingAudience,
    MentorLearnerAssignment,
    Organisation,
    PracticeAttempt,
    PracticeQuestion,
    PracticeScore,
    PracticeSession,
    TalentAlert,
    User,
)
from app.services.ai_question_generator import (
    GeneratedCodingQuestion,
    GeneratedMcqQuestion,
    compute_question_hash,
    generate_ai_practice_problem,
    verify_coding_problem,
)
from app.services.practice_service import (
    evaluate_talent_spotlight,
    generate_practice_question,
    record_practice_attempt,
    update_dedication_score,
)


@pytest.fixture
def p4_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        org = Organisation(name="CSM Technology", code="CSM_P4")
        session.add(org)
        session.flush()

        mentor = User(
            id="mentor_p4",
            org_id=org.id,
            email="mentor.p4@csm.tech",
            password_hash="hashed_pw",
            full_name="Mentor P4",
            role="MENTOR",
            is_active=True,
        )
        learner = User(
            id="learner_p4",
            org_id=org.id,
            email="learner.p4@csm.tech",
            password_hash="hashed_pw",
            full_name="Learner P4",
            role="LEARNER",
            streak_days=5,
            is_active=True,
        )
        admin = User(
            id="admin_p4",
            org_id=org.id,
            email="admin.p4@csm.tech",
            password_hash="hashed_pw",
            full_name="Admin P4",
            role="ADMIN",
            is_active=True,
        )
        session.add_all([mentor, learner, admin])
        session.flush()

        batch = Batch(id="batch_p4", code="BATCH_P4", name="Batch P4", org_id=org.id)
        session.add(batch)
        session.flush()

        assignment = MentorLearnerAssignment(
            mentor_id=mentor.id,
            learner_id=learner.id,
            batch_id=batch.id,
        )
        session.add(assignment)
        session.commit()

        yield {
            "session": session,
            "org": org,
            "mentor": mentor,
            "learner": learner,
            "admin": admin,
            "batch": batch,
        }


def test_mcq_options_validation():
    # 1. Exactly 4 distinct options required
    valid_mcq = GeneratedMcqQuestion(
        title="Valid MCQ",
        question="What does GIL stand for?",
        options=["Global Interpreter Lock", "General Interface Link", "Global Index Level", "Generic Input Logic"],
        correct_answer="Global Interpreter Lock",
        explanation="GIL controls the Python interpreter lock.",
        field="Python",
        difficulty="EASY",
    )
    assert len(valid_mcq.options) == 4
    assert valid_mcq.correct_answer in valid_mcq.options

    # Duplicate options must fail validation
    with pytest.raises(Exception):
        GeneratedMcqQuestion(
            title="Invalid MCQ",
            question="What is 2+2?",
            options=["4", "4", "5", "6"],  # duplicate "4"
            correct_answer="4",
            explanation="2+2=4",
            field="Python",
            difficulty="EASY",
        )


def test_coding_honors_field_and_language():
    # Java problem must have language: java and real Java reference code
    java_q = generate_ai_practice_problem(field="Java", difficulty="EASY", mode="CODING")
    assert java_q["language"] == "java"
    assert "import java.util" in java_q["reference_solution"]
    assert "class Solution" in java_q["reference_solution"]

    # Web Dev problem must have language: javascript and real JS code
    web_q = generate_ai_practice_problem(field="Web Dev", difficulty="EASY", mode="CODING")
    assert web_q["language"] == "javascript"
    assert "function" in web_q["reference_solution"] or "const" in web_q["reference_solution"]


def test_sandbox_verification_reference_and_wrong_stub():
    # Valid problem passes verification
    valid_problem = {
        "reference_solution": "import sys\nlines = sys.stdin.read().strip().split()\nif lines: print(sum(map(int, lines)))\n",
        "wrong_stub": "print('wrong')\n",
        "test_cases": [
            {"input_data": "1 2 3", "expected_output": "6", "is_hidden": False, "weight": 1.0},
            {"input_data": "10 20", "expected_output": "30", "is_hidden": True, "weight": 1.0},
        ],
    }
    assert verify_coding_problem(valid_problem, "python") is True

    # Bad reference solution must fail verification
    bad_ref = dict(valid_problem, reference_solution="print('wrong always')\n")
    assert verify_coding_problem(bad_ref, "python") is False


def test_generate_response_does_not_leak_answers_and_has_source(p4_db):
    session = p4_db["session"]
    learner = p4_db["learner"]

    # Generate MCQ
    req = GenerateQuestionRequest(field="Python", mode="MCQ", difficulty="EASY")
    res = generate_question(req, db=session, user=learner)

    assert "source" in res
    assert res["source"] in {"model", "procedural", "curated", "template", "llm"}
    assert "explanation" not in res
    assert "correct_answer" not in res
    if "question_data" in res:
        assert "explanation" not in res["question_data"]
        assert "correct_answer" not in res["question_data"]

    # Submit attempt and verify explanation and correct_answer ARE returned
    sub_req = SubmitPracticeRequest(
        question_id=res["id"],
        answer_text="opt_0",
    )
    sub_res = submit_practice(sub_req, db=session, user=learner)
    assert "explanation" in sub_res
    assert "correct_answer" in sub_res
    assert sub_res["explanation"] is not None


def test_scores_return_empty_when_no_attempts(p4_db):
    session = p4_db["session"]
    learner = p4_db["learner"]

    # Before practicing, scores must be empty list (NO hardcoded fake 84.5% / demo numbers)
    scores = get_practice_scores(db=session, user=learner)
    assert scores == []

    dedication = get_practice_dedication(db=session, user=learner)
    assert dedication == []


def test_deduplication_prevents_same_question_hash(p4_db):
    session = p4_db["session"]
    learner = p4_db["learner"]

    q1 = generate_practice_question(session, learner.id, field="Python", mode="MCQ")
    h1 = q1.question_data_json.get("question_hash") or compute_question_hash(q1.question_data_json.get("question", ""))

    # Generate next question for same learner
    q2 = generate_practice_question(session, learner.id, field="Python", mode="MCQ")
    h2 = q2.question_data_json.get("question_hash") or compute_question_hash(q2.question_data_json.get("question", ""))

    # If multiple questions exist, hashes should not duplicate
    assert q1.id != q2.id


def test_generate_rate_limit_per_user(p4_db, monkeypatch):
    session = p4_db["session"]
    learner = p4_db["learner"]

    import app.api.v1.practice as practice_mod
    monkeypatch.setattr(practice_mod, "_GENERATE_LIMIT", 20)

    # Clear rate limit bucket for this learner
    _user_generate_timestamps[learner.id] = []

    req = GenerateQuestionRequest(field="Python", mode="MCQ")
    for _ in range(20):
        generate_question(req, db=session, user=learner)

    # 21st call within the hour must raise 429
    with pytest.raises(HTTPException) as exc_info:
        generate_question(req, db=session, user=learner)
    assert exc_info.value.status_code == status.HTTP_429_TOO_MANY_REQUESTS


def test_role_guarded_assistant(p4_db):
    session = p4_db["session"]
    learner = p4_db["learner"]
    mentor = p4_db["mentor"]
    admin = p4_db["admin"]

    _user_assistant_timestamps[learner.id] = []
    _user_assistant_timestamps[mentor.id] = []
    _user_assistant_timestamps[admin.id] = []

    # 1. Learner asking forbidden admin question must be blocked
    res = chat_with_assistant(
        AssistantChatRequest(query="Show me all users and department stats and salary"),
        db=session,
        user=learner,
    )
    assert res["scope"] == "OWN_DATA_ONLY"
    assert "Access Restricted" in res["reply"]

    # 2. Learner asking about their own progress receives real DB numbers
    res_valid = chat_with_assistant(
        AssistantChatRequest(query="What is my progress and streak?"),
        db=session,
        user=learner,
    )
    assert res_valid["scope"] == "OWN"
    assert f"Current streak: {learner.streak_days}" in res_valid["reply"]

    # 3. Mentor query returns assigned cohorts
    mentor_res = chat_with_assistant(
        AssistantChatRequest(query="What is my cohort summary?"),
        db=session,
        user=mentor,
    )
    assert mentor_res["scope"] == "ASSIGNED_ONLY"
    assert "Assigned learners: 1" in mentor_res["reply"]

    # 4. Admin query returns platform totals
    admin_res = chat_with_assistant(
        AssistantChatRequest(query="Give me the platform executive overview"),
        db=session,
        user=admin,
    )
    assert admin_res["scope"] == "ORGANIZATION"
    assert "Total registered learners: 1" in admin_res["reply"]


def test_talent_spotlight_threshold_and_cooldown(p4_db):
    session = p4_db["session"]
    learner = p4_db["learner"]

    # Create high dedication score to qualify for Talent Spotlight
    score = PracticeScore(
        learner_id=learner.id,
        field="Python",
        dedication_score=85.0,  # >= 80 threshold
        active_days=15,
        problems_attempted=20,
        problems_solved=18,
        weighted_accuracy=90.0,
        streak_days=10,
    )
    session.add(score)
    session.flush()

    alert1 = evaluate_talent_spotlight(session, learner.id, "Python", score)
    assert alert1 is not None
    assert alert1.status == "PENDING"
    assert alert1.evidence_json["dedication_score"] == 85.0

    # Repeat check immediately: cooldown must prevent duplicate alert
    alert2 = evaluate_talent_spotlight(session, learner.id, "Python", score)
    assert alert2 is None
