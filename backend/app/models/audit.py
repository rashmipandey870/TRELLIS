"""TRELLIS Immutable Audit Logging & Access Receipts ORM Models."""

from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, ImmutableMixin, utc_now


class AuditLog(Base, ImmutableMixin):
    """Immutable audit log recording every system state mutation.

    Database invariant: No UPDATE or DELETE privileges are granted on this table.
    """

    __tablename__ = "audit_log"
    __immutable__ = True

    org_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organisations.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    actor_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), index=True, nullable=True
    )
    action: Mapped[str] = mapped_column(
        String(64), index=True, nullable=False
    )  # create, update, delete, login, etc.
    resource: Mapped[str] = mapped_column(
        String(64), index=True, nullable=False
    )  # users, grants, consents, etc.
    resource_id: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)

    # State capture for non-repudiation
    before_state_json: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    after_state_json: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # Context & Provenance
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(512), nullable=True)
    approval_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    request_id: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)
    reason: Mapped[str | None] = mapped_column(String(512), nullable=True)

    __table_args__ = (
        Index("ix_audit_org_created", "org_id", "created_at"),
        Index("ix_audit_actor_action", "actor_id", "action"),
    )


class AccessReceipt(Base, ImmutableMixin):
    """Immutable access receipt recording cross-user reads of personal/growth data.

    Database invariant: No UPDATE or DELETE privileges are granted on this table.
    """

    __tablename__ = "access_receipts"
    __immutable__ = True

    org_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organisations.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    accessor_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    subject_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    resource_type: Mapped[str] = mapped_column(
        String(64), index=True, nullable=False
    )  # growth_ring, skills_profile, etc.
    resource_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    purpose: Mapped[str] = mapped_column(String(128), nullable=False)
    read_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )

    __table_args__ = (
        Index("ix_receipts_subject_read", "subject_id", "read_at"),
        Index("ix_receipts_accessor_read", "accessor_id", "read_at"),
    )
