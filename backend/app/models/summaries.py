"""TRELLIS Pre-computed summary models for high-performance dashboards and metrics."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.assessments import Assessment
    from app.models.batches import Batch
    from app.models.user import User


class LearnerStats(Base, TimestampMixin):
    """Pre-aggregated performance statistics per learner."""

    __tablename__ = "learner_stats"

    learner_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    total_assessments_taken: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    average_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    median_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    streak_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    active_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    practice_total: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    practice_accuracy: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    attendance_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    coding_acceptance_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    velocity: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    trend_label: Mapped[str] = mapped_column(String(32), default="Steady", nullable=False)
    percentile: Mapped[float | None] = mapped_column(Float, nullable=True)
    risk_flag: Mapped[str | None] = mapped_column(String(64), nullable=True)
    risk_reasons_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    learner: Mapped["User"] = relationship("User", foreign_keys=[learner_id])


class AssessmentStats(Base, TimestampMixin):
    """Pre-aggregated metrics and distribution per assessment."""

    __tablename__ = "assessment_stats"

    assessment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("assessments.id", ondelete="CASCADE"), primary_key=True
    )
    assigned_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    started_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    submitted_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    graded_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    pass_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    mean_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    median_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    stdev_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    histogram_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    item_analysis_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    assessment: Mapped["Assessment"] = relationship("Assessment", foreign_keys=[assessment_id])


class BatchStats(Base, TimestampMixin):
    """Pre-aggregated cohort metrics per batch."""

    __tablename__ = "batch_stats"

    batch_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("batches.id", ondelete="CASCADE"), primary_key=True
    )
    learner_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    average_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    completion_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    practice_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    attendance_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    batch: Mapped["Batch"] = relationship("Batch", foreign_keys=[batch_id])


class TopicMastery(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Topic-level question accuracy tracking per learner."""

    __tablename__ = "topic_mastery"
    __table_args__ = (
        Index("ix_topic_mastery_learner_topic", "learner_id", "topic"),
    )

    learner_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    topic: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    total_questions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    correct_questions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    accuracy: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    learner: Mapped["User"] = relationship("User", foreign_keys=[learner_id])
