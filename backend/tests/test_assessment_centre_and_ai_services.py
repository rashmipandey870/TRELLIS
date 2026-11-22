"""Automated Test Suite for Assessment Centre (7 Categories), Manual Grading,
Growth Ring AI Reports, and Gardener AI Chatbot.
"""

from __future__ import annotations

from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.security import hash_password
from app.models.assessments import (
    Answer,
    Assessment,
    AssessmentAttempt,
    AssessmentAudience,
    AssessmentQuestion,
    CodingProblem,
    McqOption,
    QuestionBank,
    TestCase,
)
from app.models.base import Base
from app.models.practice import PracticeAttempt, PracticeQuestion, PracticeScore
from app.models.tenancy import Organisation
from app.models.user import Role, User
from app.services.ai_analytics_engine import generate_growth_ring_report, generate_radar_chart_svg
from app.services.code_runner import CodeRunner, LocalSubprocessRunner
from app.services.gardener_service import check_and_record_rate_limit


@pytest.fixture
def db_engine() -> Generator[Engine, None, None]:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def db_session(db_engine: Engine) -> Generator[Session, None, None]:
    session = Session(db_engine)
    try:
        yield session
    finally:
        session.close()


def test_sql_code_runner_execution() -> None:
    """Verify LocalSubprocessRunner executes SQL queries against SQLite schemas."""
    runner = LocalSubprocessRunner()

    schema_seed = """
    CREATE TABLE employees (id INT, name TEXT, salary INT);
    INSERT INTO employees VALUES (1, 'Alice', 75000);
    INSERT INTO employees VALUES (2, 'Bob', 50000);
    INSERT INTO employees VALUES (3, 'Charlie', 90000);
    """

    test_cases = [
        {
            "input_data": schema_seed,
            "expected_output": "Charlie|90000\nAlice|75000",
            "is_hidden": False,
            "weight": 1.0,
        }
    ]

    # 1. Accepted Query
    query_ok = "SELECT name, salary FROM employees WHERE salary >= 75000 ORDER BY salary DESC;"
    res_ok = runner.execute(code=query_ok, language="sql", test_cases=test_cases)
    assert res_ok.verdict == "ACCEPTED"
    assert res_ok.passed_cases == 1
    assert res_ok.score == 100.0

    # 2. Wrong Answer
    query_wrong = "SELECT name, salary FROM employees WHERE salary < 60000;"
    res_wrong = runner.execute(code=query_wrong, language="sql", test_cases=test_cases)
    assert res_wrong.verdict == "WRONG_ANSWER"
    assert res_wrong.passed_cases == 0

    # 3. Runtime Error (SQL syntax error)
    query_syntax_err = "SELEKT * FROM nonexistent_tbl;"
    res_err = runner.execute(code=query_syntax_err, language="sql", test_cases=test_cases)
    assert res_err.verdict == "RUNTIME_ERROR"
    assert "syntax error" in (res_err.case_results[0].error_message or "").lower()


