"""Create ai_question_pool table for database-persisted verified question pool.

Revision ID: 0009
Revises: 0008
Create Date: 2026-11-22 17:30:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0009'
down_revision: Union[str, None] = '0008'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    tables = insp.get_table_names()

    if "ai_question_pool" not in tables:
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
    op.drop_table("ai_question_pool")
