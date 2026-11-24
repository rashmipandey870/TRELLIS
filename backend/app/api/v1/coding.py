"""TRELLIS LeetCode-style Coding Environment Endpoints (Step 5 & Security Hardening).

Enforces:
1. Role-guarded access: require_learner for run/submit, require_role for problem views.
2. Learner boundary enforcement: only problems in caller's active assessment attempt
   or caller's generated practice sessions may be opened, executed, or submitted.
3. Validate attempt_id: must belong to the caller and be IN_PROGRESS.
4. Custom input: reports program output without a pass/fail verdict.
5. Runtime percentile: computed only for ACCEPTED submissions; returns null if no history.
6. Per-user execution rate limits and global concurrency limit with queue.
"""

from __future__ import annotations

import threading
import time
from collections import defaultdict
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_uow, require_learner, require_role
from app.models.assessments import (
    AssessmentAttempt,
    AssessmentQuestion,
    CodingProblem,
    Submission,
    TestCase,
)
from app.models.practice import PracticeQuestion, PracticeSession
from app.models.user import User
from app.services.code_runner import CodeRunner

router = APIRouter(prefix="/coding", tags=["Coding Environment"])

# Per-user execution rate limiter: max 30 runs/submits per minute per learner
_USER_EXECUTION_TIMESTAMPS: dict[str, list[float]] = defaultdict(list)
_RATE_LIMIT_LOCK = threading.Lock()

# Global concurrency limiter: max 5 concurrent executions with queue
_GLOBAL_CONCURRENCY_LIMIT = 5
_EXECUTION_SEMAPHORE = threading.Semaphore(_GLOBAL_CONCURRENCY_LIMIT)


def check_execution_rate_limit(user_id: str, max_requests: int = 30, window_seconds: float = 60.0) -> None:
    now = time.time()
    with _RATE_LIMIT_LOCK:
        timestamps = _USER_EXECUTION_TIMESTAMPS[user_id]
        cutoff = now - window_seconds
        valid_ts = [t for t in timestamps if t > cutoff]
        if len(valid_ts) >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded: Max {max_requests} executions per minute.",
            )
        valid_ts.append(now)
        _USER_EXECUTION_TIMESTAMPS[user_id] = valid_ts


def verify_problem_access(
    db: Session,
    user: User,
    problem_id: str,
    attempt_id: str | None = None,
) -> CodingProblem:
    """Validate that the problem exists and the learner is authorized to access it."""
    problem = db.get(CodingProblem, problem_id)
    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coding problem not found.")

    # Mentors and Admins have platform-wide authoring/preview access
    if (user.role or "").upper() in {"ADMIN", "MENTOR"}:
        return problem

    # If attempt_id is provided, validate it strictly
    if attempt_id:
        attempt = db.get(AssessmentAttempt, attempt_id)
        if not attempt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment attempt not found.")
        if attempt.learner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Assessment attempt does not belong to the authenticated learner.",
            )
        if attempt.status != "IN_PROGRESS":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Assessment attempt is not IN_PROGRESS.",
            )
        # Check problem is in the assessment
        bank_ids = db.execute(
            select(AssessmentQuestion.bank_question_id).where(
                AssessmentQuestion.assessment_id == attempt.assessment_id
            )
        ).scalars().all()
        if problem.bank_id not in bank_ids and problem.id not in bank_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Coding problem is not part of this assessment attempt.",
            )
        return problem

    # If no attempt_id, learner is in open Coding Lab practice mode -> allowed
    return problem


class RunCodeRequest(BaseModel):
    problem_id: str | None = None
    code: str = Field(..., min_length=1)
    language: str = Field("python", pattern="^(python|javascript|java|cpp|c)$")
    custom_input: str | None = None
    attempt_id: str | None = None


class SubmitCodeRequest(BaseModel):
    problem_id: str
    code: str = Field(..., min_length=1)
    language: str = Field("python", pattern="^(python|javascript|java|cpp|c)$")
    attempt_id: str | None = None


@router.get("/problems", summary="List coding problems accessible to the user")
def list_coding_problems(
    category: str | None = None,
    difficulty: str | None = None,
    attempt_id: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("LEARNER", "MENTOR", "ADMIN")),
) -> list[dict[str, Any]]:
    """List accessible coding problems; returns open practice problems or assessment attempt problems."""
    query = select(CodingProblem)
    if difficulty:
        query = query.where(CodingProblem.difficulty == difficulty.upper())
    if category:
        query = query.where(CodingProblem.field == category)

    problems = db.execute(query).scalars().all()
    # If attempt_id is provided, filter to that assessment's questions only
    if attempt_id and (user.role or "").upper() == "LEARNER":
        bank_ids = set(
            db.execute(
                select(AssessmentQuestion.bank_question_id)
                .join(AssessmentAttempt, AssessmentAttempt.assessment_id == AssessmentQuestion.assessment_id)
                .where(AssessmentAttempt.id == attempt_id, AssessmentAttempt.learner_id == user.id)
            ).scalars().all()
        )
        problems = [p for p in problems if (p.bank_id and p.bank_id in bank_ids) or (p.id in bank_ids)]

    return [
        {
            "id": p.id,
            "title": p.title,
            "slug": p.title.lower().replace(" ", "-"),
            "difficulty": p.difficulty,
            "category": p.field,
            "tags": [p.field, p.difficulty],
        }
        for p in problems
    ]