def test_assessment_categories_and_manual_grading_flow(db_session: Session) -> None:
    """Verify assessment with MCQ, Short Answer, File Upload, and manual mentor grading."""
    org = Organisation(name="CSM Tech", code="CSM_ASSESS_7")
    mentor_role = Role(code="MENTOR", name="Mentor", is_system_role=True)
    learner_role = Role(code="LEARNER", name="Learner", is_system_role=True)
    db_session.add_all([org, mentor_role, learner_role])
    db_session.flush()

    mentor = User(
        org_id=org.id,
        email="mentor7@csm.tech",
        password_hash=hash_password("Pass123!"),
        full_name="Mentor Devika",
        role="MENTOR",
    )
    learner = User(
        org_id=org.id,
        email="learner7@csm.tech",
        password_hash=hash_password("Pass123!"),
        full_name="Learner Rohan",
        role="LEARNER",
    )
    db_session.add_all([mentor, learner])
    db_session.flush()

    # 1. Create QuestionBank items for 3 categories
    # a. MCQ
    q_mcq = QuestionBank(
        author_id=mentor.id,
        title="Python Tuples",
        question_text="Are Python tuples mutable?",
        question_type="MCQ",
        field="Python",
        topic="Basics",
        difficulty="EASY",
    )
    db_session.add(q_mcq)
    db_session.flush()
    opt_no = McqOption(question_id=q_mcq.id, option_text="No", is_correct=True, sequence_order=1)
    opt_yes = McqOption(question_id=q_mcq.id, option_text="Yes", is_correct=False, sequence_order=2)
    db_session.add_all([opt_no, opt_yes])

    # b. SHORT_ANSWER
    q_short = QuestionBank(
        author_id=mentor.id,
        title="Explain ACID Properties",
        question_text="Explain Atomicity and Consistency in database transactions.",
        question_type="SHORT_ANSWER",
        field="Database",
        topic="Transactions",
        difficulty="MEDIUM",
        rubric_json={"criteria": "Must mention all-or-nothing and valid state transitions"},
    )
    # c. FILE_UPLOAD
    q_file = QuestionBank(
        author_id=mentor.id,
        title="System Architecture Diagram",
        question_text="Upload your microservices deployment topology diagram in PDF or PNG.",
        question_type="FILE_UPLOAD",
        field="Cloud Architecture",
        topic="Design",
        difficulty="HARD",
    )
    db_session.add_all([q_short, q_file])
    db_session.flush()

    # 2. Create Assessment with all 3 questions
    assessment = Assessment(
        mentor_id=mentor.id,
        title="Comprehensive Technical Evaluation",
        field="Engineering",
        duration_minutes=60,
        passing_score=70.0,
        status="PUBLISHED",
    )
    db_session.add(assessment)
    db_session.flush()

    aq1 = AssessmentQuestion(assessment_id=assessment.id, bank_question_id=q_mcq.id, marks=20.0, sequence_order=1)
    aq2 = AssessmentQuestion(assessment_id=assessment.id, bank_question_id=q_short.id, marks=40.0, sequence_order=2)
    aq3 = AssessmentQuestion(assessment_id=assessment.id, bank_question_id=q_file.id, marks=40.0, sequence_order=3)
    aud = AssessmentAudience(assessment_id=assessment.id, learner_id=learner.id)
    db_session.add_all([aq1, aq2, aq3, aud])
    db_session.commit()

    # 3. Learner Attempt & Submit
    attempt = AssessmentAttempt(
        assessment_id=assessment.id,
        learner_id=learner.id,
        total_marks=100.0,
        status="IN_PROGRESS",
    )
    db_session.add(attempt)
    db_session.commit()

    from app.api.v1.learner import _execute_assessment_submit
    answers = {
        q_mcq.id: {"selected_options": [opt_no.id]},
        q_short.id: {"text_response": "Atomicity ensures all-or-nothing execution. Consistency preserves integrity constraints."},
        q_file.id: {"file_url": "https://storage.csm.internal/uploads/topology.pdf", "file_name": "topology.pdf"},
    }

    res = _execute_assessment_submit(
        attempt=attempt,
        answers=answers,
        tab_switches=0,
        db=db_session,
        learner=learner,
    )

    db_session.refresh(attempt)
    assert attempt.status == "SUBMITTED"
    # Earned only MCQ score (20.0) initially; short answer & file upload are PENDING_REVIEW
    assert attempt.score == 20.0
    assert attempt.grading_status == "PENDING_REVIEW"

    # 4. Mentor Manual Grading
    from app.api.v1.mentor import GradeAttemptRequest, grade_attempt_answers

    ans_short = next(a for a in attempt.answers if a.bank_question_id == q_short.id)
    ans_file = next(a for a in attempt.answers if a.bank_question_id == q_file.id)

    grade_payload = GradeAttemptRequest(
        grades=[
            {"answer_id": ans_short.id, "score_awarded": 38.0, "feedback": "Accurate definitions."},
            {"answer_id": ans_file.id, "score_awarded": 36.0, "feedback": "Well-structured diagram."},
        ]
    )

    grade_res = grade_attempt_answers(
        attempt_id=attempt.id,
        payload=grade_payload,
        db=db_session,
        mentor=mentor,
    )

    assert grade_res["status"] == "success"
    db_session.refresh(attempt)
    # Total = 20 (MCQ) + 38 (Short) + 36 (File) = 94.0
    assert attempt.score == 94.0
    assert attempt.passed is True
    assert attempt.grading_status == "GRADED"


def test_growth_ring_report_generation_and_approval(db_session: Session) -> None:
    """Verify Growth Ring AI report generation and mentor approval."""
    org = Organisation(name="CSM Tech", code="CSM_GROWTH")
    db_session.add(org)
    db_session.flush()

    mentor = User(
        org_id=org.id,
        email="mentor_g@csm.tech",
        password_hash=hash_password("Pass123!"),
        full_name="Mentor Ananya",
        role="MENTOR",
    )
    learner = User(
        org_id=org.id,
        email="learner_g@csm.tech",
        password_hash=hash_password("Pass123!"),
        full_name="Learner Vikram",
        role="LEARNER",
    )
    db_session.add_all([mentor, learner])
    db_session.flush()

    assessment = Assessment(
        mentor_id=mentor.id,
        title="Full Stack Capstone Assessment",
        passing_score=60.0,
        status="PUBLISHED",
    )
    db_session.add(assessment)
    db_session.flush()

    attempt = AssessmentAttempt(
        assessment_id=assessment.id,
        learner_id=learner.id,
        score=85.0,
        total_marks=100.0,
        passed=True,
        status="SUBMITTED",
        grading_status="GRADED",
    )
    db_session.add(attempt)
    db_session.commit()

    # Generate Report
    report = generate_growth_ring_report(attempt.id, db_session)
    assert report["score"] == 85.0
    assert report["passed"] is True
    assert len(report["next_steps"]) == 3
    assert "<svg" in report["radar_chart_svg"]

    db_session.refresh(attempt)
    assert attempt.report_status == "PENDING_APPROVAL"

    # Mentor Approves Report
    from app.api.v1.mentor import approve_assessment_report
    app_res = approve_assessment_report(attempt.id, db=db_session, mentor=mentor)
    assert app_res["status"] == "APPROVED"

    db_session.refresh(attempt)
    assert attempt.report_status == "APPROVED"
    assert attempt.report_approved_at is not None


def test_gardener_rate_limiting() -> None:
    """Verify sliding-window rate limit caps user queries at 30/hour."""
    test_user_id = "user_rate_limit_test_001"

    for i in range(30):
        allowed, remaining = check_and_record_rate_limit(test_user_id)
        assert allowed is True
        assert remaining == 29 - i

    # 31st request should be rejected
    allowed, remaining = check_and_record_rate_limit(test_user_id)
    assert allowed is False
    assert remaining == 0
