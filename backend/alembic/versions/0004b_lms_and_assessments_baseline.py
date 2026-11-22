"""Migration 0004b: LMS, Assessments, Meetings, Practice & Platform Baseline.

Revision ID: 0004b
Revises: 0004
Create Date: 2026-11-22 06:40:00.000000

"""

from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0004b"
down_revision: Union[str, None] = "0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    existing_tables = set(insp.get_table_names())

    # 1. Update batches table if columns missing
    if "batches" in existing_tables:
        batch_cols = [c["name"] for c in insp.get_columns("batches")]
        if "code" not in batch_cols:
            op.add_column("batches", sa.Column("code", sa.String(64), nullable=True))
            op.execute("UPDATE batches SET code = 'BATCH-' || substr(id, 1, 8) WHERE code IS NULL")
            try:
                op.create_index("ix_batches_code", "batches", ["code"], unique=True)
            except Exception:
                pass
        if "description" not in batch_cols:
            op.add_column("batches", sa.Column("description", sa.Text(), nullable=True))
        if "field" not in batch_cols:
            op.add_column("batches", sa.Column("field", sa.String(128), server_default="General", nullable=False))
        if "is_active" not in batch_cols:
            op.add_column("batches", sa.Column("is_active", sa.Boolean(), server_default=sa.text("true" if bind.dialect.name == "postgresql" else "1"), nullable=False))

    # 2. Update users table if role column missing
    if "users" in existing_tables:
        user_cols = [c["name"] for c in insp.get_columns("users")]
        if "role" not in user_cols:
            op.add_column("users", sa.Column("role", sa.String(32), server_default="LEARNER", nullable=False))
            try:
                op.create_index("ix_users_role", "users", ["role"], unique=False)
            except Exception:
                pass

    # 3. refresh_tokens
    if "refresh_tokens" not in existing_tables:
        op.create_table(
            "refresh_tokens",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("org_id", sa.String(36), sa.ForeignKey("organisations.id", ondelete="RESTRICT"), index=True, nullable=False),
            sa.Column("family_id", sa.String(36), index=True, nullable=False),
            sa.Column("token_hash", sa.String(64), unique=True, index=True, nullable=False),
            sa.Column("is_revoked", sa.Boolean(), default=False, nullable=False),
            sa.Column("replaced_by_token_id", sa.String(36), nullable=True),
            sa.Column("device_info", sa.String(512), nullable=True),
            sa.Column("ip_address", sa.String(45), nullable=True),
            sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )
        try:
            op.create_index("ix_refresh_family_revoked", "refresh_tokens", ["family_id", "is_revoked"], unique=False)
        except Exception:
            pass

    # 4. mentor_learner_assignments
    if "mentor_learner_assignments" not in existing_tables:
        op.create_table(
            "mentor_learner_assignments",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("mentor_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("learner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("batch_id", sa.String(36), sa.ForeignKey("batches.id", ondelete="SET NULL"), index=True, nullable=True),
            sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.UniqueConstraint("mentor_id", "learner_id", name="uq_mentor_learner"),
        )

    # 5. meetings
    if "meetings" not in existing_tables:
        op.create_table(
            "meetings",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("title", sa.String(255), nullable=False),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("meeting_date", sa.String(32), nullable=False),
            sa.Column("start_time", sa.String(32), nullable=False),
            sa.Column("end_time", sa.String(32), nullable=False),
            sa.Column("duration_minutes", sa.Integer(), nullable=False),
            sa.Column("meeting_link", sa.String(512), nullable=False),
            sa.Column("mentor_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("batch_id", sa.String(36), sa.ForeignKey("batches.id", ondelete="SET NULL"), index=True, nullable=True),
            sa.Column("status", sa.String(32), server_default="SCHEDULED", nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # 6. meeting_audience
    if "meeting_audience" not in existing_tables:
        op.create_table(
            "meeting_audience",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("meeting_id", sa.String(36), sa.ForeignKey("meetings.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("learner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=True),
            sa.Column("batch_id", sa.String(36), sa.ForeignKey("batches.id", ondelete="CASCADE"), index=True, nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # 7. meeting_attendance
    if "meeting_attendance" not in existing_tables:
        op.create_table(
            "meeting_attendance",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("meeting_id", sa.String(36), sa.ForeignKey("meetings.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("learner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("attended", sa.Boolean(), server_default=sa.text("false" if bind.dialect.name == "postgresql" else "0"), nullable=False),
            sa.Column("marked_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("remarks", sa.String(512), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.UniqueConstraint("meeting_id", "learner_id", name="uq_meeting_attendance"),
        )

    # 8. question_bank
    if "question_bank" not in existing_tables:
        op.create_table(
            "question_bank",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("author_id", sa.String(36), sa.ForeignKey("users.id", ondelete="RESTRICT"), index=True, nullable=False),
            sa.Column("title", sa.String(255), nullable=False),
            sa.Column("question_text", sa.Text(), nullable=False),
            sa.Column("question_type", sa.String(32), nullable=False),
            sa.Column("category", sa.String(64), server_default="Technical Knowledge", nullable=False),
            sa.Column("field", sa.String(128), index=True, nullable=False),
            sa.Column("topic", sa.String(128), index=True, nullable=False),
            sa.Column("difficulty", sa.String(32), nullable=False),
            sa.Column("tags_json", sa.JSON(), nullable=True),
            sa.Column("explanation", sa.Text(), nullable=True),
            sa.Column("is_active", sa.Boolean(), server_default=sa.text("true" if bind.dialect.name == "postgresql" else "1"), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # 9. mcq_options
    if "mcq_options" not in existing_tables:
        op.create_table(
            "mcq_options",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("question_id", sa.String(36), sa.ForeignKey("question_bank.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("option_text", sa.Text(), nullable=False),
            sa.Column("is_correct", sa.Boolean(), server_default=sa.text("false" if bind.dialect.name == "postgresql" else "0"), nullable=False),
            sa.Column("explanation", sa.Text(), nullable=True),
            sa.Column("sequence_order", sa.Integer(), server_default="1", nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # 10. coding_problems
    if "coding_problems" not in existing_tables:
        op.create_table(
            "coding_problems",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("bank_id", sa.String(36), sa.ForeignKey("question_bank.id", ondelete="CASCADE"), index=True, nullable=True),
            sa.Column("title", sa.String(255), nullable=False),
            sa.Column("description", sa.Text(), nullable=False),
            sa.Column("constraints", sa.Text(), nullable=True),
            sa.Column("difficulty", sa.String(32), server_default="MEDIUM", nullable=False),
            sa.Column("field", sa.String(128), server_default="General", nullable=False),
            sa.Column("marks", sa.Float(), server_default="10.0", nullable=False),
            sa.Column("time_limit_ms", sa.Integer(), server_default="2000", nullable=False),
            sa.Column("memory_limit_mb", sa.Integer(), server_default="256", nullable=False),
            sa.Column("examples_json", sa.JSON(), nullable=True),
            sa.Column("starter_code_json", sa.JSON(), nullable=True),
            sa.Column("reference_solution", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # 11. test_cases
    if "test_cases" not in existing_tables:
        op.create_table(
            "test_cases",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("problem_id", sa.String(36), sa.ForeignKey("coding_problems.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("input_data", sa.Text(), nullable=False),
            sa.Column("expected_output", sa.Text(), nullable=False),
            sa.Column("is_hidden", sa.Boolean(), server_default=sa.text("false" if bind.dialect.name == "postgresql" else "0"), nullable=False),
            sa.Column("weight", sa.Float(), server_default="1.0", nullable=False),
            sa.Column("time_limit_ms", sa.Integer(), nullable=True),
            sa.Column("memory_limit_mb", sa.Integer(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # 12. assessments
    if "assessments" not in existing_tables:
        op.create_table(
            "assessments",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("mentor_id", sa.String(36), sa.ForeignKey("users.id", ondelete="RESTRICT"), index=True, nullable=False),
            sa.Column("batch_id", sa.String(36), sa.ForeignKey("batches.id", ondelete="SET NULL"), index=True, nullable=True),
            sa.Column("title", sa.String(255), nullable=False),
            sa.Column("field", sa.String(128), server_default="General", nullable=False),
            sa.Column("instructions", sa.Text(), nullable=True),
            sa.Column("duration_minutes", sa.Integer(), server_default="60", nullable=False),
            sa.Column("passing_score", sa.Float(), server_default="60.0", nullable=False),
            sa.Column("start_window", sa.DateTime(timezone=True), nullable=True),
            sa.Column("end_window", sa.DateTime(timezone=True), nullable=True),
            sa.Column("status", sa.String(32), server_default="DRAFT", nullable=False),
            sa.Column("version", sa.Integer(), server_default="1", nullable=False),
            sa.Column("show_explanations", sa.Boolean(), server_default=sa.text("true" if bind.dialect.name == "postgresql" else "1"), nullable=False),
            sa.Column("mask_hidden_cases", sa.Boolean(), server_default=sa.text("true" if bind.dialect.name == "postgresql" else "1"), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # 13. assessment_questions
    if "assessment_questions" not in existing_tables:
        op.create_table(
            "assessment_questions",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("assessment_id", sa.String(36), sa.ForeignKey("assessments.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("bank_question_id", sa.String(36), sa.ForeignKey("question_bank.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("sequence_order", sa.Integer(), server_default="1", nullable=False),
            sa.Column("marks", sa.Float(), server_default="5.0", nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # 14. assessment_attempts
    if "assessment_attempts" not in existing_tables:
        op.create_table(
            "assessment_attempts",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("assessment_id", sa.String(36), sa.ForeignKey("assessments.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("learner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
            sa.Column("submit_time", sa.DateTime(timezone=True), nullable=True),
            sa.Column("score", sa.Float(), server_default="0.0", nullable=False),
            sa.Column("total_marks", sa.Float(), server_default="100.0", nullable=False),
            sa.Column("passed", sa.Boolean(), server_default=sa.text("false" if bind.dialect.name == "postgresql" else "0"), nullable=False),
            sa.Column("status", sa.String(32), server_default="IN_PROGRESS", nullable=False),
            sa.Column("tab_switch_count", sa.Integer(), server_default="0", nullable=False),
            sa.Column("autosave_state_json", sa.JSON(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # 15. answers
    if "answers" not in existing_tables:
        op.create_table(
            "answers",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("attempt_id", sa.String(36), sa.ForeignKey("assessment_attempts.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("bank_question_id", sa.String(36), sa.ForeignKey("question_bank.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("selected_option_ids_json", sa.JSON(), nullable=True),
            sa.Column("is_flagged", sa.Boolean(), server_default=sa.text("false" if bind.dialect.name == "postgresql" else "0"), nullable=False),
            sa.Column("score_awarded", sa.Float(), server_default="0.0", nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # 16. submissions
    if "submissions" not in existing_tables:
        op.create_table(
            "submissions",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("attempt_id", sa.String(36), sa.ForeignKey("assessment_attempts.id", ondelete="CASCADE"), index=True, nullable=True),
            sa.Column("coding_problem_id", sa.String(36), sa.ForeignKey("coding_problems.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("learner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("code", sa.Text(), nullable=False),
            sa.Column("language", sa.String(32), nullable=False),
            sa.Column("verdict", sa.String(32), server_default="PENDING", nullable=False),
            sa.Column("runtime_ms", sa.Float(), server_default="0.0", nullable=False),
            sa.Column("memory_mb", sa.Float(), server_default="0.0", nullable=False),
            sa.Column("passed_cases", sa.Integer(), server_default="0", nullable=False),
            sa.Column("total_cases", sa.Integer(), server_default="0", nullable=False),
            sa.Column("score", sa.Float(), server_default="0.0", nullable=False),
            sa.Column("details_json", sa.JSON(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # 17. mentor_remarks
    if "mentor_remarks" not in existing_tables:
        op.create_table(
            "mentor_remarks",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("mentor_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("learner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("assessment_id", sa.String(36), sa.ForeignKey("assessments.id", ondelete="SET NULL"), index=True, nullable=True),
            sa.Column("meeting_id", sa.String(36), sa.ForeignKey("meetings.id", ondelete="SET NULL"), index=True, nullable=True),
            sa.Column("remark_text", sa.Text(), nullable=False),
            sa.Column("visibility", sa.String(32), server_default="LEARNER_AND_ADMIN", nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # 18. practice_sessions
    if "practice_sessions" not in existing_tables:
        op.create_table(
            "practice_sessions",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("learner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("field", sa.String(128), index=True, nullable=False),
            sa.Column("difficulty", sa.String(32), nullable=False),
            sa.Column("mode", sa.String(32), nullable=False),
            sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # 19. practice_questions
    if "practice_questions" not in existing_tables:
        op.create_table(
            "practice_questions",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("session_id", sa.String(36), sa.ForeignKey("practice_sessions.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("field", sa.String(128), index=True, nullable=False),
            sa.Column("difficulty", sa.String(32), nullable=False),
            sa.Column("mode", sa.String(32), nullable=False),
            sa.Column("title", sa.String(255), nullable=False),
            sa.Column("question_data_json", sa.JSON(), nullable=False),
            sa.Column("reference_solution", sa.Text(), nullable=True),
            sa.Column("verified", sa.Boolean(), server_default=sa.text("false" if bind.dialect.name == "postgresql" else "0"), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # 20. practice_attempts
    if "practice_attempts" not in existing_tables:
        op.create_table(
            "practice_attempts",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("question_id", sa.String(36), sa.ForeignKey("practice_questions.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("learner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("answer_json", sa.JSON(), nullable=False),
            sa.Column("is_correct", sa.Boolean(), server_default=sa.text("false" if bind.dialect.name == "postgresql" else "0"), nullable=False),
            sa.Column("hints_used", sa.Integer(), server_default="0", nullable=False),
            sa.Column("ai_feedback", sa.Text(), nullable=True),
            sa.Column("score", sa.Float(), server_default="0.0", nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # 21. practice_scores
    if "practice_scores" not in existing_tables:
        op.create_table(
            "practice_scores",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("learner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("field", sa.String(128), index=True, nullable=False),
            sa.Column("active_days", sa.Integer(), server_default="0", nullable=False),
            sa.Column("streak_days", sa.Integer(), server_default="0", nullable=False),
            sa.Column("problems_attempted", sa.Integer(), server_default="0", nullable=False),
            sa.Column("problems_solved", sa.Integer(), server_default="0", nullable=False),
            sa.Column("acceptance_rate", sa.Float(), server_default="0.0", nullable=False),
            sa.Column("weighted_accuracy", sa.Float(), server_default="0.0", nullable=False),
            sa.Column("dedication_score", sa.Float(), server_default="0.0", nullable=False),
            sa.Column("last_practiced_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.UniqueConstraint("learner_id", "field", name="uq_learner_practice_field"),
        )

    # 22. talent_alerts
    if "talent_alerts" not in existing_tables:
        op.create_table(
            "talent_alerts",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("learner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("mentor_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("field", sa.String(128), index=True, nullable=False),
            sa.Column("evidence_json", sa.JSON(), nullable=False),
            sa.Column("status", sa.String(32), server_default="PENDING", nullable=False),
            sa.Column("action_taken", sa.String(64), nullable=True),
            sa.Column("action_notes", sa.Text(), nullable=True),
            sa.Column("action_time", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # 23. alert_actions
    if "alert_actions" not in existing_tables:
        op.create_table(
            "alert_actions",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("alert_id", sa.String(36), sa.ForeignKey("talent_alerts.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("mentor_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("action_taken", sa.String(64), nullable=False),
            sa.Column("notes", sa.Text(), nullable=True),
            sa.Column("action_time", sa.DateTime(timezone=True), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # 24. notifications
    if "notifications" not in existing_tables:
        op.create_table(
            "notifications",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("recipient_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
            sa.Column("sender_id", sa.String(36), sa.ForeignKey("users.id", ondelete="SET NULL"), index=True, nullable=True),
            sa.Column("title", sa.String(255), nullable=False),
            sa.Column("message", sa.Text(), nullable=False),
            sa.Column("notification_type", sa.String(64), nullable=False),
            sa.Column("link", sa.String(512), nullable=True),
            sa.Column("is_read", sa.Boolean(), server_default=sa.text("false" if bind.dialect.name == "postgresql" else "0"), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # 25. system_settings
    if "system_settings" not in existing_tables:
        op.create_table(
            "system_settings",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("key", sa.String(128), unique=True, index=True, nullable=False),
            sa.Column("value_json", sa.JSON(), nullable=False),
            sa.Column("updated_by_id", sa.String(36), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )

    # 25. ai_question_pool
    if "ai_question_pool" not in existing_tables:
        op.create_table(
            "ai_question_pool",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("field", sa.String(128), index=True, nullable=False),
            sa.Column("category", sa.String(64), index=True, server_default="Technical Knowledge", nullable=False),
            sa.Column("difficulty", sa.String(32), index=True, nullable=False),
            sa.Column("mode", sa.String(32), index=True, nullable=False),
            sa.Column("language", sa.String(32), nullable=True),
            sa.Column("title", sa.String(255), nullable=False),
            sa.Column("question_hash", sa.String(64), index=True, nullable=False),
            sa.Column("question_data_json", sa.JSON(), nullable=False),
            sa.Column("provenance_json", sa.JSON(), nullable=False),
            sa.Column("is_used", sa.Boolean(), server_default=sa.text("false" if bind.dialect.name == "postgresql" else "0"), index=True, nullable=False),
            sa.Column("used_by_learner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
            sa.Column("verified", sa.Boolean(), server_default=sa.text("true" if bind.dialect.name == "postgresql" else "1"), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )


def downgrade() -> None:
    tables = [
        "ai_question_pool",
        "system_settings",
        "notifications",
        "alert_actions",
        "talent_alerts",
        "practice_scores",
        "practice_attempts",
        "practice_questions",
        "practice_sessions",
        "mentor_remarks",
        "submissions",
        "answers",
        "assessment_attempts",
        "assessment_questions",
        "assessments",
        "test_cases",
        "coding_problems",
        "mcq_options",
        "question_bank",
        "meeting_attendance",
        "meeting_audience",
        "meetings",
        "mentor_learner_assignments",
        "refresh_tokens",
    ]
    for table in tables:
        try:
            op.drop_table(table)
        except Exception:
            pass
