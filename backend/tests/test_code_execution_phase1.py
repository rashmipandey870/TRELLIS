"""TRELLIS Phase 1 Code Execution Security & Isolation Tests.

Validates:
1. Process Environment Isolation: Code executing in LocalSubprocessRunner has empty os.environ.
2. No Simulated Acceptance: A do-nothing Java program is NOT accepted.
3. Compiler/Runner Unavailability: Missing compiler or unreachable runner returns RUNNER_UNAVAILABLE.
4. Attempt Ownership Authorization: A learner cannot submit code to someone else's assessment attempt.
5. Custom Input Run: Reports output without a pass/fail verdict.
6. Runtime Percentile: Computed only for ACCEPTED submissions; returns None when no history.
7. Production Safety: Refuses to start outside dev if no isolated runner (Judge0 or Docker) is configured.
8. Output Normalization: Correctly matches outputs ignoring trailing whitespace per line.
"""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest
from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api.v1.coding import (
    RunCodeRequest,
    SubmitCodeRequest,
    run_code,
    submit_code,
    verify_problem_access,
)
from app.core.config import Settings, settings
from app.models import (
    Assessment,
    AssessmentAttempt,
    AssessmentQuestion,
    Base,
    CodingProblem,
    Organisation,
    QuestionBank,
    Submission,
    TestCase,
    User,
)
from app.services.code_runner import (
    CodeRunner,
    Judge0Runner,
    LocalSubprocessRunner,
    normalize_output,
)


@pytest.fixture
def p1_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session = Session(engine)
    try:
        org = Organisation(name="CSM Technology", code="CSM_TEST")
        session.add(org)
        session.flush()

        mentor = User(
            org_id=org.id,
            email="mentor.phase1@csm.tech",
            password_hash="hashed_pw",
            full_name="Mentor Phase1",
            role="MENTOR",
            is_active=True,
        )
        learner1 = User(
            org_id=org.id,
            email="learner1.phase1@csm.tech",
            password_hash="hashed_pw",
            full_name="Learner One",
            role="LEARNER",
            is_active=True,
        )
        learner2 = User(
            org_id=org.id,
            email="learner2.phase1@csm.tech",
            password_hash="hashed_pw",
            full_name="Learner Two",
            role="LEARNER",
            is_active=True,
        )
        session.add_all([mentor, learner1, learner2])
        session.flush()

        # Bank Question & Coding Problem
        qb = QuestionBank(
            author_id=mentor.id,
            title="Two Sum Problem",
            question_text="Add two numbers",
            question_type="CODING",
            field="Python",
            topic="Basics",
            difficulty="EASY",
        )
        session.add(qb)
        session.flush()

        cp = CodingProblem(
            bank_id=qb.id,
            title="Two Sum Problem",
            description="Given two numbers, output their sum.",
            difficulty="EASY",
            field="Python",
            marks=10.0,
            time_limit_ms=2000,
            memory_limit_mb=256,
        )
        session.add(cp)
        session.flush()

        tc1 = TestCase(
            problem_id=cp.id,
            input_data="3 5",
            expected_output="8",
            is_hidden=False,
            weight=1.0,
        )
        tc2 = TestCase(
            problem_id=cp.id,
            input_data="10 20",
            expected_output="30",
            is_hidden=True,
            weight=1.0,
        )
        session.add_all([tc1, tc2])
        session.flush()

        # Assessment and Attempt for Learner 1
        asm = Assessment(
            mentor_id=mentor.id,
            title="Python Assessment",
            field="Python",
            status="PUBLISHED",
        )
        session.add(asm)
        session.flush()

        aq = AssessmentQuestion(
            assessment_id=asm.id,
            bank_question_id=qb.id,
            sequence_order=1,
            marks=10.0,
        )
        session.add(aq)
        session.flush()

        att1 = AssessmentAttempt(
            assessment_id=asm.id,
            learner_id=learner1.id,
            status="IN_PROGRESS",
        )
        session.add(att1)
        session.commit()

        yield session, learner1, learner2, cp, att1
    finally:
        session.close()


def test_submission_that_prints_environ_finds_nothing():
    """Security test: Subprocess runner runs with empty environment env={}."""
    code = """import os, sys
env_keys = [k for k in os.environ.keys() if not k.startswith('_')]
print(len(env_keys))
"""
    test_cases = [
        {"input_data": "", "expected_output": "0", "weight": 1.0}
    ]
    res = CodeRunner.execute(code=code, language="python", test_cases=test_cases)
    assert res.verdict == "ACCEPTED"
    assert res.passed_cases == 1
    # Check actual output printed was 0
    assert res.case_results[0].actual_output.strip() == "0"


