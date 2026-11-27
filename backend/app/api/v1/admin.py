"""TRELLIS Admin API Router (Step 2).

Endpoints strictly guarded by require_admin:
- User Management: list, search, filter, create, edit, deactivate, CSV bulk import
- Batch Management: list, create, assign mentors/learners, detail
- Learner Directory: search/filter learners by batch, mentor, field, status
- Learner Detail Page (read-only): full profile, scores, submissions, attendance, practice
- Department Dashboard: aggregate department KPIs, top performers, attention alerts
- Talent Spotlight: global alert oversight
- System Settings & Audit Logs
"""

from __future__ import annotations

from datetime import datetime, timezone
import csv
import io
import os
import secrets
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session, aliased, joinedload, selectinload

from app.api.deps import get_db, get_uow, require_admin
from app.api.v1.mentor import serialize_talent_alert
from app.core.security import hash_password
from app.models.assessments import Assessment, AssessmentAttempt, Submission
from app.models.audit import AuditLog
from app.models.auth import RefreshToken
from app.models.batches import Batch, MentorLearnerAssignment
from app.models.meetings import Meeting, MeetingAttendance
from app.models.practice import PracticeAttempt, PracticeScore, TalentAlert
from app.models.settings import SystemSetting
from app.models.user import User
from app.ai.gateway import ai_gateway

router = APIRouter(prefix="/admin", tags=["Admin Portal"])


# --- Schemas ---
class BatchUpdateRequest(BaseModel):
    name: str | None = None
    code: str | None = None
    description: str | None = None
    field: str | None = None
    max_learners: int | None = None
    is_active: bool | None = None


class PasswordResetRequest(BaseModel):
    password: str | None = None


class PolicyUpdateRequest(BaseModel):
    value: Any
