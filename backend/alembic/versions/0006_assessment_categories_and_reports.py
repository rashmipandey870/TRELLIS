"""Migration 0006: Assessment Categories (7 Types), Manual Grading, and Growth Ring Reports.

Revision ID: 0006
Revises: 0005
Create Date: 2026-11-22 05:15:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0006"
down_revision: str | None = "0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. question_bank rubric_json
    op.add_column("question_bank", sa.Column("rubric_json", sa.JSON(), nullable=True))

    # 2. coding_problems problem_type & schema_ddl
    op.add_column("coding_problems", sa.Column("problem_type", sa.String(32), server_default="CODING", nullable=False))
    op.add_column("coding_problems", sa.Column("schema_ddl", sa.Text(), nullable=True))

    # 3. answers multi-category fields
    op.add_column("answers", sa.Column("text_response", sa.Text(), nullable=True))
    op.add_column("answers", sa.Column("file_url", sa.String(512), nullable=True))
    op.add_column("answers", sa.Column("file_name", sa.String(255), nullable=True))
    op.add_column("answers", sa.Column("mentor_feedback", sa.Text(), nullable=True))
    op.add_column("answers", sa.Column("grading_status", sa.String(32), server_default="GRADED", nullable=False))

    # 4. assessment_attempts grading & reports
    op.add_column("assessment_attempts", sa.Column("grading_status", sa.String(32), server_default="GRADED", nullable=False))
    op.add_column("assessment_attempts", sa.Column("report_json", sa.JSON(), nullable=True))
    op.add_column("assessment_attempts", sa.Column("report_status", sa.String(32), server_default="NONE", nullable=False))
    op.add_column("assessment_attempts", sa.Column("report_approved_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("assessment_attempts", "report_approved_at")
    op.drop_column("assessment_attempts", "report_status")
    op.drop_column("assessment_attempts", "report_json")
    op.drop_column("assessment_attempts", "grading_status")

    op.drop_column("answers", "grading_status")
    op.drop_column("answers", "mentor_feedback")
    op.drop_column("answers", "file_name")
    op.drop_column("answers", "file_url")
    op.drop_column("answers", "text_response")

    op.drop_column("coding_problems", "schema_ddl")
    op.drop_column("coding_problems", "problem_type")

    op.drop_column("question_bank", "rubric_json")
