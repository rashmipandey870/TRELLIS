"""TRELLIS FastAPI Request Dependencies & Authentication Guards."""

import contextlib
import os
from collections.abc import Generator
from pathlib import Path
from typing import Any

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decode_access_token
from app.core.uow import UnitOfWork
from app.models import Base, User

# Database session dependency
# Note: For SQLite/MySQL runtime sessions
_sync_engine = None


def warmup_database(engine: Any, max_retries: int = 3, initial_delay: float = 0.5) -> None:
    """Warm up database connection with retry backoff for serverless/cold-start databases (e.g. Neon)."""
    import time
    from sqlalchemy import text
    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except Exception:
            if attempt == max_retries:
                raise
            time.sleep(initial_delay * (2 ** (attempt - 1)))


def get_sync_engine() -> Any:
    """Return synchronous database engine.
    
    Alembic migrations are the sole schema source. Base.metadata.create_all and silent fallbacks are removed.
    Configured with connection pooling, pool_pre_ping, pool_recycle, and Neon sslmode support.
    """
    global _sync_engine
    if _sync_engine is None:
        db_url = settings.DATABASE_URL or os.environ.get("DATABASE_URL")
        if not db_url:
            repo_db = Path(__file__).resolve().parent.parent.parent.parent / "trellis_demo.db"
            backend_db = Path(__file__).resolve().parent.parent.parent / "trellis_demo.db"
            resolved_db = repo_db if repo_db.exists() else backend_db
            db_url = f"sqlite:///{resolved_db.as_posix()}"

        if db_url.startswith("mysql+asyncmy://"):
            db_url = db_url.replace("mysql+asyncmy://", "mysql+pymysql://", 1)
        elif db_url.startswith("sqlite+aiosqlite://"):
            db_url = db_url.replace("sqlite+aiosqlite://", "sqlite://", 1)
        elif db_url.startswith("postgresql+asyncpg://"):
            db_url = db_url.replace("postgresql+asyncpg://", "postgresql+psycopg2://", 1)
        elif db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif db_url.startswith("postgresql://") and not db_url.startswith("postgresql+"):
            db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

        engine_kwargs: dict[str, Any] = {
            "pool_pre_ping": True,
        }
        if "sqlite" in db_url:
            engine_kwargs["connect_args"] = {"timeout": 30.0, "check_same_thread": False}
        else:
            engine_kwargs.update({
                "pool_size": 10,
                "max_overflow": 20,
                "pool_recycle": 45,
                "pool_timeout": 15,
            })
            if "postgresql" in db_url or "postgres" in db_url:
                connect_args: dict[str, Any] = {
                    "connect_timeout": 10,
                    "keepalives": 1,
                    "keepalives_idle": 5,
                    "keepalives_interval": 2,
                    "keepalives_count": 2,
                }
                if "sslmode" not in db_url:
                    connect_args["sslmode"] = "require"
                if "neon.tech" in db_url or "52.76.128.157" in db_url or "13.251.213.89" in db_url:
                    ep = "ep-weathered-base-az6lrn9p-pooler" if "pooler" in db_url else "ep-weathered-base-az6lrn9p"
                    connect_args["options"] = f"endpoint={ep}"
                    connect_args["hostaddr"] = "13.251.213.89"
                engine_kwargs["connect_args"] = connect_args

        _sync_engine = create_engine(db_url, **engine_kwargs)
        if "sqlite" in db_url:
            @event.listens_for(_sync_engine, "connect")
            def _set_sqlite_pragma(dbapi_connection, connection_record):
                try:
                    cursor = dbapi_connection.cursor()
                    cursor.execute("PRAGMA journal_mode=WAL")
                    cursor.execute("PRAGMA busy_timeout=30000")
                    cursor.close()
                except Exception:
                    pass
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
    request: Request,
    claims: dict[str, Any] = Depends(get_current_user_claims),
    db: Session = Depends(get_db),
) -> User:
    """Retrieve active authenticated User entity, loaded once per request and cached on request.state."""
    cached_user = getattr(request.state, "current_user", None)
    user_id = claims.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token subject invalid.",
        )

    if cached_user and getattr(cached_user, "id", None) == user_id:
        user = cached_user
    else:
        user = db.get(User, user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or account is deactivated.",
            )
        request.state.current_user = user

    # Invariant: Enforce password change at initial login
    if getattr(user, "must_change_password", False):
        path = request.url.path
        allowed_paths = {"/api/v1/auth/change-password", "/api/v1/auth/logout", "/api/v1/auth/me"}
        if path not in allowed_paths:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="MUST_CHANGE_PASSWORD: You must update your temporary password before accessing platform resources.",
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

