"""TRELLIS AI Practice, Dedication Scoring & Talent Spotlight Models."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, utc_now

if TYPE_CHECKING:
    from app.models.user import User


class PracticeSession(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Ungraded, optional self-directed practice session per field and difficulty."""

    __tablename__ = "practice_sessions"

    learner_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    field: Mapped[str] = mapped_column(String(128), index=True, nullable=False)  # Python, Java, SQL, DSA, etc.
    difficulty: Mapped[str] = mapped_column(String(32), default="MEDIUM", nullable=False)  # EASY, MEDIUM, HARD
    mode: Mapped[str] = mapped_column(String(32), default="MCQ", nullable=False)  # MCQ, CODING
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    learner: Mapped["User"] = relationship("User", foreign_keys=[learner_id])
    questions: Mapped[list["PracticeQuestion"]] = relationship(
        "PracticeQuestion", back_populates="session", cascade="all, delete-orphan"
    )


class PracticeQuestion(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """LLM-generated practice question, rigorously sandbox-verified before presentation."""

    __tablename__ = "practice_questions"

    session_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("practice_sessions.id", ondelete="CASCADE"), index=True, nullable=False
    )
    field: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(32), nullable=False)
    mode: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    question_data_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    reference_solution: Mapped[str | None] = mapped_column(Text, nullable=True)
    verified: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    session: Mapped["PracticeSession"] = relationship("PracticeSession", back_populates="questions")
    attempts: Mapped[list["PracticeAttempt"]] = relationship(
        "PracticeAttempt", back_populates="question", cascade="all, delete-orphan"
    )


class PracticeAttempt(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Learner's response attempt for an AI practice question with hints and explanations."""

    __tablename__ = "practice_attempts"

    question_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("practice_questions.id", ondelete="CASCADE"), index=True, nullable=False
    )
    learner_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    answer_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    hints_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    ai_feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Relationships
    question: Mapped["PracticeQuestion"] = relationship("PracticeQuestion", back_populates="attempts")
    learner: Mapped["User"] = relationship("User", foreign_keys=[learner_id])


class PracticeScore(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Continuously computed dedication & performance score per learner per field."""

    __tablename__ = "practice_scores"
    __table_args__ = (
        UniqueConstraint("learner_id", "field", name="uq_learner_practice_field"),
    )

    learner_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    field: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    active_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    streak_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    problems_attempted: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    problems_solved: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    acceptance_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    weighted_accuracy: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    dedication_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    last_practiced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    learner: Mapped["User"] = relationship("User", foreign_keys=[learner_id])


class TalentAlert(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Talent Spotlight notification generated when a learner crosses high-performance thresholds."""

    __tablename__ = "talent_alerts"

    learner_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    mentor_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    field: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    evidence_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), default="PENDING", nullable=False
    )  # PENDING, INVITED_TO_ASSESSMENT, INTERVIEW_SCHEDULED, RECOMMENDED_PROMOTION, DISMISSED
    action_taken: Mapped[str | None] = mapped_column(String(64), nullable=True)
    action_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    action_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    learner: Mapped["User"] = relationship("User", foreign_keys=[learner_id])
    mentor: Mapped["User"] = relationship("User", foreign_keys=[mentor_id])
    actions: Mapped[list["AlertAction"]] = relationship(
        "AlertAction", back_populates="alert", cascade="all, delete-orphan"
    )


class AlertAction(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Audit log of discrete mentor actions taken on a Talent Spotlight alert."""

    __tablename__ = "alert_actions"

    alert_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("talent_alerts.id", ondelete="CASCADE"), index=True, nullable=False
    )
    mentor_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    action_taken: Mapped[str] = mapped_column(String(64), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    action_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )

    # Relationships
    alert: Mapped["TalentAlert"] = relationship("TalentAlert", back_populates="actions")
    mentor: Mapped["User"] = relationship("User", foreign_keys=[mentor_id])
