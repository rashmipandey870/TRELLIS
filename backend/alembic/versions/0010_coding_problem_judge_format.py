"""Add judge format columns to coding_problems table.

Revision ID: 0010
Revises: 0009
Create Date: 2026-11-23 01:30:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0010'
down_revision: Union[str, None] = '0009'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    columns = [c["name"] for c in insp.get_columns("coding_problems")]

    if "entry_point" not in columns:
        op.add_column("coding_problems", sa.Column("entry_point", sa.String(128), nullable=True))
    if "argument_schema" not in columns:
        op.add_column("coding_problems", sa.Column("argument_schema", sa.JSON(), nullable=True))
    if "wrong_stub" not in columns:
        op.add_column("coding_problems", sa.Column("wrong_stub", sa.Text(), nullable=True))
    if "complexity_notes" not in columns:
        op.add_column("coding_problems", sa.Column("complexity_notes", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("coding_problems", "complexity_notes")
    op.drop_column("coding_problems", "wrong_stub")
    op.drop_column("coding_problems", "argument_schema")
    op.drop_column("coding_problems", "entry_point")
