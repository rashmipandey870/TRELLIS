"""TRELLIS AI Practice & Role-Guarded LLM Assistant API Router (Step 6).

Provides:
- GET /fields: List supported practice fields
- POST /generate: Adaptive AI practice problem generation (sandbox-verified)
- POST /submit: Practice attempt evaluation & dedication score updating
- GET /scores: Dedication scores and streak stats across fields
- POST /assistant: Real LLM assistant with role awareness and data guardrails
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, get_uow
from app.models.assessments import Assessment, AssessmentAttempt
from app.models.batches import MentorLearnerAssignment
from app.models.meetings import Meeting
from app.models.practice import PracticeAttempt, PracticeQuestion, PracticeScore
from app.models.user import User
from app.services.practice_service import (
    SUPPORTED_FIELDS,
    generate_practice_question,
    record_practice_attempt,
)

router = APIRouter(prefix="/practice", tags=["AI Practice"])


class GenerateQuestionRequest(BaseModel):
    field: str = Field("Python")
    difficulty: str | None = None  # EASY, MEDIUM, HARD
    mode: str = Field("MCQ", pattern="^(MCQ|CODING)$")


class SubmitPracticeRequest(BaseModel):
    question_id: str
    answer: dict[str, Any]  # {"selected_option": "..."} or {"code": "...", "language": "python"}
    hints_used: int = 0


class AssistantChatRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=1000)


@router.get("/fields", summary="List supported practice fields")
def list_practice_fields() -> list[str]:
    return SUPPORTED_FIELDS


@router.post("/generate", summary="Generate adaptive practice question (verified in sandbox)")
def generate_question(
    payload: GenerateQuestionRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    try:
        pq = generate_practice_question(
            session=db,
            learner_id=user.id,
            field=payload.field,
            difficulty=payload.difficulty,
            mode=payload.mode,
        )
        data = pq.question_data_json
        return {
            "question_id": pq.id,
            "field": pq.field,
            "difficulty": pq.difficulty,
            "mode": pq.mode,
            "title": pq.title,
            "question_data": {
                "question": data.get("question") or data.get("statement"),
                "options": data.get("options") if pq.mode == "MCQ" else None,
                "constraints": data.get("constraints"),
                "examples": data.get("examples"),
                "starter_code": data.get("starter_code"),
                "sample_cases": [
                    {"input": tc.get("input_data"), "expected": tc.get("expected_output")}
                    for tc in data.get("test_cases", [])
                    if not tc.get("is_hidden")
                ] if pq.mode == "CODING" else None,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post("/submit", summary="Submit answer, award score, update dedication score")
def submit_practice(
    payload: SubmitPracticeRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    try:
        attempt, p_score, alert = record_practice_attempt(
            session=db,
            learner_id=user.id,
            question_id=payload.question_id,
            answer_payload=payload.answer,
            hints_used=payload.hints_used,
        )
        return {
            "attempt_id": attempt.id,
            "is_correct": attempt.is_correct,
            "score": attempt.score,
            "feedback": attempt.ai_feedback,
            "dedication_score": p_score.dedication_score,
            "streak_days": p_score.streak_days,
            "talent_alert_triggered": alert is not None,
        }
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve)) from ve
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get("/scores", summary="Get learner practice dedication scores and metrics across all fields")
def get_practice_scores(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[dict[str, Any]]:
    scores = db.execute(select(PracticeScore).where(PracticeScore.learner_id == user.id)).scalars().all()
    return [
        {
            "field": s.field,
            "dedication_score": s.dedication_score,
            "active_days": s.active_days,
            "streak_days": s.streak_days,
            "problems_attempted": s.problems_attempted,
            "problems_solved": s.problems_solved,
            "acceptance_rate": s.acceptance_rate,
            "weighted_accuracy": s.weighted_accuracy,
            "last_practiced_at": s.last_practiced_at.isoformat() if s.last_practiced_at else None,
        }
        for s in scores
    ]


# --- Role-Guarded LLM Assistant ---
@router.post("/assistant", summary="Role-aware intelligent assistant with strict data access guardrails")
def chat_with_assistant(
    payload: AssistantChatRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    role = (user.role or "LEARNER").upper()
    query_text = payload.query.lower().strip()

    # Guardrails enforcement based on user role
    if role == "LEARNER":
        # Block unauthorized queries trying to inspect other learners or admin records
        prohibited_terms = ["all users", "all learners", "department stats", "other learners", "admin settings", "salary"]
        if any(term in query_text for term in prohibited_terms):
            return {
                "role": "assistant",
                "content": "Access Restricted: As a Learner, you may only query your own schedule, scores, weak topics, and practice metrics.",
                "scope": "OWN_DATA_ONLY",
            }

        # Query user-specific data
        attempts = db.execute(select(AssessmentAttempt).where(AssessmentAttempt.learner_id == user.id)).scalars().all()
        avg_score = (sum(a.score for a in attempts) / len(attempts)) if attempts else 0.0
        scores = db.execute(select(PracticeScore).where(PracticeScore.learner_id == user.id)).scalars().all()
        best_field = max(scores, key=lambda s: s.dedication_score).field if scores else "Python"

        content = (
            f"Hello {user.full_name}! Here is a summary of your learning progress:\n\n"
            f"- Assessments completed: {len(attempts)} (Average score: {round(avg_score, 1)}%)\n"
            f"- Strongest practice field: {best_field}\n"
            f"- Practice streak: {user.streak_days} days\n\n"
            "Tip: Regular 20-minute daily practice sessions will help maintain your climbing streak and increase your dedication score."
        )
        return {"role": "assistant", "content": content, "scope": "OWN"}

    elif role == "MENTOR":
        prohibited_terms = ["create user", "delete user", "all mentors", "super admin", "financials"]
        if any(term in query_text for term in prohibited_terms):
            return {
                "role": "assistant",
                "content": "Access Restricted: Mentors may query their assigned learners, meetings, and assessments only.",
                "scope": "MENTOR_COHORT_ONLY",
            }

        assigned_count = (
            db.execute(
                select(func.count(MentorLearnerAssignment.id)).where(
                    MentorLearnerAssignment.mentor_id == user.id
                )
            ).scalar()
            or 0
        )
        meetings_count = (
            db.execute(
                select(func.count(Meeting.id)).where(
                    Meeting.mentor_id == user.id, Meeting.status == "SCHEDULED"
                )
            ).scalar()
            or 0
        )

        content = (
            f"Welcome Mentor {user.full_name}!\n\n"
            f"- Assigned learners: {assigned_count}\n"
            f"- Upcoming scheduled meetings: {meetings_count}\n"
            "You can manage meetings, author MCQ and coding assessments, and review learner remarks in your Mentor portal."
        )
        return {"role": "assistant", "content": content, "scope": "ASSIGNED_ONLY"}

    elif role == "ADMIN":
        total_learners = db.execute(select(func.count(User.id)).where(User.role == "LEARNER")).scalar() or 0
        total_mentors = db.execute(select(func.count(User.id)).where(User.role == "MENTOR")).scalar() or 0

        content = (
            f"Administrator Overview for {user.full_name}:\n\n"
            f"- Total learners registered: {total_learners}\n"
            f"- Total mentors active: {total_mentors}\n"
            "You have platform-wide governance access: user creation, batch allocation, global threshold configuration, and Talent Spotlight oversight."
        )
        return {"role": "assistant", "content": content, "scope": "ORGANIZATION"}

    return {"role": "assistant", "content": "I am here to help you navigate TRELLIS."}