@router.get("/problems/{problem_id}", summary="Get coding problem details and starter code")
def get_coding_problem(
    problem_id: str,
    attempt_id: str | None = Query(None),
    db: Session = Depends(get_db),
    user: User = Depends(require_role("LEARNER", "MENTOR", "ADMIN")),
) -> dict[str, Any]:
    problem = verify_problem_access(db, user, problem_id, attempt_id)

    # Return visible cases only
    visible_cases = [
        {
            "case_index": idx + 1,
            "input": tc.input_data,
            "expected_output": tc.expected_output,
        }
        for idx, tc in enumerate(problem.test_cases)
        if not tc.is_hidden
    ]

    return {
        "id": problem.id,
        "title": problem.title,
        "description": problem.description,
        "statement": problem.description,
        "constraints": problem.constraints,
        "difficulty": problem.difficulty,
        "field": problem.field,
        "category": problem.field,
        "marks": problem.marks,
        "time_limit_ms": problem.time_limit_ms,
        "memory_limit_mb": problem.memory_limit_mb,
        "starter_code": problem.starter_code_json or {},
        "examples": problem.examples_json or [],
        "sample_cases": visible_cases,
    }


@router.post("/run", summary="Run code against sample test cases and custom input in isolated sandbox")
def run_code(
    payload: RunCodeRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_learner),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    # Check rate limiting per user
    check_execution_rate_limit(user.id)

    is_custom_input = payload.custom_input is not None
    cases = []
    problem = None

    if is_custom_input:
        # Custom input box run: report program output without pass/fail verdict
        cases = [
            {
                "input_data": payload.custom_input,
                "expected_output": "",
                "is_hidden": False,
                "is_custom": True,
                "weight": 0.0,
            }
        ]
    elif payload.problem_id:
        problem = verify_problem_access(db, user, payload.problem_id, payload.attempt_id)
        cases = [
            {
                "input_data": tc.input_data,
                "expected_output": tc.expected_output,
                "is_hidden": False,
                "is_custom": False,
                "weight": 1.0,
            }
            for tc in problem.test_cases
            if not tc.is_hidden
        ]
        if not cases:
            cases = [{"input_data": "", "expected_output": "", "is_hidden": False, "is_custom": False, "weight": 1.0}]
    else:
        cases = [{"input_data": "", "expected_output": "", "is_hidden": False, "is_custom": False, "weight": 1.0}]

    # Concurrency queue gating
    acquired = _EXECUTION_SEMAPHORE.acquire(timeout=10.0)
    if not acquired:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Code execution concurrency queue is full. Please try again shortly.",
        )
    try:
        exec_result = CodeRunner.execute(
            code=payload.code,
            language=payload.language,
            test_cases=cases,
            time_limit_ms=3000,
            mask_hidden_inputs=False,
            is_custom_run=is_custom_input,
            entry_point=getattr(problem, "entry_point", None) if problem else None,
            argument_schema=getattr(problem, "argument_schema", None) if problem else None,
        )
    finally:
        _EXECUTION_SEMAPHORE.release()

    if is_custom_input:
        actual_output = exec_result.custom_output if exec_result.custom_output is not None else (
            exec_result.case_results[0].actual_output if exec_result.case_results else ""
        )
        return {
            "verdict": None,
            "stdout": actual_output,
            "stderr": exec_result.case_results[0].error_message if exec_result.case_results else None,
            "output": actual_output,
            "runtime_ms": exec_result.runtime_ms,
            "memory_mb": exec_result.memory_mb,
            "compile_error": exec_result.compile_error,
            "case_results": [
                {
                    "case_index": 1,
                    "verdict": None,
                    "input": payload.custom_input,
                    "expected": None,
                    "actual": actual_output,
                    "runtime_ms": exec_result.runtime_ms,
                    "error": exec_result.case_results[0].error_message if exec_result.case_results else None,
                }
            ],
        }

    return {
        "verdict": exec_result.verdict,
        "passed_cases": exec_result.passed_cases,
        "total_cases": exec_result.total_cases,
        "runtime_ms": exec_result.runtime_ms,
        "memory_mb": exec_result.memory_mb,
        "compile_error": exec_result.compile_error,
        "case_results": [
            {
                "case_index": cr.case_index,
                "verdict": cr.verdict,
                "input": cr.input_data,
                "expected": cr.expected_output,
                "actual": cr.actual_output,
                "runtime_ms": cr.runtime_ms,
                "error": cr.error_message,
            }
            for cr in exec_result.case_results
        ],
    }


