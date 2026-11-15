"""Migration 0004: User Pseudonym Salt and Climbing Streak Tracking.

Revision ID: 0004
Revises: 0003
Create Date: 2026-11-15 01:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0004"
down_revision: str | None = "0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("pseudonym_salt", sa.String(64), nullable=True))
    op.add_column(
        "users",
        sa.Column("streak_days", sa.Integer(), server_default=sa.text("0"), nullable=False),
    )
    op.add_column(
        "users",
        sa.Column(
            "streak_freezes_remaining", sa.Integer(), server_default=sa.text("2"), nullable=False
        ),
    )
    op.add_column("users", sa.Column("last_active_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "last_active_at")
    op.drop_column("users", "streak_freezes_remaining")
    op.drop_column("users", "streak_days")
    op.drop_column("users", "pseudonym_salt")
