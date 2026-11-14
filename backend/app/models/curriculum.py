"""TRELLIS Curriculum & Pathways ORM Models (Slice 1.6)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.user import User


class Pathway(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Learning pathway composing courses into an end-to-end competency journey."""

    __tablename__ = "pathways"

    org_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organisations.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    author_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    target_role_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    estimated_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    is_first_90_days: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    author: Mapped[User] = relationship("User", foreign_keys=[author_id])
    courses: Mapped[list[Course]] = relationship(
        "Course",
        back_populates="pathway",
        cascade="all, delete-orphan",
        order_by="Course.sequence_order",
    )
    enrolments: Mapped[list[Enrolment]] = relationship(
        "Enrolment", back_populates="pathway", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("org_id", "code", name="uq_pathways_org_code"),
        Index("ix_pathways_is_published", "is_published"),
        Index("ix_pathways_first_90_days", "is_first_90_days"),
    )


class Course(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Individual course within a pathway, forming a prerequisite DAG."""

    __tablename__ = "courses"

    org_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organisations.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    pathway_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("pathways.id", ondelete="CASCADE"), index=True, nullable=False
    )
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sequence_order: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    prerequisite_course_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("courses.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    pathway: Mapped[Pathway] = relationship("Pathway", back_populates="courses")
    prerequisite: Mapped[Course | None] = relationship("Course", remote_side="Course.id")
    modules: Mapped[list[Module]] = relationship(
        "Module",
        back_populates="course",
        cascade="all, delete-orphan",
        order_by="Module.sequence_order",
    )

    __table_args__ = (UniqueConstraint("pathway_id", "code", name="uq_courses_pathway_code"),)


class Module(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Atomic instructional module (Lesson, Lab, Assessment, Reflection)."""

    __tablename__ = "modules"

    org_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organisations.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    course_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("courses.id", ondelete="CASCADE"), index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    module_type: Mapped[str] = mapped_column(
        String(64), default="LESSON", nullable=False
    )  # LESSON, LAB, ASSESSMENT, REFLECTION
    sequence_order: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    content_json: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # Relationships
    course: Mapped[Course] = relationship("Course", back_populates="modules")


class Cohort(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Learning cohort grouping employees under a Trainer/Mentor."""

    __tablename__ = "cohorts"

    org_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organisations.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    pathway_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("pathways.id", ondelete="SET NULL"), nullable=True
    )
    trainer_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    start_date: Mapped[Any | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[Any | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    batches: Mapped[list[Batch]] = relationship(
        "Batch", back_populates="cohort", cascade="all, delete-orphan"
    )
    enrolments: Mapped[list[Enrolment]] = relationship("Enrolment", back_populates="cohort")

    __table_args__ = (UniqueConstraint("org_id", "code", name="uq_cohorts_org_code"),)


class Batch(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Sub-cohort grouping for practical workshops and labs."""

    __tablename__ = "batches"

    org_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organisations.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    cohort_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("cohorts.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    max_learners: Mapped[int] = mapped_column(Integer, default=30, nullable=False)

    # Relationships
    cohort: Mapped[Cohort] = relationship("Cohort", back_populates="batches")
    enrolments: Mapped[list[Enrolment]] = relationship("Enrolment", back_populates="batch")


class Enrolment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Employee enrolment and continuous progress record in a Pathway."""

    __tablename__ = "enrolments"

    org_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organisations.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    pathway_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("pathways.id", ondelete="CASCADE"), index=True, nullable=False
    )
    cohort_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("cohorts.id", ondelete="SET NULL"), nullable=True
    )
    batch_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("batches.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(36), default="ENROLLED", nullable=False
    )  # ENROLLED, IN_PROGRESS, COMPLETED, DROPPED
    progress_percent: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    completed_at: Mapped[Any | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    user: Mapped[User] = relationship("User")
    pathway: Mapped[Pathway] = relationship("Pathway", back_populates="enrolments")
    cohort: Mapped[Cohort | None] = relationship("Cohort", back_populates="enrolments")
    batch: Mapped[Batch | None] = relationship("Batch", back_populates="enrolments")

    __table_args__ = (
        UniqueConstraint("user_id", "pathway_id", name="uq_enrolments_user_pathway"),
        Index("ix_enrolments_user_status", "user_id", "status"),
    )