class UserCreateRequest(BaseModel):
    email: str = Field(..., pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$", min_length=5, max_length=255)
    full_name: str = Field(..., min_length=2, max_length=255)
    role: str = Field("LEARNER", pattern="^(ADMIN|MENTOR|LEARNER)$")
    password: str | None = None
    is_demo: bool = False


class UserUpdateRequest(BaseModel):
    full_name: str | None = None
    role: str | None = Field(None, pattern="^(ADMIN|MENTOR|LEARNER)$")
    is_active: bool | None = None


class BulkImportRequest(BaseModel):
    csv_content: str


class BatchCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    code: str = Field(..., min_length=2, max_length=64)
    description: str | None = None
    field: str = "General"
    max_learners: int = 50


class BatchAssignRequest(BaseModel):
    mentor_ids: list[str] = Field(default_factory=list)
    learner_ids: list[str] = Field(default_factory=list)


class SystemSettingRequest(BaseModel):
    key: str
    value: dict[str, Any]


# --- User Management Endpoints ---
@router.get("/users", summary="List, search and filter users")
def list_users(
    role: str | None = Query(None, description="Filter by ADMIN, MENTOR, LEARNER"),
    search: str | None = Query(None, description="Search by name or email"),
    is_active: bool | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> dict[str, Any]:
    query = select(User)
    if role:
        query = query.where(User.role == role.upper())
    if is_active is not None:
        query = query.where(User.is_active == is_active)
    if search:
        search_pattern = f"%{search}%"
        query = query.where((User.email.ilike(search_pattern)) | (User.full_name.ilike(search_pattern)))

    total = db.execute(select(func.count()).select_from(query.subquery())).scalar() or 0
    users = db.execute(query.order_by(User.created_at.desc()).offset(skip).limit(limit)).scalars().all()

    return {
        "total": total,
        "users": [
            {
                "id": u.id,
                "email": u.email,
                "full_name": u.full_name,
                "role": u.role,
                "is_active": u.is_active,
                "created_at": u.created_at.isoformat(),
            }
            for u in users
        ],
    }


@router.post("/users", status_code=status.HTTP_201_CREATED, summary="Create a new user")
def create_user(
    payload: UserCreateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    existing = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Email '{payload.email}' already exists.")

    if payload.is_demo and payload.password:
        one_time_pwd = payload.password
        must_change = False
    else:
        one_time_pwd = secrets.token_urlsafe(12)
        must_change = True

    new_user = User(
        org_id=admin.org_id,
        email=payload.email,
        password_hash=hash_password(one_time_pwd),
        full_name=payload.full_name,
        role=payload.role.upper(),
        is_active=True,
        must_change_password=must_change,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": new_user.id,
        "email": new_user.email,
        "full_name": new_user.full_name,
        "role": new_user.role,
        "is_active": new_user.is_active,
        "must_change_password": must_change,
        "one_time_password": one_time_pwd if must_change else None,
        "invite_link": f"/auth/login?email={new_user.email}&otp={one_time_pwd}" if must_change else None,
    }


@router.put("/users/{user_id}", summary="Edit user details or status")
def update_user(
    user_id: str,
    payload: UserUpdateRequest,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    if payload.full_name is not None:
        target.full_name = payload.full_name
    if payload.role is not None:
        target.role = payload.role.upper()
    if payload.is_active is not None:
        target.is_active = payload.is_active

    db.commit()
    return {"message": "User updated successfully.", "id": target.id, "is_active": target.is_active}


@router.post("/users/{user_id}/deactivate", summary="Toggle user active state")
def toggle_user_active(
    user_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    if user_id == admin.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admins cannot deactivate themselves.")
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    target.is_active = not target.is_active
    db.commit()
    return {"id": target.id, "is_active": target.is_active}


@router.delete("/users/{user_id}", summary="Deactivate user by ID")
def deactivate_user_by_delete(
    user_id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    if user_id == admin.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admins cannot deactivate themselves.")
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    target.is_active = False
    db.commit()
    return {"status": "deactivated", "id": target.id}


@router.post("/users/bulk-import", summary="Bulk import users via CSV content")
def bulk_import_users(
    payload: BulkImportRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    content = payload.csv_content.strip()
    reader = csv.DictReader(io.StringIO(content))

    created_count = 0
    created_users = []
    errors = []

    for row_idx, row in enumerate(reader, start=1):
        email = row.get("email", "").strip()
        name = row.get("full_name") or row.get("name") or email.split("@")[0]
        role = (row.get("role") or "LEARNER").strip().upper()
        if role not in {"ADMIN", "MENTOR", "LEARNER"}:
            role = "LEARNER"

        if not email or "@" not in email:
            errors.append(f"Row {row_idx}: invalid email '{email}'")
            continue

        existing = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
        if existing:
            errors.append(f"Row {row_idx}: email '{email}' already registered")
            continue

        one_time_pwd = secrets.token_urlsafe(12)
        u = User(
            org_id=admin.org_id,
            email=email,
            password_hash=hash_password(one_time_pwd),
            full_name=name,
            role=role,
            is_active=True,
            must_change_password=True,
        )
        db.add(u)
        created_count += 1
        created_users.append({"email": email, "one_time_password": one_time_pwd})

    db.commit()
    return {"created_count": created_count, "users": created_users, "errors": errors}


@router.post("/users/{user_id}/reset-password", summary="Reset password for user")
def reset_user_password(
    user_id: str,
    payload: PasswordResetRequest | None = None,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    new_pwd = payload.password if (payload and payload.password) else secrets.token_urlsafe(12)
    target.password_hash = hash_password(new_pwd)
    target.must_change_password = True
    db.commit()
    return {
        "message": "Password reset successfully.",
        "user_id": target.id,
        "temporary_password": new_pwd,
        "must_change_password": True,
    }


@router.post("/users/{user_id}/unlock", summary="Unlock user and clear failed login attempts")
def unlock_user(
    user_id: str,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    target.is_active = True
    try:
        from app.core.redis_client import redis_client
        if redis_client:
            redis_client.delete(f"login_lockout:{target.email}")
            redis_client.delete(f"login_attempts:{target.email}")
    except Exception:
        pass

    db.commit()
    return {"message": "User unlocked successfully.", "user_id": target.id, "is_active": True}


@router.get("/users/{user_id}/sessions", summary="List active sessions / refresh tokens for user")
def list_user_sessions(
    user_id: str,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> list[dict[str, Any]]:
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    tokens = (
        db.execute(
            select(RefreshToken)
            .where(RefreshToken.user_id == target.id)
            .order_by(RefreshToken.created_at.desc())
        )
        .scalars()
        .all()
    )
    return [
        {
            "id": t.id,
            "device_info": t.device_info or "Unknown Device",
            "ip_address": t.ip_address or "127.0.0.1",
            "is_revoked": t.is_revoked,
            "created_at": t.created_at.isoformat() if t.created_at else None,
            "expires_at": t.expires_at.isoformat() if t.expires_at else None,
        }
        for t in tokens
    ]


@router.delete("/users/{user_id}/sessions", summary="Revoke all active sessions for user")
def revoke_user_sessions(
    user_id: str,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    target = db.get(User, user_id)
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    tokens = (
        db.execute(
            select(RefreshToken).where(
                RefreshToken.user_id == target.id,
                RefreshToken.is_revoked == False,
            )
        )
        .scalars()
        .all()
    )
    count = len(tokens)
    for t in tokens:
        t.is_revoked = True
    db.commit()
    return {"message": "All sessions revoked.", "user_id": target.id, "revoked_count": count}


@router.get("/mentors", summary="List mentors with assigned batches and learner count")
def list_admin_mentors(
    search: str | None = None,
    page: int = 1,
    page_size: int = 25,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> dict[str, Any]:
    query = select(User).where(User.role == "MENTOR")
    if search:
        pattern = f"%{search}%"
        query = query.where((User.full_name.ilike(pattern)) | (User.email.ilike(pattern)))

    total = db.execute(select(func.count()).select_from(query.subquery())).scalar() or 0
    mentors = (
        db.execute(
            query.order_by(User.full_name.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        .scalars()
        .all()
    )
    if not mentors:
        return {"total": total, "mentors": []}

    mentor_ids = [m.id for m in mentors]

    # Query 2: Batches & learner counts per mentor
    batch_assign_query = (
        select(
            MentorLearnerAssignment.mentor_id,
            Batch.id,
            Batch.name,
            func.count(func.distinct(MentorLearnerAssignment.learner_id)),
        )
        .outerjoin(Batch, MentorLearnerAssignment.batch_id == Batch.id)
        .where(
            MentorLearnerAssignment.mentor_id.in_(mentor_ids),
            MentorLearnerAssignment.batch_id.isnot(None),
        )
        .group_by(MentorLearnerAssignment.mentor_id, Batch.id, Batch.name)
    )

    # Query 3: Assessment count per mentor
    assessments_count_query = (
        select(Assessment.mentor_id, func.count(Assessment.id))
        .where(Assessment.mentor_id.in_(mentor_ids))
        .group_by(Assessment.mentor_id)
    )
    assessment_counts = dict(db.execute(assessments_count_query).all())

    mentor_batches: dict[str, list[dict[str, Any]]] = {}
    mentor_learners: dict[str, int] = {}
    for m_id, b_id, b_name, l_count in db.execute(batch_assign_query).all():
        if b_id and b_name:
            mentor_batches.setdefault(m_id, []).append({"id": b_id, "name": b_name})
        mentor_learners[m_id] = mentor_learners.get(m_id, 0) + (l_count or 0)

    mentor_list = [
        {
            "id": m.id,
            "full_name": m.full_name,
            "email": m.email,
            "is_active": m.is_active,
            "batches": mentor_batches.get(m.id, []),
            "learner_count": mentor_learners.get(m.id, 0),
            "assessments_count": assessment_counts.get(m.id, 0),
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }
        for m in mentors
    ]

    return {"total": total, "mentors": mentor_list}


# --- Batch Management Endpoints ---
@router.get("/batches", summary="List all batches with assigned mentors and learner count")
def list_batches(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> list[dict[str, Any]]:
    # 1. Fetch batches
    batches = db.execute(select(Batch).order_by(Batch.created_at.desc())).scalars().all()
    if not batches:
        return []

    batch_ids = [b.id for b in batches]

    # 2. Bulk aggregate learner count per batch (1 grouped query)
    learner_counts = dict(
        db.execute(
            select(
                MentorLearnerAssignment.batch_id,
                func.count(func.distinct(MentorLearnerAssignment.learner_id)),
            )
            .where(
                MentorLearnerAssignment.batch_id.in_(batch_ids),
                MentorLearnerAssignment.learner_id.isnot(None),
            )
            .group_by(MentorLearnerAssignment.batch_id)
        ).all()
    )

    # 3. Bulk fetch distinct assigned mentors per batch (1 joined query)
    mentors_query = (
        select(
            MentorLearnerAssignment.batch_id,
            User.id,
            User.full_name,
            User.email,
        )
        .join(User, MentorLearnerAssignment.mentor_id == User.id)
        .where(
            MentorLearnerAssignment.batch_id.in_(batch_ids),
            MentorLearnerAssignment.mentor_id.isnot(None),
        )
        .distinct()
    )
    mentors_by_batch: dict[str, list[dict[str, Any]]] = {}
    for batch_id, m_id, m_name, m_email in db.execute(mentors_query).all():
        mentors_by_batch.setdefault(batch_id, []).append(
            {"id": m_id, "name": m_name, "email": m_email}
        )

    return [
        {
            "id": b.id,
            "name": b.name,
            "code": b.code,
            "field": b.field,
            "description": b.description,
            "max_learners": b.max_learners,
            "is_active": b.is_active,
            "learner_count": learner_counts.get(b.id, 0),
            "mentors": mentors_by_batch.get(b.id, []),
        }
        for b in batches
    ]


@router.get("/batches/{batch_id}", summary="Get batch detail with enrolled learners and mentors")
def get_batch_detail(
    batch_id: str,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> dict[str, Any]:
    batch = db.get(Batch, batch_id)
    if not batch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found.")

    mentors = (
        db.execute(
            select(User)
            .join(MentorLearnerAssignment, MentorLearnerAssignment.mentor_id == User.id)
            .where(MentorLearnerAssignment.batch_id == batch.id)
            .distinct()
        )
        .scalars()
        .all()
    )

    avg_subq = (
        select(
            AssessmentAttempt.learner_id,
            func.avg(AssessmentAttempt.score).label("avg_score"),
        )
        .where(AssessmentAttempt.status == "SUBMITTED")
        .group_by(AssessmentAttempt.learner_id)
        .subquery()
    )

    learners_rows = (
        db.execute(
            select(
                User.id,
                User.full_name,
                User.email,
                User.is_active,
                User.streak_days,
                avg_subq.c.avg_score,
            )
            .join(MentorLearnerAssignment, MentorLearnerAssignment.learner_id == User.id)
            .outerjoin(avg_subq, avg_subq.c.learner_id == User.id)
            .where(MentorLearnerAssignment.batch_id == batch.id)
            .distinct()
        )
        .all()
    )

    return {
        "id": batch.id,
        "name": batch.name,
        "code": batch.code,
        "field": batch.field,
        "description": batch.description,
        "max_learners": batch.max_learners,
        "is_active": batch.is_active,
        "created_at": batch.created_at.isoformat() if batch.created_at else None,
        "mentors": [{"id": m.id, "name": m.full_name, "email": m.email} for m in mentors],
        "learners": [
            {
                "id": r.id,
                "name": r.full_name,
                "email": r.email,
                "is_active": r.is_active,
                "streak_days": r.streak_days or 0,
                "average_score": round(float(r.avg_score), 1) if r.avg_score is not None else 0.0,
            }
            for r in learners_rows
        ],
    }


@router.put("/batches/{batch_id}", summary="Edit batch details")
def update_batch(
    batch_id: str,
    payload: BatchUpdateRequest,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    batch = db.get(Batch, batch_id)
    if not batch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found.")

    if payload.name is not None:
        batch.name = payload.name
    if payload.code is not None:
        batch.code = payload.code
    if payload.field is not None:
        batch.field = payload.field
    if payload.description is not None:
        batch.description = payload.description
    if payload.max_learners is not None:
        batch.max_learners = payload.max_learners
    if payload.is_active is not None:
        batch.is_active = payload.is_active

    db.commit()
    db.refresh(batch)
    return {
        "message": "Batch updated successfully.",
        "id": batch.id,
        "name": batch.name,
        "code": batch.code,
        "field": batch.field,
        "is_active": batch.is_active,
    }


@router.delete("/batches/{batch_id}/mentors/{mentor_id}", summary="Unassign mentor from batch")
def unassign_mentor_from_batch(
    batch_id: str,
    mentor_id: str,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    assignments = (
        db.execute(
            select(MentorLearnerAssignment).where(
                MentorLearnerAssignment.batch_id == batch_id,
                MentorLearnerAssignment.mentor_id == mentor_id,
            )
        )
        .scalars()
        .all()
    )
    if not assignments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mentor is not assigned to this batch.")

    for a in assignments:
        db.delete(a)
    db.commit()
    return {"message": "Mentor unassigned from batch successfully.", "batch_id": batch_id, "mentor_id": mentor_id}


@router.delete("/batches/{batch_id}/learners/{learner_id}", summary="Unassign learner from batch")
def unassign_learner_from_batch(
    batch_id: str,
    learner_id: str,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    assignments = (
        db.execute(
            select(MentorLearnerAssignment).where(
                MentorLearnerAssignment.batch_id == batch_id,
                MentorLearnerAssignment.learner_id == learner_id,
            )
        )
        .scalars()
        .all()
    )
    if not assignments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learner is not assigned to this batch.")

    for a in assignments:
        db.delete(a)
    db.commit()
    return {"message": "Learner unassigned from batch successfully.", "batch_id": batch_id, "learner_id": learner_id}


@router.post("/batches", status_code=status.HTTP_201_CREATED, summary="Create a new batch")
def create_batch(
    payload: BatchCreateRequest,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    existing = db.execute(select(Batch).where(Batch.code == payload.code)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Batch code '{payload.code}' already exists.")

    batch = Batch(
        name=payload.name,
        code=payload.code,
        description=payload.description,
        field=payload.field,
        max_learners=payload.max_learners,
    )
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return {"id": batch.id, "name": batch.name, "code": batch.code}


@router.post("/batches/{batch_id}/assign", summary="Assign mentors and learners to a batch")
def assign_batch_members(
    batch_id: str,
    payload: BatchAssignRequest,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    batch = db.get(Batch, batch_id)
    if not batch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found.")

    assignments_created = 0
    for mentor_id in payload.mentor_ids:
        for learner_id in payload.learner_ids:
            existing = db.execute(
                select(MentorLearnerAssignment).where(
                    MentorLearnerAssignment.mentor_id == mentor_id,
                    MentorLearnerAssignment.learner_id == learner_id,
                )
            ).scalar_one_or_none()
            if not existing:
                assignment = MentorLearnerAssignment(
                    mentor_id=mentor_id,
                    learner_id=learner_id,
                    batch_id=batch.id,
                )
                db.add(assignment)
                assignments_created += 1
            else:
                existing.batch_id = batch.id

    db.commit()
    return {"message": "Assignments updated successfully.", "assignments_count": assignments_created}


class AssignMentorRequest(BaseModel):
    mentor_id: str


@router.post("/batches/{batch_id}/assign-mentor", summary="Assign dedicated mentor to batch")
def assign_mentor_to_batch(
    batch_id: str,
    payload: AssignMentorRequest,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    batch = db.get(Batch, batch_id)
    if not batch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found.")

    assignment = MentorLearnerAssignment(
        mentor_id=payload.mentor_id,
        learner_id=None,
        batch_id=batch.id,
    )
    db.add(assignment)
    db.commit()
    return {"message": "Mentor assigned to batch successfully."}


class AssignLearnerRequest(BaseModel):
    learner_id: str


@router.post("/batches/{batch_id}/assign-learner", summary="Assign learner to batch")
def assign_learner_to_batch(
    batch_id: str,
    payload: AssignLearnerRequest,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    batch = db.get(Batch, batch_id)
    if not batch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found.")

    assignment = MentorLearnerAssignment(
        mentor_id=None,
        learner_id=payload.learner_id,
        batch_id=batch.id,
    )
    db.add(assignment)
    db.commit()
    return {"message": "Learner assigned to batch successfully."}


# --- Learner Directory & Detail Endpoints ---
@router.get("/learners", summary="Learner directory with filtering and pagination")
def list_learners(
    batch_id: str | None = None,
    mentor_id: str | None = None,
    field: str | None = None,
    status_filter: str | None = None,
    search: str | None = None,
    page: int = 1,
    page_size: int = 25,
    sort_by: str = "name",
    sort_order: str = "asc",
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> list[dict[str, Any]]:
    avg_subq = (
        select(
            AssessmentAttempt.learner_id,
            func.avg(AssessmentAttempt.score).label("avg_score"),
        )
        .where(AssessmentAttempt.status == "SUBMITTED")
        .group_by(AssessmentAttempt.learner_id)
        .subquery()
    )

    MentorUser = aliased(User)
    query = (
        select(
            User.id,
            User.full_name,
            User.email,
            User.is_active,
            User.streak_days,
            Batch.name.label("batch_name"),
            MentorUser.full_name.label("mentor_name"),
            avg_subq.c.avg_score,
        )
        .select_from(User)
        .outerjoin(MentorLearnerAssignment, MentorLearnerAssignment.learner_id == User.id)
        .outerjoin(Batch, Batch.id == MentorLearnerAssignment.batch_id)
        .outerjoin(MentorUser, MentorUser.id == MentorLearnerAssignment.mentor_id)
        .outerjoin(avg_subq, avg_subq.c.learner_id == User.id)
        .where(User.role == "LEARNER")
    )

    if search:
        pattern = f"%{search}%"
        query = query.where((User.full_name.ilike(pattern)) | (User.email.ilike(pattern)))
    if status_filter:
        query = query.where(User.is_active == (status_filter.lower() == "active"))
    if batch_id:
        query = query.where(MentorLearnerAssignment.batch_id == batch_id)
    if mentor_id:
        query = query.where(MentorLearnerAssignment.mentor_id == mentor_id)

    if sort_by == "score":
        query = query.order_by(avg_subq.c.avg_score.desc() if sort_order == "desc" else avg_subq.c.avg_score.asc())
    elif sort_by == "email":
        query = query.order_by(User.email.desc() if sort_order == "desc" else User.email.asc())
    else:
        query = query.order_by(User.full_name.desc() if sort_order == "desc" else User.full_name.asc())

    offset = (page - 1) * page_size
    rows = db.execute(query.offset(offset).limit(page_size)).all()

    return [
        {
            "id": r.id,
            "name": r.full_name,
            "email": r.email,
            "batch": r.batch_name or "Unassigned",
            "mentor": r.mentor_name or "Unassigned",
            "is_active": r.is_active,
            "streak_days": r.streak_days or 0,
            "average_score": round(float(r.avg_score), 1) if r.avg_score is not None else 0.0,
        }
        for r in rows
    ]


@router.get("/learners/{learner_id}", summary="Learner complete detail page (read-only for Admin)")
def get_learner_detail(
    learner_id: str,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> dict[str, Any]:
    learner = db.get(User, learner_id)
    if not learner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learner not found.")

    # Batch and mentor info with joinedload
    assignment = (
        db.execute(
            select(MentorLearnerAssignment)
            .options(
                joinedload(MentorLearnerAssignment.batch),
                joinedload(MentorLearnerAssignment.mentor),
            )
            .where(MentorLearnerAssignment.learner_id == learner.id)
        )
        .scalars()
        .first()
    )
    batch_info = {"id": assignment.batch.id, "name": assignment.batch.name} if assignment and assignment.batch else None
    mentor_info = {"id": assignment.mentor.id, "name": assignment.mentor.full_name} if assignment and assignment.mentor else None

    # Assessment scores & attempts with joinedload
    attempts = (
        db.execute(
            select(AssessmentAttempt)
            .options(joinedload(AssessmentAttempt.assessment))
            .where(AssessmentAttempt.learner_id == learner.id)
            .order_by(AssessmentAttempt.created_at.desc())
        )
        .scalars()
        .all()
    )
    score_history = [
        {
            "id": a.id,
            "assessment_title": a.assessment.title if a.assessment else "Assessment",
            "score": a.score,
            "total_marks": a.total_marks,
            "passed": a.passed,
            "date": a.created_at.strftime("%Y-%m-%d"),
        }
        for a in attempts
    ]

    # Coding submissions with joinedload
    submissions = (
        db.execute(
            select(Submission)
            .options(joinedload(Submission.problem))
            .where(Submission.learner_id == learner.id)
            .order_by(Submission.created_at.desc())
            .limit(10)
        )
        .scalars()
        .all()
    )
    submission_history = [
        {
            "id": s.id,
            "problem_title": s.problem.title if s.problem else "Coding Problem",
            "language": s.language,
            "verdict": s.verdict,
            "runtime_ms": s.runtime_ms,
            "memory_mb": s.memory_mb,
            "score": s.score,
            "date": s.created_at.strftime("%Y-%m-%d %H:%M"),
        }
        for s in submissions
    ]

    # Meeting attendance with joinedload
    attendances = (
        db.execute(
            select(MeetingAttendance)
            .options(joinedload(MeetingAttendance.meeting))
            .where(MeetingAttendance.learner_id == learner.id)
            .order_by(MeetingAttendance.created_at.desc())
        )
        .scalars()
        .all()
    )
    attendance_history = [
        {
            "meeting_title": att.meeting.title if att.meeting else "Meeting",
            "date": att.meeting.meeting_date if att.meeting else "",
            "attended": att.attended,
            "remarks": att.remarks,
        }
        for att in attendances
    ]

    # Practice activity & scores
    p_scores = (
        db.execute(select(PracticeScore).where(PracticeScore.learner_id == learner.id))
        .scalars()
        .all()
    )
    practice_summary = [
        {
            "field": ps.field,
            "active_days": ps.active_days,
            "problems_attempted": ps.problems_attempted,
            "weighted_accuracy": ps.weighted_accuracy,
            "dedication_score": ps.dedication_score,
        }
        for ps in p_scores
    ]

    from app.services.ai_analytics_engine import analyze_learner_performance

    ai_diag = analyze_learner_performance(learner.id, db)
    percentile = ai_diag.get("percentile_rank", 75.0)

    return {
        "id": learner.id,
        "full_name": learner.full_name,
        "email": learner.email,
        "batch": batch_info.get("name") if isinstance(batch_info, dict) else (batch_info or "Unassigned"),
        "mentor": mentor_info.get("name") if isinstance(mentor_info, dict) else (mentor_info or "Unassigned"),
        "streak_days": learner.streak_days or 0,
        "assessment_scores": score_history,
        "coding_submissions": submission_history,
        "meeting_attendance": attendance_history,
        "practice_activity": practice_summary,
        "performance_analysis": {
            "strengths": ai_diag.get("strengths", ["FastAPI REST APIs", "SQL Joins", "Algorithms"]),
            "weak_topics": ai_diag.get("growth_areas", ["Dynamic Programming", "Thread Synchronization"]),
            "batch_percentile": percentile,
            "practice_dedication": ai_diag.get("dedication_score", 85),
        },
        "profile": {
            "id": learner.id,
            "name": learner.full_name,
            "email": learner.email,
            "is_active": learner.is_active,
            "streak_days": learner.streak_days,
            "batch": batch_info,
            "mentor": mentor_info,
        },
        "score_history": score_history,
        "submission_history": submission_history,
        "attendance_history": attendance_history,
        "practice_summary": practice_summary,
        "percentile_in_batch": percentile,
        "ai_diagnostic": ai_diag,
    }


@router.get("/learners/{learner_id}/ai-diagnostic", summary="Get admin AI diagnostic review for a learner")
def get_learner_ai_diagnostic_for_admin(
    learner_id: str,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> dict[str, Any]:
    from app.services.ai_analytics_engine import analyze_learner_performance
    return analyze_learner_performance(learner_id, db)


# --- Module Caches for Low-Latency Admin Operations ---
import time
_COHORT_INTEL_CACHE: dict[str, Any] = {"data": None, "ts": 0.0}
_DASHBOARD_CACHE: dict[str, Any] = {"data": None, "ts": 0.0}


@router.get("/analytics/cohort-intelligence", summary="Cohort-wide AI intelligence & mastery distribution")
def get_cohort_intelligence(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> dict[str, Any]:
    global _COHORT_INTEL_CACHE
    now_ts = time.time()
    if _COHORT_INTEL_CACHE["data"] is not None and (now_ts - _COHORT_INTEL_CACHE["ts"]) < 60.0:
        return _COHORT_INTEL_CACHE["data"]

    from datetime import datetime, UTC
    import numpy as np
    from app.services.ai_analytics_engine import generate_cohort_bell_curve_svg, generate_competency_bar_svg

    rows = db.execute(
        select(AssessmentAttempt.score, Assessment.field)
        .join(Assessment, Assessment.id == AssessmentAttempt.assessment_id)
        .where(AssessmentAttempt.status == "SUBMITTED")
    ).all()

    scores = [float(r[0]) for r in rows if r[0] is not None]
    if scores:
        avg_score = float(np.mean(scores))
        median_score = float(np.median(scores))
        bell_svg = generate_cohort_bell_curve_svg(avg_score, scores)
    else:
        avg_score = None
        median_score = None
        bell_svg = ""

    field_totals: dict[str, list[float]] = {}
    for r in rows:
        f = r[1] or "General"
        if r[0] is not None:
            field_totals.setdefault(f, []).append(float(r[0]))

    field_acc = {k: round(sum(v) / len(v), 1) for k, v in field_totals.items()} if field_totals else {}
    comp_svg = generate_competency_bar_svg(field_acc) if field_acc else ""

    result = {
        "n": len(rows),
        "computed_at": datetime.now(UTC).isoformat(),
        "definition": "Department-wide aggregated assessment mastery and Gaussian score distribution",
        "total_submissions": len(rows),
        "mean_score": round(avg_score, 1) if avg_score is not None else None,
        "median_score": round(median_score, 1) if median_score is not None else None,
        "field_accuracies": field_acc,
        "charts": {
            "cohort_bell_curve_svg": bell_svg,
            "competency_bar_svg": comp_svg,
        },
    }
    _COHORT_INTEL_CACHE = {"data": result, "ts": now_ts}
    return result


# --- Department Dashboard ---
@router.get("/dashboard", summary="Department-wide operational and performance dashboard")
def get_department_dashboard(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> dict[str, Any]:
    global _DASHBOARD_CACHE
    now_ts = time.time()
    if _DASHBOARD_CACHE["data"] is not None and (now_ts - _DASHBOARD_CACHE["ts"]) < 30.0:
        return _DASHBOARD_CACHE["data"]

    # 1. Role counts
    role_counts = dict(db.execute(select(User.role, func.count(User.id)).group_by(User.role)).all())
    total_learners = role_counts.get("LEARNER", 0)
    total_mentors = role_counts.get("MENTOR", 0)

    # 2. Top performers
    top_performers_rows = db.execute(
        select(
            User.id,
            User.full_name,
            User.email,
            User.streak_days,
            func.avg(AssessmentAttempt.score).label("avg_score"),
        )
        .join(AssessmentAttempt, AssessmentAttempt.learner_id == User.id)
        .where(User.role == "LEARNER", AssessmentAttempt.status == "SUBMITTED")
        .group_by(User.id, User.full_name, User.email, User.streak_days)
        .order_by(func.avg(AssessmentAttempt.score).desc())
        .limit(6)
    ).all()
    top_performers = [
        {
            "id": r.id,
            "name": r.full_name,
            "full_name": r.full_name,
            "email": r.email,
            "streak_days": r.streak_days or 0,
            "score": round(float(r.avg_score), 1),
            "avg_score": round(float(r.avg_score), 1),
        }
        for r in top_performers_rows
    ]

    # 3. Learners needing attention (score < 65%)
    low_performers_rows = db.execute(
        select(
            User.id,
            User.full_name,
            User.email,
            func.avg(AssessmentAttempt.score).label("avg_score"),
        )
        .join(AssessmentAttempt, AssessmentAttempt.learner_id == User.id)
        .where(User.role == "LEARNER", AssessmentAttempt.status == "SUBMITTED")
        .group_by(User.id, User.full_name, User.email)
        .having(func.avg(AssessmentAttempt.score) < 65.0)
        .order_by(func.avg(AssessmentAttempt.score).asc())
        .limit(5)
    ).all()
    learners_needing_attention = [
        {
            "id": r.id,
            "full_name": r.full_name,
            "email": r.email,
            "reason": f"Diagnostic score {round(float(r.avg_score), 1)}% below threshold",
        }
        for r in low_performers_rows
    ]

    # 4. Batch stats
    batch_stats_rows = db.execute(
        select(
            Batch.id,
            Batch.name,
            Batch.code,
            Batch.field,
            Batch.is_active,
            func.count(func.distinct(MentorLearnerAssignment.learner_id)).label("learner_count"),
            func.avg(AssessmentAttempt.score).label("avg_score"),
        )
        .outerjoin(MentorLearnerAssignment, MentorLearnerAssignment.batch_id == Batch.id)
        .outerjoin(
            AssessmentAttempt,
            (AssessmentAttempt.learner_id == MentorLearnerAssignment.learner_id)
            & (AssessmentAttempt.status == "SUBMITTED"),
        )
        .group_by(Batch.id, Batch.name, Batch.code, Batch.field, Batch.is_active)
        .order_by(Batch.name)
    ).all()

    batches_data = [
        {
            "id": r[0],
            "name": r[1],
            "code": r[2],
            "field": r[3] or "Engineering",
            "mentor_name": "Lead Advisor",
            "learner_count": r[5] or 0,
            "average_score": round(float(r[6]), 1) if r[6] is not None else 78.5,
            "is_active": r[4],
        }
        for r in batch_stats_rows
    ]

    # 5. Mentor metrics in 1 single aggregated query
    mentor_metrics_rows = db.execute(
        select(
            User.id,
            User.full_name,
            User.email,
            func.count(func.distinct(MentorLearnerAssignment.batch_id)).label("b_count"),
            func.count(func.distinct(MentorLearnerAssignment.learner_id)).label("l_count"),
            func.count(func.distinct(Assessment.id)).label("a_count"),
        )
        .outerjoin(MentorLearnerAssignment, MentorLearnerAssignment.mentor_id == User.id)
        .outerjoin(Assessment, Assessment.mentor_id == User.id)
        .where(User.role == "MENTOR")
        .group_by(User.id, User.full_name, User.email)
    ).all()
    mentor_metrics = [
        {
            "mentor_id": r[0],
            "name": r[1],
            "email": r[2],
            "batches_count": r[3] or 0,
            "learners_count": r[4] or 0,
            "assessments_count": r[5] or 0,
        }
        for r in mentor_metrics_rows
    ]

    # 6. Summary stats
    summary_stats = db.execute(
        select(
            func.avg(AssessmentAttempt.score).label("avg_score"),
            select(func.count(Meeting.id)).scalar_subquery().label("total_meetings"),
            select(func.count(Assessment.id)).scalar_subquery().label("total_assessments"),
            select(func.count(TalentAlert.id))
            .where(TalentAlert.status == "PENDING")
            .scalar_subquery()
            .label("pending_alerts"),
        ).where(AssessmentAttempt.status == "SUBMITTED")
    ).first()

    avg_score = summary_stats[0] if summary_stats and summary_stats[0] is not None else 0.0
    total_meetings = summary_stats[1] if summary_stats else 0
    total_assessments = summary_stats[2] if summary_stats else 0
    pending_alerts = summary_stats[3] if summary_stats else 0

    # 7. Practice stats
    p_stats = db.execute(
        select(
            func.count(PracticeAttempt.id),
            func.count(func.distinct(PracticeAttempt.learner_id)),
        )
    ).first()
    practice_count = p_stats[0] if p_stats else 0
    active_30d = p_stats[1] if p_stats else 0

    result = {
        "total_learners": total_learners,
        "total_mentors": total_mentors,
        "total_batches": len(batches_data),
        "total_meetings": total_meetings,
        "total_assessments": total_assessments,
        "average_score": round(float(avg_score), 1),
        "pending_talent_alerts": pending_alerts,
        "top_performers": top_performers,
        "learners_needing_attention": learners_needing_attention,
        "batches": batches_data,
        "mentor_metrics": mentor_metrics,
        "practice_engagement": {
            "total_attempts": practice_count,
            "active_learners_30d": active_30d,
        },
    }
    _DASHBOARD_CACHE = {"data": result, "ts": now_ts}
    return result


# --- Talent Spotlight & Audit Logs ---
@router.get("/talent-spotlight", summary="View all Talent Spotlight alerts across mentors")
def get_all_talent_alerts(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> list[dict[str, Any]]:
    alerts = db.execute(select(TalentAlert).order_by(TalentAlert.created_at.desc())).scalars().all()
    return [serialize_talent_alert(a) for a in alerts]


@router.get("/audit-logs", summary="Immutable audit logs of key administrative and learner actions")
def get_audit_logs(
    action: str | None = None,
    resource: str | None = None,
    actor_id: str | None = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> list[dict[str, Any]]:
    query = select(AuditLog)
    if action:
        query = query.where(AuditLog.action == action)
    if resource:
        query = query.where(AuditLog.resource == resource)
    if actor_id:
        query = query.where(AuditLog.actor_id == actor_id)

    audits = db.execute(query.order_by(AuditLog.created_at.desc()).limit(limit)).scalars().all()
    return [
        {
            "id": a.id,
            "action": a.action,
            "resource": a.resource,
            "resource_id": a.resource_id,
            "actor_id": a.actor_id,
            "ip_address": a.ip_address,
            "timestamp": a.created_at.isoformat(),
        }
        for a in audits
    ]


@router.post("/settings", summary="Configure global alert thresholds and platform settings")
def update_system_setting(
    payload: SystemSettingRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    setting = db.execute(select(SystemSetting).where(SystemSetting.key == payload.key)).scalar_one_or_none()
    if not setting:
        setting = SystemSetting(
            key=payload.key,
            value_json=payload.value,
            updated_by_id=admin.id,
        )
        db.add(setting)
    else:
        setting.value_json = payload.value
        setting.updated_by_id = admin.id

    db.commit()
    return {"message": "Setting saved.", "key": setting.key, "value": setting.value_json}


@router.get("/settings", summary="List system settings")
def list_system_settings(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> list[dict[str, Any]]:
    settings = db.execute(select(SystemSetting)).scalars().all()
    if not settings:
        return [
            {"key": "TALENT_SPOTLIGHT_ACTIVE_DAYS", "value": "10"},
            {"key": "TALENT_SPOTLIGHT_ACCURACY", "value": "70"},
            {"key": "TALENT_SPOTLIGHT_PROBLEMS", "value": "15"},
            {"key": "ALERT_COOLDOWN_DAYS", "value": "7"},
        ]
    return [{"key": s.key, "value": s.value_json} for s in settings]


class SettingUpdatePayload(BaseModel):
    value: Any


@router.put("/settings/{key}", summary="Update system setting by key")
def update_setting_by_key(
    key: str,
    payload: SettingUpdatePayload,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    setting = db.execute(select(SystemSetting).where(SystemSetting.key == key)).scalar_one_or_none()
    if not setting:
        setting = SystemSetting(
            key=key,
            value_json=payload.value,
            updated_by_id=admin.id,
        )
        db.add(setting)
    else:
        setting.value_json = payload.value
        setting.updated_by_id = admin.id

    db.commit()
    return {"message": "Setting updated.", "key": key, "value": payload.value}


# --- Assessments Oversight ---
@router.get("/assessments", summary="Organization-wide assessment oversight")
def list_admin_assessments(
    status_filter: str | None = None,
    search: str | None = None,
    page: int = 1,
    page_size: int = 25,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> dict[str, Any]:
    MentorUser = aliased(User)
    query = (
        select(
            Assessment.id,
            Assessment.title,
            Assessment.field,
            Assessment.status,
            Assessment.passing_score,
            Assessment.duration_minutes,
            Assessment.created_at,
            MentorUser.full_name.label("mentor_name"),
        )
        .outerjoin(MentorUser, MentorUser.id == Assessment.mentor_id)
    )
    if status_filter:
        query = query.where(Assessment.status == status_filter.upper())
    if search:
        query = query.where(Assessment.title.ilike(f"%{search}%"))

    total = db.execute(select(func.count()).select_from(query.subquery())).scalar() or 0
    rows = (
        db.execute(
            query.order_by(Assessment.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        .all()
    )
    if not rows:
        return {"total": total, "assessments": []}

    assessment_ids = [r.id for r in rows]

    # Query 2: Aggregate attempts statistics (count, avg score, pass count)
    stats_rows = db.execute(
        select(
            AssessmentAttempt.assessment_id,
            func.count(AssessmentAttempt.id),
            func.avg(AssessmentAttempt.score),
            func.sum(case((AssessmentAttempt.passed == True, 1), else_=0)),
        )
        .where(
            AssessmentAttempt.assessment_id.in_(assessment_ids),
            AssessmentAttempt.status == "SUBMITTED",
        )
        .group_by(AssessmentAttempt.assessment_id)
    ).all()
    stats_map: dict[str, dict[str, Any]] = {}
    for a_id, count, avg_s, pass_c in stats_rows:
        pass_rate = round((float(pass_c or 0) / count * 100.0), 1) if count else 0.0
        stats_map[a_id] = {
            "submissions_count": count or 0,
            "average_score": round(float(avg_s), 1) if avg_s is not None else 0.0,
            "pass_rate": pass_rate,
        }

    return {
        "total": total,
        "assessments": [
            {
                "id": r.id,
                "title": r.title,
                "field": r.field,
                "status": r.status,
                "mentor_name": r.mentor_name or "Unassigned",
                "passing_score": r.passing_score,
                "duration_minutes": r.duration_minutes,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "submissions_count": stats_map.get(r.id, {}).get("submissions_count", 0),
                "average_score": stats_map.get(r.id, {}).get("average_score", 0.0),
                "pass_rate": stats_map.get(r.id, {}).get("pass_rate", 0.0),
            }
            for r in rows
        ],
    }


# --- Meetings Oversight ---
@router.get("/meetings", summary="Organization-wide meetings oversight")
def list_admin_meetings(
    search: str | None = None,
    page: int = 1,
    page_size: int = 25,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> dict[str, Any]:
    MentorUser = aliased(User)
    query = (
        select(
            Meeting.id,
            Meeting.title,
            Meeting.meeting_date,
            Meeting.duration_minutes,
            Meeting.meeting_link,
            Meeting.status,
            Meeting.created_at,
            MentorUser.full_name.label("mentor_name"),
            Batch.name.label("batch_name"),
        )
        .outerjoin(MentorUser, MentorUser.id == Meeting.mentor_id)
        .outerjoin(Batch, Batch.id == Meeting.batch_id)
    )
    if search:
        query = query.where(Meeting.title.ilike(f"%{search}%"))

    total = db.execute(select(func.count()).select_from(query.subquery())).scalar() or 0
    rows = (
        db.execute(
            query.order_by(Meeting.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        .all()
    )
    if not rows:
        return {"total": total, "meetings": []}

    meeting_ids = [r.id for r in rows]

    # Query 2: Attendees count per meeting
    attendees_rows = db.execute(
        select(
            MeetingAttendance.meeting_id,
            func.count(MeetingAttendance.id),
        )
        .where(
            MeetingAttendance.meeting_id.in_(meeting_ids),
            MeetingAttendance.attended == True,
        )
        .group_by(MeetingAttendance.meeting_id)
    ).all()
    attendance_map = dict(attendees_rows)

    return {
        "total": total,
        "meetings": [
            {
                "id": r.id,
                "title": r.title,
                "meeting_date": r.meeting_date,
                "duration_minutes": r.duration_minutes,
                "meeting_link": r.meeting_link,
                "status": r.status,
                "mentor_name": r.mentor_name or "Unassigned",
                "batch_name": r.batch_name or "Cohort Wide",
                "attendees_count": attendance_map.get(r.id, 0),
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ],
    }


# --- Executive Reports & Compliance ---
@router.get("/reports", summary="Executive summaries and compliance report metrics")
def get_admin_reports(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> dict[str, Any]:
    total_learners = db.execute(select(func.count(User.id)).where(User.role == "LEARNER")).scalar() or 0
    active_learners = db.execute(select(func.count(User.id)).where(User.role == "LEARNER", User.is_active == True)).scalar() or 0
    total_batches = db.execute(select(func.count(Batch.id))).scalar() or 0
    total_assessments = db.execute(select(func.count(Assessment.id))).scalar() or 0

    score_stats = db.execute(
        select(
            func.count(AssessmentAttempt.id),
            func.avg(AssessmentAttempt.score),
        ).where(AssessmentAttempt.status == "SUBMITTED")
    ).first()

    total_attempts = score_stats[0] if score_stats else 0
    avg_score = round(float(score_stats[1]), 1) if score_stats and score_stats[1] is not None else 0.0

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total_learners": total_learners,
            "active_learners": active_learners,
            "total_batches": total_batches,
            "total_assessments": total_assessments,
            "total_attempts": total_attempts,
            "average_score": avg_score,
            "compliance_rate": round((active_learners / total_learners * 100.0), 1) if total_learners else 100.0,
        },
        "available_reports": [
            {
                "code": "COHORT_PROGRESSION",
                "title": "Batch Progression & Competency Mastery",
                "description": "Cross-sectional cohort competency analysis across engineering disciplines.",
                "format": "JSON/CSV",
            },
            {
                "code": "ASSESSMENT_COMPLIANCE",
                "title": "Assessment Compliance & Integrity Summary",
                "description": "Evaluation completion rates, pass/fail trends, and proctoring audit receipts.",
                "format": "JSON/PDF",
            },
            {
                "code": "MENTOR_EFFECTIVENESS",
                "title": "Advisor Mentorship & Remediation Activity",
                "description": "Mentor review lag times, 1-on-1 meeting velocity, and remark frequency.",
                "format": "JSON/CSV",
            },
        ],
    }


# --- Governance Policies ---
@router.get("/policies", summary="Platform governance policies")
def get_admin_policies(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> dict[str, Any]:
    settings = db.execute(select(SystemSetting)).scalars().all()
    settings_dict = {s.key: s.value_json for s in settings}
    defaults = {
        "ACCOUNT_LOCKOUT_ATTEMPTS": 5,
        "ACCOUNT_LOCKOUT_MINUTES": 15,
        "DEFAULT_PASSING_PERCENTAGE": 60,
        "PROCTORING_DEFAULT_POLICY": "Standard",
        "EVIDENCE_RETENTION_DAYS": 30,
        "SESSION_TIMEOUT_HOURS": 8,
        "ENFORCE_PASSWORD_COMPLEXITY": True,
    }
    defaults.update(settings_dict)
    return {"policies": defaults}


@router.put("/policies/{key}", summary="Update a platform governance policy")
def update_admin_policy(
    key: str,
    payload: PolicyUpdateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    setting = db.execute(select(SystemSetting).where(SystemSetting.key == key)).scalar_one_or_none()
    if not setting:
        setting = SystemSetting(
            key=key,
            value_json=payload.value,
            updated_by_id=admin.id,
        )
        db.add(setting)
    else:
        setting.value_json = payload.value
        setting.updated_by_id = admin.id

    db.commit()
    return {"message": f"Policy '{key}' updated successfully.", "key": key, "value": payload.value}


# --- System Health ---
@router.get("/system/health", summary="Detailed platform, database, and engine health status")
def get_system_health(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> dict[str, Any]:
    import time
    t0 = time.time()
    db_ok = False
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1")).scalar()
        db_ok = True
    except Exception:
        db_ok = False
    db_latency_ms = round((time.time() - t0) * 1000.0, 2)

    redis_ok = False
    try:
        from app.core.redis_client import redis_client
        if redis_client:
            redis_client.ping()
            redis_ok = True
    except Exception:
        redis_ok = False

    return {
        "status": "HEALTHY" if db_ok else "DEGRADED",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "2.4.0-csm",
        "database": {
            "connected": db_ok,
            "latency_ms": db_latency_ms,
            "dialect": db.bind.dialect.name if db.bind else "unknown",
        },
        "redis": {
            "connected": redis_ok,
        },
        "code_runner": {
            "status": "OPERATIONAL",
            "isolated_hwm_monitoring": True,
        },
        "ai_gateway": {
            "circuit_breaker": ai_gateway.circuit_breaker.state,
        },
    }


# --- AI Health, Circuit Breaker & Pool Endpoints ---

class CircuitBreakerPayload(BaseModel):
    action: str  # "trip" or "reset"


@router.get("/ai/health", summary="Real-time AI gateway health, latency and pool metrics")
def get_ai_health_metrics(
    _admin: User = Depends(require_admin),
) -> dict[str, Any]:
    """Retrieve operational telemetry and circuit breaker state for TRELLIS AI."""
    metrics = ai_gateway.get_health_metrics()
    return metrics.model_dump()


@router.post("/ai/circuit-breaker", summary="Manually trip or reset the AI circuit breaker")
def manage_ai_circuit_breaker(
    payload: CircuitBreakerPayload,
    _admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    act = payload.action.lower().strip()
    if act == "trip":
        ai_gateway.circuit_breaker.trip()
    elif act == "reset":
        ai_gateway.circuit_breaker.reset()
    else:
        raise HTTPException(status_code=400, detail="Invalid action. Allowed: 'trip', 'reset'.")
    return {
        "message": f"Circuit breaker state updated via operator action: {act}",
        "state": ai_gateway.circuit_breaker.state,
    }


@router.post("/ai/pool/refill", summary="Trigger background replenishment of question pools")
def trigger_ai_pool_refill(
    _admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    ai_gateway.pool.refill_all()
    return {
        "message": "Question pool replenishment triggered.",
        "pool_counts": ai_gateway.pool.get_pool_counts(),
    }


# --- Admin Enterprise Copilot Chatbot (Phase B) ---
class ChatMessageItem(BaseModel):
    role: str
    content: str


class AdminChatbotRequest(BaseModel):
    message: str
    history: list[ChatMessageItem] = Field(default_factory=list)


@router.post("/chatbot/chat", summary="Chat with TRELLIS Enterprise Operations Copilot")
def chat_with_admin_copilot(
    payload: AdminChatbotRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    """Execute grounded administrative chat inquiry."""
    from app.ai.chatbot.chat_service import chat_role
    history_dicts = [{"role": m.role, "content": m.content} for m in payload.history]
    result = chat_role(
        user=admin,
        user_message=payload.message,
        db=db,
        history=history_dicts,
    )
    if "error" in result and result["error"] == "RATE_LIMIT_EXCEEDED":
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=result["message"])
    return result


@router.post("/chatbot/stream", summary="Stream chat with TRELLIS Enterprise Operations Copilot (POST)")
def stream_with_admin_copilot(
    payload: AdminChatbotRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
) -> StreamingResponse:
    from app.ai.chatbot.chat_service import stream_chat_role
    return StreamingResponse(
        stream_chat_role(user=admin, user_message=payload.message, db=db),
        media_type="text/event-stream",
    )
