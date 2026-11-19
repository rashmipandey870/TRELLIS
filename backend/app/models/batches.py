"""TRELLIS Batch & Mentor-Learner Assignment Models."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, utc_now

if TYPE_CHECKING:
    from app.models.user import User


class Batch(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Learning Batch grouping learners under assigned mentors."""

    __tablename__ = "batches"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    field: Mapped[str] = mapped_column(String(128), default="General", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    max_learners: Mapped[int] = mapped_column(Integer, default=50, nullable=False)
    org_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("organisations.id", ondelete="RESTRICT"), nullable=True
    )
    cohort_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("cohorts.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    assignments: Mapped[list["MentorLearnerAssignment"]] = relationship(
        "MentorLearnerAssignment", back_populates="batch", cascade="all, delete-orphan"
    )
    cohort: Mapped[Any | None] = relationship("Cohort", back_populates="batches")
    enrolments: Mapped[list[Any]] = relationship("Enrolment", back_populates="batch")


class MentorLearnerAssignment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Explicit mapping assigning a Mentor to a Learner within an optional Batch."""

    __tablename__ = "mentor_learner_assignments"
    __table_args__ = (
        UniqueConstraint("mentor_id", "learner_id", name="uq_mentor_learner"),
    )

    mentor_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    learner_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    batch_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("batches.id", ondelete="SET NULL"), index=True, nullable=True
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )

    # Relationships
    mentor: Mapped["User"] = relationship("User", foreign_keys=[mentor_id])
    learner: Mapped["User"] = relationship("User", foreign_keys=[learner_id])
    batch: Mapped["Batch | None"] = relationship("Batch", back_populates="assignments")
