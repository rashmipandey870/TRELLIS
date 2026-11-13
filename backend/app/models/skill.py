"""TRELLIS Skills Taxonomy & Role Benchmarks ORM Models."""

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Skill(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Core skill taxonomy node."""

    __tablename__ = "skills"
    __table_args__ = (UniqueConstraint("org_id", "code", name="uq_skills_org_code"),)

    org_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organisations.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    code: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(
        String(64), index=True, nullable=False
    )  # TECHNICAL, DOMAIN, BEHAVIOURAL
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    decay_half_life_days: Mapped[int] = mapped_column(Integer, default=365, nullable=False)

    # Relationships
    levels: Mapped[list["SkillLevel"]] = relationship(
        "SkillLevel", back_populates="skill", cascade="all, delete-orphan", lazy="selectin"
    )


class SkillLevel(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Rubrics and performance descriptors per skill level (1 to 5)."""

    __tablename__ = "skill_levels"
    __table_args__ = (
        UniqueConstraint("skill_id", "level_number", name="uq_skill_levels_skill_level"),
    )

    skill_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("skills.id", ondelete="CASCADE"), index=True, nullable=False
    )
    level_number: Mapped[int] = mapped_column(Integer, nullable=False)  # 1 to 5
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    rubric_text: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationships
    skill: Mapped["Skill"] = relationship("Skill", back_populates="levels")


class SkillEdge(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Graph edges connecting prerequisite, complementary, and specialization skills."""

    __tablename__ = "skill_edges"
    __table_args__ = (
        UniqueConstraint(
            "source_skill_id", "target_skill_id", "relationship_type", name="uq_skill_edges_pair"
        ),
    )

    org_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organisations.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    source_skill_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("skills.id", ondelete="CASCADE"), index=True, nullable=False
    )
    target_skill_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("skills.id", ondelete="CASCADE"), index=True, nullable=False
    )
    relationship_type: Mapped[str] = mapped_column(
        String(32), nullable=False
    )  # PREREQUISITE, COMPLEMENTARY, SPECIALIZATION


class RoleRequirement(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Skill benchmarks required for specific role job bands."""

    __tablename__ = "role_requirements"
    __table_args__ = (
        UniqueConstraint("org_id", "role_code", "skill_id", name="uq_role_requirements_role_skill"),
    )

    org_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organisations.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    role_code: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    skill_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("skills.id", ondelete="CASCADE"), index=True, nullable=False
    )
    target_level: Mapped[int] = mapped_column(Integer, nullable=False)  # 1 to 5
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    skill: Mapped["Skill"] = relationship("Skill")
