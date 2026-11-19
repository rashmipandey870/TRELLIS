"""TRELLIS Global System Settings & Alert Threshold Configurations."""

from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.user import User


class SystemSetting(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Dynamic platform configuration (e.g. Talent Spotlight thresholds, cooldowns)."""

    __tablename__ = "system_settings"

    key: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    value_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    updated_by_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    updated_by: Mapped["User | None"] = relationship("User")
