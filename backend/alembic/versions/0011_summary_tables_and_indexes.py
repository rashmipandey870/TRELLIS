"""Add precomputed summary tables and composite indexes.

Revision ID: 0011
Revises: 0010
Create Date: 2026-11-24 05:00:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0011'
down_revision: Union[str, None] = '0010'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    tables = insp.get_table_names()

    if "learner_stats" not in tables:
        op.create_table(
            "learner_stats",
            sa.Column("learner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
            sa.Column("total_assessments_taken", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("average_score", sa.Float(), nullable=False, server_default="0.0"),
            sa.Column("median_score", sa.Float(), nullable=False, server_default="0.0"),
            sa.Column("streak_days", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("active_days", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("practice_total", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("practice_accuracy", sa.Float(), nullable=False, server_default="0.0"),
            sa.Column("attendance_rate", sa.Float(), nullable=False, server_default="0.0"),
            sa.Column("coding_acceptance_rate", sa.Float(), nullable=False, server_default="0.0"),
            sa.Column("velocity", sa.Float(), nullable=False, server_default="0.0"),
            sa.Column("trend_label", sa.String(32), nullable=False, server_default="Steady"),
            sa.Column("percentile", sa.Float(), nullable=True),
            sa.Column("risk_flag", sa.String(64), nullable=True),
            sa.Column("risk_reasons_json", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        )

    if "assessment_stats" not in tables:
        op.create_table(
            "assessment_stats",
            sa.Column("assessment_id", sa.String(36), sa.ForeignKey("assessments.id", ondelete="CASCADE"), primary_key=True),
            sa.Column("assigned_count", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("started_count", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("submitted_count", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("graded_count", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("pass_rate", sa.Float(), nullable=False, server_default="0.0"),
            sa.Column("mean_score", sa.Float(), nullable=False, server_default="0.0"),
            sa.Column("median_score", sa.Float(), nullable=False, server_default="0.0"),
            sa.Column("stdev_score", sa.Float(), nullable=False, server_default="0.0"),
            sa.Column("histogram_json", sa.Text(), nullable=True),
            sa.Column("item_analysis_json", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        )

    if "batch_stats" not in tables:
        op.create_table(
            "batch_stats",
            sa.Column("batch_id", sa.String(36), sa.ForeignKey("batches.id", ondelete="CASCADE"), primary_key=True),
            sa.Column("learner_count", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("average_score", sa.Float(), nullable=False, server_default="0.0"),
            sa.Column("completion_rate", sa.Float(), nullable=False, server_default="0.0"),
            sa.Column("practice_count", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("attendance_rate", sa.Float(), nullable=False, server_default="0.0"),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        )

    if "topic_mastery" not in tables:
        op.create_table(
            "topic_mastery",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("learner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
            sa.Column("topic", sa.String(100), nullable=False, index=True),
            sa.Column("total_questions", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("correct_questions", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("accuracy", sa.Float(), nullable=False, server_default="0.0"),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        )


def downgrade() -> None:
    op.drop_table("topic_mastery")
    op.drop_table("batch_stats")
    op.drop_table("assessment_stats")
    op.drop_table("learner_stats")
