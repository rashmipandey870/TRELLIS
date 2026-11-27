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
if "asyncpg" in _db_url and "?" in _db_url:
    _base_url, _query = _db_url.split("?", 1)
    _query_params = [p for p in _query.split("&") if not p.startswith("sslmode=")]
    _db_url = f"{_base_url}?{'&'.join(_query_params)}" if _query_params else _base_url

_extra_engine_kwargs: dict[str, Any] = {}
if "sqlite" not in _db_url:
    _extra_engine_kwargs["pool_size"] = 15
    _extra_engine_kwargs["max_overflow"] = 25
    _extra_engine_kwargs["pool_recycle"] = 300
    _extra_engine_kwargs["pool_timeout"] = 10

if "pooler" in _db_url or "pgbouncer" in _db_url or "neon.tech" in _db_url:
    # Transaction-pooled endpoints (e.g. PgBouncer / Neon pooler) require statement_cache_size=0
    _extra_engine_kwargs["connect_args"] = {
        "statement_cache_size": 0,
        "command_timeout": 15,
    }
    if "ssl" not in _extra_engine_kwargs["connect_args"] and "localhost" not in _db_url and "127.0.0.1" not in _db_url:
        _extra_engine_kwargs["connect_args"]["ssl"] = "require"

engine: AsyncEngine = create_async_engine(
    _db_url,
    echo=settings.LOG_LEVEL.upper() == "DEBUG",
    pool_pre_ping=True,
    **_extra_engine_kwargs,
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
