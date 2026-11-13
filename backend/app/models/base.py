"""TRELLIS Base ORM Models, Mixins & Meta Configuration."""

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import DateTime, String, event, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


def utc_now() -> datetime:
    """Return current UTC datetime with timezone awareness."""
    return datetime.now(UTC)


class Base(DeclarativeBase):
    """Declarative Base class for all TRELLIS database entities."""

    # Set by subclasses for immutability enforcement
    __immutable__: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert model instance fields into a dictionary."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class UUIDPrimaryKeyMixin:
    """Mixin providing standardized 36-character UUID primary key."""

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        sort_order=-100,
    )


class TimestampMixin:
    """Mixin providing UTC created_at and updated_at tracking."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )


class ImmutableMixin:
    """Mixin for append-only audit and ledger tables."""

    __immutable__: bool = True

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        sort_order=-100,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )


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


# Automatically bind immutability enforcement to all ORM sessions
event.listen(Session, "before_flush", enforce_immutability_before_flush)
