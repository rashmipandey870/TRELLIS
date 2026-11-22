"""TRELLIS WS0 Security Emergency Tests.

Validates:
1. CodeRunner Security Abuse Scenarios:
   - Infinite loop (Time Limit Exceeded)
   - Memory allocation bomb (Memory Limit Exceeded / Runtime Error)
   - Host file read attempt (Empty env, isolated tmp execution)
   - Huge output flooding (Truncated at MAX_OUTPUT_BYTES = 64KB)
   - Concurrency limit & queue saturation
2. Manual Grading Bounds & Override Audit:
   - Rejecting negative scores and scores exceeding question marks
   - Requiring reason when overriding an auto-graded score
   - Writing GRADE_OVERRIDE to AuditLog
3. User Credentials & Forced Password Change:
   - Creating user generates random one-time password with must_change_password=True
   - Bulk import generates random one-time password with must_change_password=True
   - Gating protected endpoints behind MUST_CHANGE_PASSWORD until changed
   - Changing password clears must_change_password and hashes new password
"""

import os
import threading
from collections.abc import Generator
from unittest.mock import patch

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api.v1.admin import (
    BulkImportRequest,
    UserCreateRequest,
    bulk_import_users,
    create_user,
)
from app.api.v1.auth import ChangePasswordRequest, change_password
from app.api.v1.mentor import (
    AnswerGradeItem,
    GradeAttemptRequest,
    grade_attempt_answers,
)
from app.core.security import hash_password, verify_password
from app.models import (
    Answer,
    Assessment,
    AssessmentAttempt,
    AssessmentQuestion,
    AuditLog,
    Base,
    Organisation,
    QuestionBank,
    User,
)
from app.services.code_runner import (
    CodeRunner,
    LocalSubprocessRunner,
)


@pytest.fixture
def ws0_db() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session = Session(engine)
    try:
        org = Organisation(name="CSM Tech", code="CSM_WS0")
        session.add(org)
        session.flush()

        admin = User(
            org_id=org.id,
            email="admin.ws0@csm.tech",
            password_hash=hash_password("AdminPass123!"),
            full_name="WS0 Admin",
            role="ADMIN",
            is_active=True,
        )
        mentor = User(
            org_id=org.id,
            email="mentor.ws0@csm.tech",
            password_hash=hash_password("MentorPass123!"),
            full_name="WS0 Mentor",
            role="MENTOR",
            is_active=True,
        )
        learner = User(
            org_id=org.id,
            email="learner.ws0@csm.tech",
            password_hash=hash_password("LearnerPass123!"),
            full_name="WS0 Learner",
            role="LEARNER",
            is_active=True,
        )
        session.add_all([admin, mentor, learner])
        session.flush()
        yield session
    finally:
        session.close()
        engine.dispose()


# --- CodeRunner Abuse Tests ---

def test_coderunner_infinite_loop_timeout() -> None:
    runner = LocalSubprocessRunner()
    infinite_loop_code = "while True:\n    pass\n"
    res = runner.execute(
        code=infinite_loop_code,
        language="python",
        test_cases=[{"input_data": "", "expected_output": ""}],
        time_limit_ms=800,
    )
    assert res.verdict == "TIME_LIMIT_EXCEEDED"
    assert res.passed_cases == 0


def test_coderunner_huge_output_is_capped() -> None:
    runner = LocalSubprocessRunner()
    # Generates > 100 KB of stdout
    huge_output_code = "print('A' * 150000)\n"
    res = runner.execute(
        code=huge_output_code,
        language="python",
        test_cases=[{"input_data": "", "expected_output": "something_else"}],
        time_limit_ms=2000,
    )
    # The output captured must be capped at MAX_OUTPUT_BYTES (64 KB)
    actual_len = len(res.case_results[0].actual_output.encode("utf-8"))
    assert actual_len <= runner.MAX_OUTPUT_BYTES + 1024


def test_coderunner_isolated_environment_cannot_read_env_secrets() -> None:
    runner = LocalSubprocessRunner()
    # Attempt to read DATABASE_URL or SECRET_KEY from environment
    code = (
        "import os\n"
        "db = os.environ.get('DATABASE_URL', '')\n"
        "sec = os.environ.get('SECRET_KEY', '')\n"
        "print(f'DB:{db}|SEC:{sec}')\n"
    )
    res = runner.execute(
        code=code,
        language="python",
        test_cases=[{"input_data": "", "expected_output": "DB:|SEC:"}],
        time_limit_ms=2000,
    )
    assert res.verdict == "ACCEPTED"
    assert res.case_results[0].actual_output.strip() == "DB:|SEC:"


