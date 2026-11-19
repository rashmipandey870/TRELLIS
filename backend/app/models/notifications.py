"""TRELLIS In-App Notifications & Audit Trail Models."""

from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.user import User


class Notification(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """In-app notifications for meetings, assessments, and Talent Spotlight alerts."""

    __tablename__ = "notifications"

    recipient_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    sender_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), index=True, nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    notification_type: Mapped[str] = mapped_column(
        String(64), default="SYSTEM", nullable=False
    )  # MEETING, ASSESSMENT, TALENT_ALERT, SYSTEM
    link: Mapped[str | None] = mapped_column(String(512), nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    recipient: Mapped["User"] = relationship("User", foreign_keys=[recipient_id])
    sender: Mapped["User | None"] = relationship("User", foreign_keys=[sender_id])
