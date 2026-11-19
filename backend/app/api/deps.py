"""TRELLIS FastAPI Request Dependencies & Authentication Guards."""

import contextlib
from collections.abc import Generator
from typing import Any

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decode_access_token
from app.core.uow import UnitOfWork
from app.models import Base, User

# Database session dependency
# Note: For SQLite/MySQL runtime sessions
_sync_engine = None


def get_sync_engine() -> Any:
    """Return synchronous database engine."""
    global _sync_engine
    if _sync_engine is None:
        db_url = settings.DATABASE_URL.replace("mysql+asyncmy://", "mysql+pymysql://")
        if db_url.startswith("sqlite+aiosqlite://"):
            db_url = db_url.replace("sqlite+aiosqlite://", "sqlite://", 1)
        if not db_url:
            db_url = "sqlite:///:memory:"
        try:
            _sync_engine = create_engine(db_url, pool_pre_ping=True)
            Base.metadata.create_all(_sync_engine)
        except Exception:
            _sync_engine = create_engine("sqlite:///:memory:")
            Base.metadata.create_all(_sync_engine)
    return _sync_engine


def get_db() -> Generator[Session, None, None]:
    """Provide synchronous database session for request lifecycle."""
    engine = get_sync_engine()
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


security_bearer = HTTPBearer(auto_error=False)


def get_uow(
    request: Request,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials | None = Depends(security_bearer),
) -> Generator[UnitOfWork, None, None]:
    """Provide UnitOfWork with in-transaction audit logging for mutating endpoints."""
    claims = None
    if credentials and credentials.credentials:
        with contextlib.suppress(Exception):
            claims = decode_access_token(credentials.credentials)
    uow = UnitOfWork(session=db, request=request, claims=claims)
    try:
        yield uow
    except Exception:
        uow.rollback()
        raise


def get_current_user_claims(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_bearer),
) -> dict[str, Any]:
    """Validate Bearer JWT access token and return token payload claims."""
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        claims = decode_access_token(credentials.credentials)
        return claims
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired access token: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def get_current_user(
    claims: dict[str, Any] = Depends(get_current_user_claims),
    db: Session = Depends(get_db),
) -> User:
    """Retrieve active authenticated User entity."""
    user_id = claims.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token subject invalid.",
        )

    user = db.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or account is deactivated.",
        )

    return user


def require_role(*roles: str) -> Any:
    """Enforce that the authenticated user possesses one of the allowed roles (ADMIN, MENTOR, LEARNER)."""

    def dependency(
        current_user: User = Depends(get_current_user),
        claims: dict[str, Any] = Depends(get_current_user_claims),
    ) -> User:
        user_roles = set()
        if current_user.role:
            user_roles.add(current_user.role.upper())
        for r in claims.get("roles", []):
            user_roles.add(str(r).upper())
        if hasattr(current_user, "grants") and current_user.grants:
            for g in current_user.grants:
                if g.role and g.role.code:
                    user_roles.add(g.role.code.upper())

        # Map legacy role names if present
        if "SUPER_ADMIN" in user_roles or "LK_ADMIN" in user_roles:
            user_roles.add("ADMIN")
        if "TRAINER" in user_roles or "TRAINER_MENTOR" in user_roles:
            user_roles.add("MENTOR")
        if "EMPLOYEE" in user_roles:
            user_roles.add("LEARNER")

        allowed = {r.upper() for r in roles}
        if not user_roles.intersection(allowed):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: Action requires one of {allowed} role(s).",
            )
        return current_user

    return dependency


require_admin = require_role("ADMIN")
require_mentor = require_role("MENTOR")
require_learner = require_role("LEARNER")
require_mentor_or_admin = require_role("MENTOR", "ADMIN")


def verify_mentor_learner_access(mentor: User, learner_id: str, db: Session) -> bool:
    """Verify that a mentor is assigned to the learner, or allow if user is an ADMIN."""
    if (mentor.role or "").upper() == "ADMIN":
        return True
    from app.models.batches import MentorLearnerAssignment

    from sqlalchemy import select
    assignment = db.execute(
        select(MentorLearnerAssignment).where(
            MentorLearnerAssignment.mentor_id == mentor.id,
            MentorLearnerAssignment.learner_id == learner_id,
        )
    ).scalar_one_or_none()
    return assignment is not None