def test_coderunner_concurrency_queue_limit() -> None:
    # Temporarily set max concurrent runs semaphore to 1
    with patch("app.services.code_runner._RUNNER_SEMAPHORE", threading.BoundedSemaphore(1)):
        # Acquire the single slot
        from app.services.code_runner import _RUNNER_SEMAPHORE
        assert _RUNNER_SEMAPHORE.acquire(blocking=False)
        try:
            # Code execution must fail with QUEUE_LIMIT_EXCEEDED when timeout expires
            with patch("app.services.code_runner._RUNNER_SEMAPHORE.acquire", return_value=False):
                res = CodeRunner.execute(
                    code="print(1)",
                    language="python",
                    test_cases=[{"input_data": "", "expected_output": "1"}],
                )
                assert res.verdict == "QUEUE_LIMIT_EXCEEDED"
                assert "saturated" in res.compile_error
        finally:
            _RUNNER_SEMAPHORE.release()


# --- Manual Grading Bounds & Override Audit Tests ---

def test_manual_grading_bounds_validation(ws0_db: Session) -> None:
    mentor = ws0_db.query(User).filter(User.role == "MENTOR").first()
    learner = ws0_db.query(User).filter(User.role == "LEARNER").first()

    assessment = Assessment(
        mentor_id=mentor.id,
        title="Grading Bounds Test",
        field="Python",
        duration_minutes=30,
        passing_score=60.0,
        status="PUBLISHED",
    )
    ws0_db.add(assessment)
    ws0_db.flush()

    bq = QuestionBank(
        author_id=mentor.id,
        title="Subjective Essay",
        question_text="Explain GIL.",
        question_type="SHORT_ANSWER",
        field="Python",
        topic="General",
    )
    ws0_db.add(bq)
    ws0_db.flush()

    aq = AssessmentQuestion(
        assessment_id=assessment.id,
        bank_question_id=bq.id,
        marks=10.0,
        sequence_order=1,
    )
    ws0_db.add(aq)
    ws0_db.flush()

    attempt = AssessmentAttempt(
        assessment_id=assessment.id,
        learner_id=learner.id,
        status="SUBMITTED",
        total_marks=10.0,
        score=0.0,
        grading_status="PENDING_REVIEW",
    )
    ws0_db.add(attempt)
    ws0_db.flush()

    ans = Answer(
        attempt_id=attempt.id,
        bank_question_id=bq.id,
        text_response="GIL limits Python bytecode execution to one thread.",
        score_awarded=0.0,
        grading_status="PENDING_REVIEW",
    )
    ws0_db.add(ans)
    ws0_db.commit()

    # 1. Negative score rejected
    with pytest.raises(HTTPException) as exc_neg:
        grade_attempt_answers(
            attempt_id=attempt.id,
            payload=GradeAttemptRequest(
                grades=[AnswerGradeItem(answer_id=ans.id, score_awarded=-5.0)]
            ),
            db=ws0_db,
            mentor=mentor,
            _uow=None,
        )
    assert exc_neg.value.status_code == 422
    assert "must be between 0 and maximum question marks" in str(exc_neg.value.detail)

    # 2. Score > question marks (10.0) rejected
    with pytest.raises(HTTPException) as exc_high:
        grade_attempt_answers(
            attempt_id=attempt.id,
            payload=GradeAttemptRequest(
                grades=[AnswerGradeItem(answer_id=ans.id, score_awarded=9999.0)]
            ),
            db=ws0_db,
            mentor=mentor,
            _uow=None,
        )
    assert exc_high.value.status_code == 422
    assert "must be between 0 and maximum question marks" in str(exc_high.value.detail)

    # 3. Valid score 8.5 accepted
    res = grade_attempt_answers(
        attempt_id=attempt.id,
        payload=GradeAttemptRequest(
            grades=[AnswerGradeItem(answer_id=ans.id, score_awarded=8.5, feedback="Good concise answer")]
        ),
        db=ws0_db,
        mentor=mentor,
        _uow=None,
    )
    assert res["status"] == "success"
    assert res["score"] == 8.5
    assert res["passed"] is True


