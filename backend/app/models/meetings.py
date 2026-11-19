"""TRELLIS Meeting Scheduling & Attendance Models."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, utc_now

if TYPE_CHECKING:
    from app.models.batches import Batch
    from app.models.user import User


class Meeting(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Live/virtual meeting scheduled by a Mentor for their learners/batches."""

    __tablename__ = "meetings"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    meeting_date: Mapped[str] = mapped_column(String(32), nullable=False)  # YYYY-MM-DD
    start_time: Mapped[str] = mapped_column(String(32), nullable=False)  # HH:MM
    end_time: Mapped[str] = mapped_column(String(32), nullable=False)  # HH:MM
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    meeting_link: Mapped[str] = mapped_column(String(512), nullable=False)  # Validated Teams/Zoom/Meet URL
    mentor_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    batch_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("batches.id", ondelete="SET NULL"), index=True, nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(32), default="SCHEDULED", nullable=False
    )  # SCHEDULED, COMPLETED, CANCELLED

    # Relationships
    mentor: Mapped["User"] = relationship("User", foreign_keys=[mentor_id])
    batch: Mapped["Batch | None"] = relationship("Batch")
    audiences: Mapped[list["MeetingAudience"]] = relationship(
        "MeetingAudience", back_populates="meeting", cascade="all, delete-orphan"
    )
    attendances: Mapped[list["MeetingAttendance"]] = relationship(
        "MeetingAttendance", back_populates="meeting", cascade="all, delete-orphan"
    )


class MeetingAudience(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Specific audience assignment for a meeting (learner or batch)."""

    __tablename__ = "meeting_audience"

    meeting_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("meetings.id", ondelete="CASCADE"), index=True, nullable=False
    )
    learner_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=True
    )
    batch_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("batches.id", ondelete="CASCADE"), index=True, nullable=True
    )

    # Relationships
    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="audiences")
    learner: Mapped["User | None"] = relationship("User")


class MeetingAttendance(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Attendance record marked by the mentor after a meeting."""

    __tablename__ = "meeting_attendance"
    __table_args__ = (
        UniqueConstraint("meeting_id", "learner_id", name="uq_meeting_attendance"),
    )

    meeting_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("meetings.id", ondelete="CASCADE"), index=True, nullable=False
    )
    learner_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    attended: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    marked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    remarks: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # Relationships
    meeting: Mapped["Meeting"] = relationship("Meeting", back_populates="attendances")
    learner: Mapped["User"] = relationship("User")
