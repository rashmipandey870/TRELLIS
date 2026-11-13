"""TRELLIS Multi-Tenancy ORM Models."""

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.user import User


class Organisation(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Organisation entity representing tenant boundary for multi-tenancy logical isolation."""

    __tablename__ = "organisations"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="ACTIVE", nullable=False)

    # Relationships
    users: Mapped[list["User"]] = relationship(
        "User", back_populates="organisation", lazy="selectin"
    )
