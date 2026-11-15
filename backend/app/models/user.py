"""TRELLIS User Identity, Roles, Employment & Consent ORM Models."""

from datetime import date, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, Boolean, Date, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, utc_now

if TYPE_CHECKING:
    from app.models.tenancy import Organisation


class User(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Core user entity representing employees, trainers, managers, and administrators."""

    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("org_id", "email", name="uq_users_org_email"),)

    org_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organisations.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Per-employee cryptographic salt for Evidence Ledger pseudonymisation (DPDP Crypto-Shredding)
    pseudonym_salt: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # Climbing streak tracking
    streak_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    streak_freezes_remaining: Mapped[int] = mapped_column(Integer, default=2, nullable=False)
    last_active_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Preferences & Accessibility (Dyslexia font, theme, calm mode)
    preferences_json: Mapped[dict[str, Any] | None] = mapped_column(
        JSON, default=dict, nullable=True
    )

    # TOTP MFA (Required for LK_ADMIN & SUPER_ADMIN)
    totp_secret: Mapped[str | None] = mapped_column(String(64), nullable=True)
    totp_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recovery_codes_json: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    # Relationships
    organisation: Mapped["Organisation"] = relationship("Organisation", back_populates="users")
    employment_record: Mapped["EmploymentRecord | None"] = relationship(
        "EmploymentRecord",
        back_populates="user",
        uselist=False,
        foreign_keys="EmploymentRecord.user_id",
        lazy="selectin",
    )
    grants: Mapped[list["Grant"]] = relationship(
        "Grant",
        back_populates="user",
        foreign_keys="Grant.user_id",
        lazy="selectin",
    )
    consents: Mapped[list["Consent"]] = relationship(
        "Consent", back_populates="user", lazy="selectin"
    )


class EmploymentRecord(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Employment metadata, department, designation, and reporting hierarchy."""

    __tablename__ = "employment_records"
    __table_args__ = (
        UniqueConstraint("org_id", "employee_code", name="uq_employment_org_employee_code"),
    )

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    org_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organisations.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    employee_code: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    department: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    designation: Mapped[str] = mapped_column(String(128), nullable=False)
    reporting_line_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    hire_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(
        "User", back_populates="employment_record", foreign_keys=[user_id]
    )
    reporting_manager: Mapped["User | None"] = relationship(
        "User", foreign_keys=[reporting_line_id]
    )


class Role(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """System and domain roles matching the TRELLIS Role-Permission Matrix."""

    __tablename__ = "roles"

    code: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(String(512), nullable=True)
    is_system_role: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    grants: Mapped[list["Grant"]] = relationship("Grant", back_populates="role")


class Grant(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """User-to-Role assignments with optional expiry, approval references, and audit tracking."""

    __tablename__ = "grants"
    __table_args__ = (UniqueConstraint("user_id", "role_id", name="uq_grants_user_role"),)

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    role_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("roles.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    org_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organisations.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    granted_by_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    approval_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="grants", foreign_keys=[user_id])
    role: Mapped["Role"] = relationship("Role", back_populates="grants")
    granted_by: Mapped["User | None"] = relationship("User", foreign_keys=[granted_by_id])


class Consent(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """DPDP Consent Passport entity tracking purpose-specific consent and 1-click revocation."""

    __tablename__ = "consents"
    __table_args__ = (UniqueConstraint("user_id", "purpose_code", name="uq_consents_user_purpose"),)

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    org_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organisations.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    purpose_code: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), default="GRANTED", nullable=False
    )  # GRANTED, REVOKED
    granted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="consents")
