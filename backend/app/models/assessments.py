"""TRELLIS Assessment Engine, Question Bank & Coding Problem Models."""

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
    from app.models.batches import Batch
    from app.models.user import User


class QuestionBank(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Reusable repository of vetted assessment questions."""

    __tablename__ = "question_bank"

    author_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(String(32), nullable=False)  # MCQ, CODING, SQL, SHORT_ANSWER, SCENARIO, COMMUNICATION, FILE_UPLOAD, LIKERT
    category: Mapped[str] = mapped_column(String(64), default="Technical Knowledge", server_default="Technical Knowledge", nullable=False)
    field: Mapped[str] = mapped_column(String(128), index=True, nullable=False)  # Python, Java, DSA, Web, etc.
    topic: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    difficulty: Mapped[str] = mapped_column(String(32), default="MEDIUM", nullable=False)  # EASY, MEDIUM, HARD
    tags_json: Mapped[list[str] | None] = mapped_column(JSON, default=list, nullable=True)
    rubric_json: Mapped[dict[str, Any] | None] = mapped_column(JSON, default=dict, nullable=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    author: Mapped["User"] = relationship("User", foreign_keys=[author_id])
    options: Mapped[list["McqOption"]] = relationship(
        "McqOption", back_populates="question", cascade="all, delete-orphan"
    )
    coding_problem: Mapped["CodingProblem | None"] = relationship(
        "CodingProblem", back_populates="bank_question", uselist=False, cascade="all, delete-orphan"
    )


class McqOption(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Multiple choice options for an MCQ question."""

    __tablename__ = "mcq_options"

    question_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("question_bank.id", ondelete="CASCADE"), index=True, nullable=False
    )
    option_text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    sequence_order: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Relationships
    question: Mapped["QuestionBank"] = relationship("QuestionBank", back_populates="options")


class CodingProblem(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """LeetCode-style coding problem with starter code and test specifications."""

    __tablename__ = "coding_problems"

    bank_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("question_bank.id", ondelete="CASCADE"), index=True, nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    constraints: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty: Mapped[str] = mapped_column(String(32), default="MEDIUM", nullable=False)
    field: Mapped[str] = mapped_column(String(128), default="General", nullable=False)
    marks: Mapped[float] = mapped_column(Float, default=10.0, nullable=False)
    time_limit_ms: Mapped[int] = mapped_column(Integer, default=2000, nullable=False)
    memory_limit_mb: Mapped[int] = mapped_column(Integer, default=256, nullable=False)
    examples_json: Mapped[list[dict[str, Any]] | None] = mapped_column(JSON, default=list, nullable=True)
    starter_code_json: Mapped[dict[str, str] | None] = mapped_column(JSON, default=dict, nullable=True)
    reference_solution: Mapped[str | None] = mapped_column(Text, nullable=True)
    problem_type: Mapped[str] = mapped_column(String(32), default="CODING", nullable=False)
    schema_ddl: Mapped[str | None] = mapped_column(Text, nullable=True)
    entry_point: Mapped[str | None] = mapped_column(String(128), nullable=True)
    argument_schema: Mapped[list[dict[str, Any]] | None] = mapped_column(JSON, default=list, nullable=True)
    wrong_stub: Mapped[str | None] = mapped_column(Text, nullable=True)
    complexity_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    bank_question: Mapped["QuestionBank | None"] = relationship("QuestionBank", back_populates="coding_problem")
    test_cases: Mapped[list["TestCase"]] = relationship(
        "TestCase", back_populates="problem", cascade="all, delete-orphan"
    )


class TestCase(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Test case for automated code evaluation."""

    __test__ = False
    __tablename__ = "test_cases"

    problem_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("coding_problems.id", ondelete="CASCADE"), index=True, nullable=False
    )
    input_data: Mapped[str] = mapped_column(Text, nullable=False)
    expected_output: Mapped[str] = mapped_column(Text, nullable=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    time_limit_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    memory_limit_mb: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Relationships
    problem: Mapped["CodingProblem"] = relationship("CodingProblem", back_populates="test_cases")


class Assessment(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Formal assessment created and managed by Mentors."""

    __tablename__ = "assessments"

    mentor_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    batch_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("batches.id", ondelete="SET NULL"), index=True, nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    field: Mapped[str] = mapped_column(String(128), default="General", nullable=False)
    instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    passing_score: Mapped[float] = mapped_column(Float, default=60.0, nullable=False)
    start_window: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_window: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(
        String(32), default="DRAFT", nullable=False
    )  # DRAFT, PUBLISHED, ARCHIVED
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    show_explanations: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    mask_hidden_cases: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    mentor: Mapped["User"] = relationship("User", foreign_keys=[mentor_id])
    batch: Mapped["Batch | None"] = relationship("Batch")
    questions: Mapped[list["AssessmentQuestion"]] = relationship(
        "AssessmentQuestion", back_populates="assessment", cascade="all, delete-orphan", order_by="AssessmentQuestion.sequence_order"
    )
    attempts: Mapped[list["AssessmentAttempt"]] = relationship(
        "AssessmentAttempt", back_populates="assessment", cascade="all, delete-orphan"
    )
    audience_learners: Mapped[list["AssessmentAudience"]] = relationship(
        "AssessmentAudience", back_populates="assessment", cascade="all, delete-orphan"
    )


class AssessmentAudience(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Specific learners assigned to an assessment outside or within batches."""

    __tablename__ = "assessment_audience"

    assessment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("assessments.id", ondelete="CASCADE"), index=True, nullable=False
    )
    learner_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )

    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="audience_learners")
    learner: Mapped["User"] = relationship("User")


class AssessmentQuestion(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Questions linked to a specific assessment with custom order and weight."""

    __tablename__ = "assessment_questions"

    assessment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("assessments.id", ondelete="CASCADE"), index=True, nullable=False
    )
    bank_question_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("question_bank.id", ondelete="CASCADE"), index=True, nullable=False
    )
    sequence_order: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    marks: Mapped[float] = mapped_column(Float, default=5.0, nullable=False)

    # Relationships
    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="questions")
    question: Mapped["QuestionBank"] = relationship("QuestionBank")


