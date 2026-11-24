"""Add assessment_notes table for mentor module study notes.

Revision ID: 0012
Revises: 0011
Create Date: 2026-11-24 18:00:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '0012'
down_revision: Union[str, None] = '0011'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    tables = insp.get_table_names()

    if "assessment_notes" not in tables:
        op.create_table(
            "assessment_notes",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("assessment_id", sa.String(36), sa.ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True),
            sa.Column("author_id", sa.String(36), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True),
            sa.Column("title", sa.String(255), nullable=False),
            sa.Column("module_name", sa.String(255), nullable=False, server_default="Core Module"),
            sa.Column("summary", sa.Text(), nullable=True),
            sa.Column("content", sa.Text(), nullable=False),
            sa.Column("key_takeaways", sa.JSON(), nullable=True),
            sa.Column("recommended_reading", sa.JSON(), nullable=True),
            sa.Column("estimated_read_time_minutes", sa.Integer(), nullable=False, server_default="10"),
            sa.Column("is_published", sa.Boolean(), nullable=False, server_default="true"),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        )


def downgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    tables = insp.get_table_names()

    if "assessment_notes" in tables:
        op.drop_table("assessment_notes")
