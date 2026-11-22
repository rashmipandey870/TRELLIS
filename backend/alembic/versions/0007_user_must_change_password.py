"""Add must_change_password to users.

Revision ID: 0007_user_must_change_password
Revises: 0006_assessment_categories_and_reports
Create Date: 2026-11-22 06:25:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0007_user_must_change_password'
down_revision: Union[str, None] = '0006_assessment_categories_and_reports'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    cols = [c["name"] for c in insp.get_columns("users")]
    if "must_change_password" not in cols:
        op.add_column("users", sa.Column("must_change_password", sa.Boolean(), server_default=sa.text("false"), nullable=False))


def downgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    cols = [c["name"] for c in insp.get_columns("users")]
    if "must_change_password" in cols:
        op.drop_column("users", "must_change_password")
