"""Migration 0003: Pathways, Courses, Modules, Cohorts, and Enrolments (Slice 1.6).

Revision ID: 0003
Revises: 0002
Create Date: 2026-11-14 23:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0003"
down_revision: str | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. pathways
    op.create_table(
        "pathways",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "org_id",
            sa.String(36),
            sa.ForeignKey("organisations.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("code", sa.String(64), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "author_id",
            sa.String(36),
            sa.ForeignKey("users.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("is_published", sa.Boolean(), default=False, nullable=False),
        sa.Column("target_role_code", sa.String(64), nullable=True),
        sa.Column("estimated_hours", sa.Float(), default=0.0, nullable=False),
        sa.Column("is_first_90_days", sa.Boolean(), default=False, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("org_id", "code", name="uq_pathways_org_code"),
    )
    op.create_index("ix_pathways_org_id", "pathways", ["org_id"])
    op.create_index("ix_pathways_author_id", "pathways", ["author_id"])
    op.create_index("ix_pathways_is_published", "pathways", ["is_published"])
    op.create_index("ix_pathways_first_90_days", "pathways", ["is_first_90_days"])

    # 2. courses
    op.create_table(
        "courses",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "org_id",
            sa.String(36),
            sa.ForeignKey("organisations.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "pathway_id",
            sa.String(36),
            sa.ForeignKey("pathways.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("code", sa.String(64), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sequence_order", sa.Integer(), default=1, nullable=False),
        sa.Column(
            "prerequisite_course_id",
            sa.String(36),
            sa.ForeignKey("courses.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("pathway_id", "code", name="uq_courses_pathway_code"),
    )
    op.create_index("ix_courses_org_id", "courses", ["org_id"])
    op.create_index("ix_courses_pathway_id", "courses", ["pathway_id"])

    # 3. modules
    op.create_table(
        "modules",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "org_id",
            sa.String(36),
            sa.ForeignKey("organisations.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "course_id",
            sa.String(36),
            sa.ForeignKey("courses.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("module_type", sa.String(64), default="LESSON", nullable=False),
        sa.Column("sequence_order", sa.Integer(), default=1, nullable=False),
        sa.Column("estimated_minutes", sa.Integer(), default=30, nullable=False),
        sa.Column("content_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_modules_org_id", "modules", ["org_id"])
    op.create_index("ix_modules_course_id", "modules", ["course_id"])

    # 4. cohorts
    op.create_table(
        "cohorts",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "org_id",
            sa.String(36),
            sa.ForeignKey("organisations.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("code", sa.String(64), nullable=False),
        sa.Column(
            "pathway_id",
            sa.String(36),
            sa.ForeignKey("pathways.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "trainer_id",
            sa.String(36),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("org_id", "code", name="uq_cohorts_org_code"),
    )
    op.create_index("ix_cohorts_org_id", "cohorts", ["org_id"])

    # 5. batches
    op.create_table(
        "batches",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "org_id",
            sa.String(36),
            sa.ForeignKey("organisations.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "cohort_id",
            sa.String(36),
            sa.ForeignKey("cohorts.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("max_learners", sa.Integer(), default=30, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_batches_org_id", "batches", ["org_id"])
    op.create_index("ix_batches_cohort_id", "batches", ["cohort_id"])

    # 6. enrolments
    op.create_table(
        "enrolments",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "org_id",
            sa.String(36),
            sa.ForeignKey("organisations.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.String(36),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "pathway_id",
            sa.String(36),
            sa.ForeignKey("pathways.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "cohort_id",
            sa.String(36),
            sa.ForeignKey("cohorts.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "batch_id",
            sa.String(36),
            sa.ForeignKey("batches.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("status", sa.String(36), default="ENROLLED", nullable=False),
        sa.Column("progress_percent", sa.Float(), default=0.0, nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", "pathway_id", name="uq_enrolments_user_pathway"),
    )
    op.create_index("ix_enrolments_org_id", "enrolments", ["org_id"])
    op.create_index("ix_enrolments_user_id", "enrolments", ["user_id"])
    op.create_index("ix_enrolments_pathway_id", "enrolments", ["pathway_id"])


def downgrade() -> None:
    op.drop_table("enrolments")
    op.drop_table("batches")
    op.drop_table("cohorts")
    op.drop_table("modules")
    op.drop_table("courses")
    op.drop_table("pathways")
