"""Add category to question_bank.

Revision ID: 0008
Revises: 0007
Create Date: 2026-11-22 08:00:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0008'
down_revision: Union[str, None] = '0007'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    tables = insp.get_table_names()
    if "question_bank" in tables:
        cols = [c["name"] for c in insp.get_columns("question_bank")]
        if "category" not in cols:
            op.add_column(
                "question_bank",
                sa.Column("category", sa.String(64), server_default="Technical Knowledge", nullable=False),
            )


def downgrade() -> None:
    op.drop_column("question_bank", "category")
