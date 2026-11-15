"""TRELLIS Personalised Home API Router (Slice 1.7b).

Endpoints:
- GET /api/v1/home: Real-time learner dashboard computed from database state.
- POST /api/v1/home/freeze-streak: Transactionally audited streak freeze consumption.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_claims, get_db, get_uow
from app.core.policy import require_permission
from app.core.uow import UnitOfWork
from app.services.home_service import freeze_streak_service, get_home_data

router = APIRouter(prefix="/home", tags=["Home"])


# --- Schemas ---
class LearnerProfileSchema(BaseModel):
    id: str
    name: str
    email: str
    role: str
    avatar_url: str | None = None
    org_id: str
    role_code: str


class EnrolmentProgressSchema(BaseModel):
    enrolment_id: str
    pathway_id: str
    pathway_title: str
    pathway_code: str
    target_role_code: str | None = None
    progress_pct: int
    current_module_id: str
    current_module_name: str
    current_course_id: str
    current_course_title: str
    estimated_minutes_remaining: int
    total_modules: int
    completed_modules: int


class SkillGapSchema(BaseModel):
    skill_id: str
    skill_code: str
    skill_name: str
    category: str
    current_level: int
    required_level: int
    gap_magnitude: int
    is_critical: bool
    sample_size: int
    evidence_label: str  # STRONG_EVIDENCE | DEVELOPING_EVIDENCE | LIMITED_EVIDENCE | NOT_ENOUGH_DATA
    why_this: str


class DayActivitySchema(BaseModel):
    day_label: str
    date_str: str
    completed: bool
    is_today: bool


class ClimbingStreakSchema(BaseModel):
    current_streak_days: int
    longest_streak_days: int
    freezes_remaining: int
    has_activity_today: bool
    weekly_history: list[DayActivitySchema]


class AssignedSessionSchema(BaseModel):
    id: str
    title: str
    cohort_name: str
    trainer_name: str
    starts_at: str
    duration_minutes: int
    meeting_link: str
    session_type: str


class GreenhouseIdeaSchema(BaseModel):
    id: str
    title: str
    summary: str
    author_name: str
    author_role: str
    upvotes_count: int
    status: str
    tags: list[str]


class HomeDashboardResponseSchema(BaseModel):
    profile: LearnerProfileSchema
    enrolment: EnrolmentProgressSchema | None = None
    skill_gaps: list[SkillGapSchema]
    streak: ClimbingStreakSchema
    sessions: list[AssignedSessionSchema]
    greenhouse_idea: GreenhouseIdeaSchema


class FreezeStreakResponseSchema(BaseModel):
    user_id: str
    streak_freezes_remaining: int
    current_streak_days: int


# --- Endpoints ---
@router.get(
    "",
    response_model=HomeDashboardResponseSchema,
    summary="Get personalised home telemetry computed from real database state",
)
def get_home_dashboard(
    request: Request,
    claims: dict[str, Any] = Depends(get_current_user_claims),
    db: Session = Depends(get_db),
    _perm: Any = Depends(require_permission("read", "enrolments")),
) -> dict[str, Any]:
    """Compute complete personalised dashboard from database records for the authenticated user."""
    user_id = claims.get("sub", "")
    org_id = claims.get("org_id", "")

    try:
        data = get_home_data(session=db, user_id=user_id, org_id=org_id)
        return data
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.post(
    "/freeze-streak",
    response_model=FreezeStreakResponseSchema,
    summary="Consume one streak freeze in a transactionally audited mutation",
)
def consume_streak_freeze(
    request: Request,
    claims: dict[str, Any] = Depends(get_current_user_claims),
    uow: UnitOfWork = Depends(get_uow),
    _perm: Any = Depends(require_permission("read", "enrolments")),
) -> dict[str, Any]:
    """Consume a streak freeze. Decrements user streak freezes in DB and writes transactional audit row."""
    user_id = claims.get("sub", "")
    org_id = claims.get("org_id", "")
    request_id = request.headers.get("X-Request-ID")

    try:
        result = freeze_streak_service(
            uow=uow,
            user_id=user_id,
            org_id=org_id,
            request_id=request_id,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
