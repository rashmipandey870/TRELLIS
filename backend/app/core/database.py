"""TRELLIS Database Engine, Session Factory & Immutability Enforcement."""

from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy import event, inspect
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session

from app.core.config import settings

# Configure Async Engine
_db_url = settings.DATABASE_URL or "sqlite+aiosqlite:///:memory:"
engine: AsyncEngine = create_async_engine(
    _db_url,
    echo=settings.LOG_LEVEL.upper() == "DEBUG",
    pool_pre_ping=True,
    **({"pool_size": 10, "max_overflow": 20} if "sqlite" not in _db_url else {}),
)

# Async Session Factory
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency providing an async database session per request."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def enforce_immutability_before_flush(session: Session, flush_context: Any, instances: Any) -> None:
    """Session event listener enforcing append-only immutability at the application ORM level.

    Strictly forbids any UPDATE or DELETE operations on entities marked with __immutable__ = True.
    """
    for obj in session.dirty:
        if getattr(obj, "__immutable__", False):
            # Check if any column data actually changed
            state = inspect(obj)
            if state and any(attr.history.has_changes() for attr in state.attrs):
                raise PermissionError(
                    f"IMMUTABILITY_VIOLATION: Table '{obj.__tablename__}' is append-only. "
                    f"UPDATE operations are strictly forbidden on record id '{getattr(obj, 'id', 'unknown')}'."
                )

    for obj in session.deleted:
        if getattr(obj, "__immutable__", False):
            raise PermissionError(
                f"IMMUTABILITY_VIOLATION: Table '{obj.__tablename__}' is append-only. "
                f"DELETE operations are strictly forbidden on record id '{getattr(obj, 'id', 'unknown')}'."
            )


# Register immutability event listeners
event.listen(Session, "before_flush", enforce_immutability_before_flush)