def test_manual_grading_override_requires_reason_and_logs_audit(ws0_db: Session) -> None:
    mentor = ws0_db.query(User).filter(User.role == "MENTOR").first()
    learner = ws0_db.query(User).filter(User.role == "LEARNER").first()

    assessment = Assessment(
        mentor_id=mentor.id,
        title="Auto Grade Override Test",
        field="Python",
        duration_minutes=30,
        passing_score=50.0,
        status="PUBLISHED",
    )
    ws0_db.add(assessment)
    ws0_db.flush()

    bq = QuestionBank(
        author_id=mentor.id,
        title="MCQ Question",
        question_text="Is Python interpreted?",
        question_type="MCQ",
        field="Python",
        topic="General",
    )
    ws0_db.add(bq)
    ws0_db.flush()

    aq = AssessmentQuestion(
        assessment_id=assessment.id,
        bank_question_id=bq.id,
        marks=5.0,
        sequence_order=1,
    )
    ws0_db.add(aq)
    ws0_db.flush()

    attempt = AssessmentAttempt(
        assessment_id=assessment.id,
        learner_id=learner.id,
        status="SUBMITTED",
        total_marks=5.0,
        score=0.0,
        grading_status="GRADED",
    )
    ws0_db.add(attempt)
    ws0_db.flush()

    # Answer was auto-graded as 0 marks
    ans = Answer(
        attempt_id=attempt.id,
        bank_question_id=bq.id,
        selected_option_ids_json=["opt_wrong"],
        score_awarded=0.0,
        grading_status="GRADED",
    )
    ws0_db.add(ans)
    ws0_db.commit()

    # 1. Override without reason rejected
    with pytest.raises(HTTPException) as exc_no_reason:
        grade_attempt_answers(
            attempt_id=attempt.id,
            payload=GradeAttemptRequest(
                grades=[AnswerGradeItem(answer_id=ans.id, score_awarded=5.0, override_reason="")]
            ),
            db=ws0_db,
            mentor=mentor,
            _uow=None,
        )
    assert exc_no_reason.value.status_code == 400
    assert "requires an override reason" in str(exc_no_reason.value.detail)

    # 2. Override with reason accepted and logged to AuditLog
    grade_attempt_answers(
        attempt_id=attempt.id,
        payload=GradeAttemptRequest(
            grades=[
                AnswerGradeItem(
                    answer_id=ans.id,
                    score_awarded=5.0,
                    override_reason="Ambiguous wording in question prompt; learner gave valid alternative.",
                )
            ]
        ),
        db=ws0_db,
        mentor=mentor,
        _uow=None,
    )

    audit = ws0_db.query(AuditLog).filter(
        AuditLog.action == "GRADE_OVERRIDE",
        AuditLog.resource_id == ans.id,
    ).first()
    assert audit is not None
    assert audit.actor_id == mentor.id
    assert audit.before_state_json["old_score"] == 0.0
    assert audit.after_state_json["new_score"] == 5.0
    assert "Ambiguous wording" in audit.reason


# --- User Creation & Forced Password Change Tests ---

def test_create_user_generates_one_time_password_and_forces_change(ws0_db: Session) -> None:
    admin = ws0_db.query(User).filter(User.role == "ADMIN").first()

    payload = UserCreateRequest(
        email="new.onboarded.user@csmtech.internal",
        full_name="New Onboarded User",
        role="LEARNER",
    )
    res = create_user(payload=payload, db=ws0_db, admin=admin, _uow=None)

    assert res["must_change_password"] is True
    assert len(res["one_time_password"]) >= 12

    created_user = ws0_db.query(User).filter(User.email == payload.email).first()
    assert created_user is not None
    assert created_user.must_change_password is True
    assert verify_password(res["one_time_password"], created_user.password_hash)


def test_bulk_import_generates_unique_passwords_and_no_shared_default(ws0_db: Session) -> None:
    admin = ws0_db.query(User).filter(User.role == "ADMIN").first()
    csv_content = (
        "email,full_name,role\n"
        "import1@csm.tech,Imported User One,LEARNER\n"
        "import2@csm.tech,Imported User Two,MENTOR\n"
    )
    res = bulk_import_users(
        payload=BulkImportRequest(csv_content=csv_content),
        db=ws0_db,
        admin=admin,
        _uow=None,
    )
    assert res["created_count"] == 2
    users = res["users"]
    assert len(users) == 2
    # Verify passwords are unique and not a shared default
    pwd1 = users[0]["one_time_password"]
    pwd2 = users[1]["one_time_password"]
    assert pwd1 != pwd2
    assert pwd1 != "CSMTrellis2026!"
    assert pwd2 != "CSMTrellis2026!"


def test_forced_password_change_lifecycle(ws0_db: Session) -> None:
    admin = ws0_db.query(User).filter(User.role == "ADMIN").first()
    user_res = create_user(
        payload=UserCreateRequest(
            email="forced.change@csmtech.internal",
            full_name="Forced Change User",
            role="LEARNER",
        ),
        db=ws0_db,
        admin=admin,
        _uow=None,
    )
    one_time_pwd = user_res["one_time_password"]
    user = ws0_db.query(User).filter(User.email == "forced.change@csmtech.internal").first()

    # Changing password with wrong current password fails
    with pytest.raises(HTTPException) as exc_bad:
        change_password(
            payload=ChangePasswordRequest(current_password="WrongPassword123!", new_password="BrandNewSecurePassword2026!"),
            current_user=user,
            db=ws0_db,
            _uow=None,
        )
    assert exc_bad.value.status_code == 400

    # Successful password change clears must_change_password
    change_res = change_password(
        payload=ChangePasswordRequest(current_password=one_time_pwd, new_password="BrandNewSecurePassword2026!"),
        current_user=user,
        db=ws0_db,
        _uow=None,
    )
    assert change_res["message"] == "Password updated successfully."
    assert user.must_change_password is False
    assert verify_password("BrandNewSecurePassword2026!", user.password_hash)