def test_do_nothing_java_program_is_not_accepted():
    """No simulated execution: A do-nothing Java program MUST NOT be accepted."""
    code = """public class Solution {
    public static void main(String[] args) {
        // Do nothing
    }
}"""
    test_cases = [
        {"input_data": "42", "expected_output": "42", "weight": 1.0}
    ]
    res = CodeRunner.execute(code=code, language="java", test_cases=test_cases)
    # It must either fail due to WRONG_ANSWER (empty output != '42') or RUNNER_UNAVAILABLE if javac is missing
    # Under no circumstances may it return ACCEPTED!
    assert res.verdict != "ACCEPTED"
    assert res.verdict in {"WRONG_ANSWER", "RUNNER_UNAVAILABLE", "COMPILATION_ERROR"}


def test_runner_unavailable_returns_error():
    """When a remote runner (Judge0) is unreachable, it returns RUNNER_UNAVAILABLE."""
    runner = Judge0Runner(base_url="http://127.0.0.1:59999", api_key="invalid")
    res = runner.execute(
        code="print(1)",
        language="python",
        test_cases=[{"input_data": "", "expected_output": "1", "weight": 1.0}],
    )
    assert res.verdict == "RUNNER_UNAVAILABLE"
    assert "unavailable" in (res.compile_error or "").lower()
    assert res.passed_cases == 0


def test_learner_cannot_submit_to_someone_elses_attempt(p1_db):
    """Access boundary test: Learner 2 cannot submit code to Learner 1's attempt."""
    session, learner1, learner2, problem, attempt1 = p1_db

    # Learner 2 tries to submit to Learner 1's attempt
    payload = SubmitCodeRequest(
        problem_id=problem.id,
        code="print('hello')",
        language="python",
        attempt_id=attempt1.id,
    )

    with pytest.raises(HTTPException) as exc_info:
        submit_code(
            payload=payload,
            db=session,
            user=learner2,
            _uow=None,
        )
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert "does not belong" in exc_info.value.detail


def test_custom_input_run_reports_output_without_verdict(p1_db):
    """Custom input execution reports standard output without pass/fail grading."""
    session, learner1, learner2, problem, attempt1 = p1_db

    payload = RunCodeRequest(
        problem_id=problem.id,
        code="import sys\nval = sys.stdin.read().strip()\nprint(f'ECHO: {val}')",
        language="python",
        custom_input="trellis test input",
        attempt_id=attempt1.id,
    )

    result = run_code(
        payload=payload,
        db=session,
        user=learner1,
        _uow=None,
    )

    # Must NOT have pass/fail verdict
    assert result.get("verdict") is None
    assert "ECHO: trellis test input" in result.get("output", "")
    assert "ECHO: trellis test input" in result.get("stdout", "")


def test_runtime_percentile_computation_and_null_on_no_history(p1_db):
    """Runtime percentile: Computed only for ACCEPTED, null when no historical submissions."""
    session, learner1, learner2, problem, attempt1 = p1_db

    # Submit correct solution
    payload = SubmitCodeRequest(
        problem_id=problem.id,
        code="import sys\nnums = sys.stdin.read().split()\nif nums: print(int(nums[0]) + int(nums[1]))",
        language="python",
        attempt_id=attempt1.id,
    )

    res = submit_code(
        payload=payload,
        db=session,
        user=learner1,
        _uow=None,
    )

    assert res["verdict"] == "ACCEPTED"
    # First submission: no prior historical submissions exist, so runtime_percentile must be None
    assert res["runtime_percentile"] is None


def test_production_safety_refuses_local_runner(tmp_path):
    """Settings refuse to start in production if CODE_RUNNER is local."""
    priv_file = tmp_path / "jwt_private.pem"
    pub_file = tmp_path / "jwt_public.pem"
    priv_file.write_text("dummy_priv_key")
    pub_file.write_text("dummy_pub_key")

    with pytest.raises(RuntimeError) as exc_info:
        Settings(
            TRELLIS_ENV="production",
            DATABASE_URL="sqlite:///test.db",
            DATABASE_MIGRATION_URL="sqlite:///test.db",
            JWT_PRIVATE_KEY_PATH=str(priv_file),
            JWT_PUBLIC_KEY_PATH=str(pub_file),
            FIELD_ENCRYPTION_KEY="prod-fernet-key-32bytes-base64=",
            CODE_RUNNER="local",
        )
    assert "CODE_RUNNER must be 'judge0' or 'docker'" in str(exc_info.value)


def test_output_normalization_trims_trailing_whitespace():
    """Verify output normalization trims trailing spaces per line."""
    out1 = "line 1   \nline 2\t  \nline 3   \n"
    out2 = "line 1\nline 2\nline 3"
    assert normalize_output(out1) == normalize_output(out2)
