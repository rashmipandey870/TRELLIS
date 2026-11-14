"""TRELLIS Curriculum & Pathways API Router (Slice 1.6).

Endpoints:
- GET  /api/v1/pathways: List published pathways with optional role filtering
- GET  /api/v1/pathways/first-90-days: Dedicated First-90-Days onboarding pathway
- GET  /api/v1/pathways/{id}: Retrieve detailed pathway course/module hierarchy
- POST /api/v1/pathways: Create pathway and validate prerequisite DAG (Transactional audit)
- POST /api/v1/pathways/{id}/publish: Publish pathway with SoD validation (Transactional audit)
- POST /api/v1/pathways/{id}/enrol: Enrol learner in pathway (Transactional audit)
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_claims, get_db, get_uow
from app.core.policy import require_permission
from app.core.uow import UnitOfWork
from app.models.curriculum import Enrolment, Pathway
from app.services.pathway_service import (
    create_pathway_service,
    enrol_user_in_pathway_service,
    publish_pathway_service,
)

router = APIRouter(prefix="/pathways", tags=["Pathways & Curriculum"])


# --- Schemas ---


class ModuleCreateSchema(BaseModel):
    title: str = Field(..., max_length=255)
    module_type: str = "LESSON"
    sequence_order: int = 1
    estimated_minutes: int = 30
    content_json: dict[str, Any] | None = None


class CourseCreateSchema(BaseModel):
    code: str = Field(..., max_length=64)
    title: str = Field(..., max_length=255)
    description: str | None = None
    sequence_order: int = 1
    prerequisite_code: str | None = None
    modules: list[ModuleCreateSchema] = []


class PathwayCreateSchema(BaseModel):
    code: str = Field(..., max_length=64)
    title: str = Field(..., max_length=255)
    description: str | None = None
    target_role_code: str | None = None
    estimated_hours: float = 0.0
    is_first_90_days: bool = False
    courses: list[CourseCreateSchema] = []


class ModuleResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    module_type: str
    sequence_order: int
    estimated_minutes: int


class CourseResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    code: str
    title: str
    description: str | None
    sequence_order: int
    modules: list[ModuleResponseSchema] = []


class PathwayResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    code: str
    title: str
    description: str | None
    is_published: bool
    target_role_code: str | None
    estimated_hours: float
    is_first_90_days: bool
    courses: list[CourseResponseSchema] = []


class EnrolmentResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    pathway_id: str
    user_id: str
    status: str
    progress_percent: float


# --- Endpoints ---


@router.get(
    "/first-90-days",
    response_model=PathwayResponseSchema,
    summary="Get First-90-Days onboarding pathway",
)
def get_first_90_days_pathway(
    claims: dict[str, Any] = Depends(get_current_user_claims),
    db: Session = Depends(get_db),
) -> Pathway:
    """Retrieve the active First-90-Days onboarding pathway for new engineering hires."""
    org_id = claims.get("org_id", "")
    stmt = (
        select(Pathway)
        .where(
            Pathway.org_id == org_id,
            Pathway.is_first_90_days.is_(True),
            Pathway.is_published.is_(True),
        )
        .limit(1)
    )
    pathway = db.execute(stmt).scalars().first()
    if not pathway:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active First-90-Days onboarding pathway configured for this organisation.",
        )
    return pathway


@router.get(
    "",
    response_model=list[PathwayResponseSchema],
    summary="List available learning pathways",
)
def list_pathways(
    include_drafts: bool = Query(False),
    target_role: str | None = Query(None),
    claims: dict[str, Any] = Depends(get_current_user_claims),
    db: Session = Depends(get_db),
) -> list[Pathway]:
    """List pathways accessible to the current user."""
    org_id = claims.get("org_id", "")
    roles = claims.get("roles", [])

    can_view_drafts = any(
        r in {"CONTENT_AUTHOR", "LK_ADMIN", "SUPER_ADMIN", "TRAINER_MENTOR"} for r in roles
    )

    stmt = select(Pathway).where(Pathway.org_id == org_id)

    if not (include_drafts and can_view_drafts):
        stmt = stmt.where(Pathway.is_published.is_(True))

    if target_role:
        stmt = stmt.where(Pathway.target_role_code == target_role)

    stmt = stmt.order_by(Pathway.created_at.desc())
    return list(db.execute(stmt).scalars().all())


@router.get(
    "/{id}",
    response_model=PathwayResponseSchema,
    summary="Get pathway details with courses and modules",
)
def get_pathway_detail(
    id: str,
    claims: dict[str, Any] = Depends(get_current_user_claims),
    db: Session = Depends(get_db),
) -> Pathway:
    """Retrieve complete curriculum hierarchy for a pathway."""
    org_id = claims.get("org_id", "")
    roles = claims.get("roles", [])
    pathway = db.get(Pathway, id)

    if not pathway or pathway.org_id != org_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pathway not found.")

    can_view_drafts = any(
        r in {"CONTENT_AUTHOR", "LK_ADMIN", "SUPER_ADMIN", "TRAINER_MENTOR"} for r in roles
    )
    if not pathway.is_published and not can_view_drafts and pathway.author_id != claims.get("sub"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pathway not found.")

    return pathway


@router.post(
    "",
    response_model=PathwayResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new learning pathway (Transactional audit)",
)
def create_pathway(
    payload: PathwayCreateSchema,
    request: Request,
    claims: dict[str, Any] = Depends(get_current_user_claims),
    uow: UnitOfWork = Depends(get_uow),
    _perm: Any = Depends(require_permission("create", "pathways")),
) -> Pathway:
    """Create a new learning pathway, validate course DAG, and commit in-transaction audit log."""
    org_id = claims.get("org_id", "")
    author_id = claims.get("sub", "")
    request_id = request.headers.get("X-Request-ID")

    courses_dicts = [c.model_dump() for c in payload.courses]

    try:
        pathway = create_pathway_service(
            uow=uow,
            org_id=org_id,
            author_id=author_id,
            code=payload.code,
            title=payload.title,
            description=payload.description,
            target_role_code=payload.target_role_code,
            estimated_hours=payload.estimated_hours,
            is_first_90_days=payload.is_first_90_days,
            courses_data=courses_dicts,
            request_id=request_id,
        )
        return pathway
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.post(
    "/{id}/publish",
    response_model=PathwayResponseSchema,
    summary="Publish a pathway with separation of duties (Transactional audit)",
)
def publish_pathway(
    id: str,
    request: Request,
    claims: dict[str, Any] = Depends(get_current_user_claims),
    uow: UnitOfWork = Depends(get_uow),
    _perm: Any = Depends(require_permission("publish", "pathways")),
) -> Pathway:
    """Publish a draft pathway. Separation of duties forbids author from publishing own pathway."""
    org_id = claims.get("org_id", "")
    publisher_id = claims.get("sub", "")
    request_id = request.headers.get("X-Request-ID")

    try:
        pathway = publish_pathway_service(
            uow=uow,
            pathway_id=id,
            publisher_id=publisher_id,
            org_id=org_id,
            request_id=request_id,
        )
        return pathway
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.post(
    "/{id}/enrol",
    response_model=EnrolmentResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Enrol learner in pathway (Transactional audit)",
)
def enrol_in_pathway(
    id: str,
    request: Request,
    claims: dict[str, Any] = Depends(get_current_user_claims),
    uow: UnitOfWork = Depends(get_uow),
    _perm: Any = Depends(require_permission("enrol", "enrolments")),
) -> Enrolment:
    """Enrol the authenticated learner in the specified learning pathway."""
    org_id = claims.get("org_id", "")
    user_id = claims.get("sub", "")
    request_id = request.headers.get("X-Request-ID")

    try:
        enrolment = enrol_user_in_pathway_service(
            uow=uow,
            pathway_id=id,
            user_id=user_id,
            org_id=org_id,
            request_id=request_id,
        )
        return enrolment
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
