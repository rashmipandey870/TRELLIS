"""TRELLIS FastAPI Request Dependencies & Authentication Guards."""

from collections.abc import Generator
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decode_access_token
from app.models import Base, User

# Database session dependency
# Note: For SQLite/MySQL runtime sessions
_sync_engine = None


def get_sync_engine() -> Any:
    """Return synchronous database engine."""
    global _sync_engine
    if _sync_engine is None:
        db_url = settings.DATABASE_URL.replace("mysql+asyncmy://", "mysql+pymysql://")
        if "mysql" not in db_url:
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
