"""Migration 0005: Assessment Audience for Batch and Selected Learners.

Revision ID: 0005
Revises: 0004
Create Date: 2026-11-20 16:15:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0005"
down_revision: str | None = "0004b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    if "assessment_audience" not in insp.get_table_names():
        op.create_table(
            "assessment_audience",
            sa.Column("id", sa.String(36), primary_key=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("assessment_id", sa.String(36), sa.ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True),
            sa.Column("learner_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        )


def downgrade() -> None:
    op.drop_table("assessment_audience")