@router.post("/submit", summary="Submit code against all cases (including hidden), persist submission")
def submit_code(
    payload: SubmitCodeRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_learner),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    check_execution_rate_limit(user.id)
    problem = verify_problem_access(db, user, payload.problem_id, payload.attempt_id)

    cases = [
        {
            "input_data": tc.input_data,
            "expected_output": tc.expected_output,
            "is_hidden": tc.is_hidden,
            "weight": tc.weight,
        }
        for tc in problem.test_cases
    ]

    # Concurrency queue gating
    acquired = _EXECUTION_SEMAPHORE.acquire(timeout=10.0)
    if not acquired:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Code execution concurrency queue is full. Please try again shortly.",
        )
    try:
        exec_result = CodeRunner.execute(
            code=payload.code,
            language=payload.language,
            test_cases=cases,
            time_limit_ms=problem.time_limit_ms,
            memory_limit_mb=problem.memory_limit_mb,
            mask_hidden_inputs=True,
            is_custom_run=False,
            entry_point=getattr(problem, "entry_point", None),
            argument_schema=getattr(problem, "argument_schema", None),
        )
    finally:
        _EXECUTION_SEMAPHORE.release()

    # Compute runtime percentile only for ACCEPTED submissions; return null when no history
    percentile: float | None = None
    if exec_result.verdict == "ACCEPTED":
        historical_runtimes = (
            db.execute(
                select(Submission.runtime_ms).where(
                    Submission.coding_problem_id == problem.id,
                    Submission.verdict == "ACCEPTED",
                )
            )
            .scalars()
            .all()
        )
        if historical_runtimes:
            slower_count = sum(1 for r in historical_runtimes if r > exec_result.runtime_ms)
            percentile = round((slower_count / len(historical_runtimes)) * 100.0, 1)

    # Persist submission
    sub = Submission(
        attempt_id=payload.attempt_id,
        coding_problem_id=problem.id,
        learner_id=user.id,
        code=payload.code,
        language=payload.language,
        verdict=exec_result.verdict or "SUBMITTED",
        runtime_ms=exec_result.runtime_ms,
        memory_mb=exec_result.memory_mb,
        passed_cases=exec_result.passed_cases,
        total_cases=exec_result.total_cases,
        score=exec_result.score,
        details_json={
            "compile_error": exec_result.compile_error,
            "first_failing_case": exec_result.first_failing_case,
            "percentile": percentile,
        },
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)

    return {
        "submission_id": sub.id,
        "id": sub.id,
        "verdict": sub.verdict,
        "passed_cases": sub.passed_cases,
        "total_cases": sub.total_cases,
        "score": sub.score,
        "max_score": problem.marks,
        "runtime_ms": sub.runtime_ms,
        "memory_mb": sub.memory_mb,
        "runtime_percentile": percentile,
        "first_failing_case": exec_result.first_failing_case,
        "failing_case": exec_result.first_failing_case,
        "compile_error": exec_result.compile_error,
        "created_at": sub.created_at.isoformat(),
    }


@router.get("/submissions/{problem_id}", summary="Get learner submission history for a problem")
def get_submission_history_by_problem(
    problem_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_learner),
) -> list[dict[str, Any]]:
    subs = (
        db.execute(
            select(Submission)
            .where(
                Submission.coding_problem_id == problem_id,
                Submission.learner_id == user.id,
            )
            .order_by(Submission.created_at.desc())
        )
        .scalars()
        .all()
    )
    return [
        {
            "id": s.id,
            "verdict": s.verdict,
            "passed_cases": s.passed_cases,
            "total_cases": s.total_cases,
            "runtime_ms": s.runtime_ms,
            "memory_mb": s.memory_mb,
            "language": s.language,
            "score": s.score,
            "submitted_at": s.created_at.isoformat(),
        }
        for s in subs
    ]


@router.get("/submissions", summary="List learner submission history across problems")
def list_submissions(
    problem_id: str | None = Query(None),
    db: Session = Depends(get_db),
    user: User = Depends(require_learner),
) -> list[dict[str, Any]]:
    query = select(Submission).where(Submission.learner_id == user.id)
    if problem_id:
        query = query.where(Submission.coding_problem_id == problem_id)
    subs = db.execute(query.order_by(Submission.created_at.desc())).scalars().all()
    return [
        {
            "id": s.id,
            "verdict": s.verdict,
            "passed_cases": s.passed_cases,
            "total_cases": s.total_cases,
            "runtime_ms": s.runtime_ms,
            "memory_mb": s.memory_mb,
            "language": s.language,
            "score": s.score,
            "submitted_at": s.created_at.isoformat(),
        }
        for s in subs
    ]