class AssessmentAttempt(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Learner's attempt at an assessment, tracking duration, autosave state, and score."""

    __tablename__ = "assessment_attempts"

    assessment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("assessments.id", ondelete="CASCADE"), index=True, nullable=False
    )
    learner_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    submit_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_marks: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), default="IN_PROGRESS", nullable=False
    )  # IN_PROGRESS, SUBMITTED, EXPIRED
    tab_switch_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    autosave_state_json: Mapped[dict[str, Any] | None] = mapped_column(JSON, default=dict, nullable=True)
    grading_status: Mapped[str] = mapped_column(
        String(32), default="GRADED", nullable=False
    )  # GRADED, PENDING_REVIEW
    report_json: Mapped[dict[str, Any] | None] = mapped_column(JSON, default=None, nullable=True)
    report_status: Mapped[str] = mapped_column(
        String(32), default="NONE", nullable=False
    )  # NONE, PENDING_APPROVAL, APPROVED, REJECTED
    report_approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="attempts")
    learner: Mapped["User"] = relationship("User", foreign_keys=[learner_id])
    answers: Mapped[list["Answer"]] = relationship(
        "Answer", back_populates="attempt", cascade="all, delete-orphan"
    )
    submissions: Mapped[list["Submission"]] = relationship(
        "Submission", back_populates="attempt", cascade="all, delete-orphan"
    )


class Answer(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Answer provided for a question within an assessment attempt."""

    __tablename__ = "answers"

    attempt_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("assessment_attempts.id", ondelete="CASCADE"), index=True, nullable=False
    )
    bank_question_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("question_bank.id", ondelete="CASCADE"), index=True, nullable=False
    )
    selected_option_ids_json: Mapped[list[str] | None] = mapped_column(JSON, default=list, nullable=True)
    text_response: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    file_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    mentor_feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    grading_status: Mapped[str] = mapped_column(
        String(32), default="GRADED", nullable=False
    )  # GRADED, PENDING_REVIEW
    is_flagged: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    score_awarded: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Relationships
    attempt: Mapped["AssessmentAttempt"] = relationship("AssessmentAttempt", back_populates="answers")
    question: Mapped["QuestionBank"] = relationship("QuestionBank")

    @property
    def question_id(self) -> str:
        return self.bank_question_id


class Submission(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Code submission executed and evaluated against test cases."""

    __tablename__ = "submissions"

    attempt_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("assessment_attempts.id", ondelete="CASCADE"), index=True, nullable=True
    )
    coding_problem_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("coding_problems.id", ondelete="CASCADE"), index=True, nullable=False
    )
    learner_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    code: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(32), nullable=False)  # python, java, javascript, cpp, c
    verdict: Mapped[str] = mapped_column(
        String(32), default="PENDING", nullable=False
    )  # ACCEPTED, WRONG_ANSWER, RUNTIME_ERROR, TIME_LIMIT_EXCEEDED, MEMORY_LIMIT_EXCEEDED, COMPILATION_ERROR
    runtime_ms: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    memory_mb: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    passed_cases: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_cases: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    details_json: Mapped[dict[str, Any] | None] = mapped_column(JSON, default=dict, nullable=True)

    # Relationships
    attempt: Mapped["AssessmentAttempt | None"] = relationship("AssessmentAttempt", back_populates="submissions")
    problem: Mapped["CodingProblem"] = relationship("CodingProblem")
    learner: Mapped["User"] = relationship("User", foreign_keys=[learner_id])
