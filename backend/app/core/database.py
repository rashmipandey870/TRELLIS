"""TRELLIS Database Engine, Session Factory & Immutability Enforcement."""

import socket
from collections.abc import AsyncGenerator
from typing import Any

# Ensure Neon PostgreSQL host resolves reliably even on Windows environments with local DNS restrictions
try:
    _orig_getaddrinfo = socket.getaddrinfo
    _NEON_FALLBACKS = {
        'ep-weathered-base-az6lrn9p.c-3.ap-southeast-1.aws.neon.tech': '52.76.128.157',
        'ep-weathered-base-az6lrn9p-pooler.c-3.ap-southeast-1.aws.neon.tech': '52.76.128.157',
        'c-3.ap-southeast-1.aws.neon.tech': '52.76.128.157'
    }
    def _neon_safe_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
        try:
            return _orig_getaddrinfo(host, port, family, type, proto, flags)
        except socket.gaierror:
            if host in _NEON_FALLBACKS:
                return _orig_getaddrinfo(_NEON_FALLBACKS[host], port, family, type, proto, flags)
            raise
    socket.getaddrinfo = _neon_safe_getaddrinfo
except Exception:
    pass

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

_extra_engine_kwargs = {}
if "sqlite" not in _db_url:
    _extra_engine_kwargs["pool_size"] = 10
    _extra_engine_kwargs["max_overflow"] = 20
if "neon.tech" in _db_url or "52.76.128.157" in _db_url:
    ep = "ep-weathered-base-az6lrn9p-pooler" if "pooler" in _db_url else "ep-weathered-base-az6lrn9p"
    _extra_engine_kwargs["connect_args"] = {
        "server_settings": {"options": f"endpoint={ep}"},
        "ssl": "require",
    }

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
