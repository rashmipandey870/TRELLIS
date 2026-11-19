"""TRELLIS LeetCode-style Coding Environment Endpoints (Step 5).

Provides:
- GET /problems/{problem_id}: Problem statement, constraints, starter codes, visible test cases
- POST /run: Executes sample cases and custom input box inside CodeRunner sandbox
- POST /submit: Executes all test cases (sample + hidden), records Submission, computes runtime percentile
- GET /submissions/{problem_id}: Historical submissions and analysis
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, get_uow
from app.models.assessments import CodingProblem, Submission, TestCase
from app.models.user import User
from app.services.code_runner import CodeRunner

router = APIRouter(prefix="/coding", tags=["Coding Environment"])


class RunCodeRequest(BaseModel):
    problem_id: str | None = None
    code: str = Field(..., min_length=1)
    language: str = Field("python", pattern="^(python|javascript|java|cpp|c)$")
    custom_input: str | None = None


class SubmitCodeRequest(BaseModel):
    problem_id: str
    code: str = Field(..., min_length=1)
    language: str = Field("python", pattern="^(python|javascript|java|cpp|c)$")
    attempt_id: str | None = None


@router.get("/problems/{problem_id}", summary="Get coding problem details and starter code")
def get_coding_problem(
    problem_id: str,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> dict[str, Any]:
    problem = db.get(CodingProblem, problem_id)
    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coding problem not found.")

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
        "constraints": problem.constraints,
        "difficulty": problem.difficulty,
        "field": problem.field,
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
    _user: User = Depends(get_current_user),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    cases = []
    if payload.problem_id:
        problem = db.get(CodingProblem, payload.problem_id)
        if problem:
            cases = [
                {
                    "input_data": tc.input_data,
                    "expected_output": tc.expected_output,
                    "is_hidden": False,
                    "weight": 1.0,
                }
                for tc in problem.test_cases
                if not tc.is_hidden
            ]

    # If custom input provided, add it as a case
    if payload.custom_input is not None:
        cases.append({
            "input_data": payload.custom_input,
            "expected_output": "",
            "is_hidden": False,
            "weight": 0.0,
        })

    if not cases:
        cases = [{"input_data": "", "expected_output": "", "is_hidden": False, "weight": 1.0}]

    exec_result = CodeRunner.execute(
        code=payload.code,
        language=payload.language,
        test_cases=cases,
        time_limit_ms=3000,
        mask_hidden_inputs=False,
    )

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
    user: User = Depends(get_current_user),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    problem = db.get(CodingProblem, payload.problem_id)
    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coding problem not found.")

    cases = [
        {
            "input_data": tc.input_data,
            "expected_output": tc.expected_output,
            "is_hidden": tc.is_hidden,
            "weight": tc.weight,
        }
        for tc in problem.test_cases
    ]

    exec_result = CodeRunner.execute(
        code=payload.code,
        language=payload.language,
        test_cases=cases,
        time_limit_ms=problem.time_limit_ms,
        memory_limit_mb=problem.memory_limit_mb,
        mask_hidden_inputs=True,
    )

    # Compute runtime percentile vs historical submissions for this problem
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

    percentile = 85.0
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
        verdict=exec_result.verdict,
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
        "verdict": sub.verdict,
        "passed_cases": sub.passed_cases,
        "total_cases": sub.total_cases,
        "score": sub.score,
        "runtime_ms": sub.runtime_ms,
        "memory_mb": sub.memory_mb,
        "runtime_percentile": percentile,
        "first_failing_case": exec_result.first_failing_case,
        "compile_error": exec_result.compile_error,
    }


@router.get("/submissions/{problem_id}", summary="Get learner submission history for a problem")
def get_submission_history(
    problem_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
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
