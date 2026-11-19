"""TRELLIS Mentor Feedback & Review Remarks Models."""

from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.assessments import Assessment
    from app.models.meetings import Meeting
    from app.models.user import User


class MentorRemark(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Structured qualitative remarks and 1:1 notes given by a Mentor for a Learner."""

    __tablename__ = "mentor_remarks"

    mentor_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    learner_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    assessment_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("assessments.id", ondelete="SET NULL"), index=True, nullable=True
    )
    meeting_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("meetings.id", ondelete="SET NULL"), index=True, nullable=True
    )
    remark_text: Mapped[str] = mapped_column(Text, nullable=False)
    visibility: Mapped[str] = mapped_column(
        String(32), default="LEARNER_AND_ADMIN", nullable=False
    )  # LEARNER_AND_ADMIN, ADMIN_ONLY

    # Relationships
    mentor: Mapped["User"] = relationship("User", foreign_keys=[mentor_id])
    learner: Mapped["User"] = relationship("User", foreign_keys=[learner_id])
    assessment: Mapped["Assessment | None"] = relationship("Assessment")
    meeting: Mapped["Meeting | None"] = relationship("Meeting")
