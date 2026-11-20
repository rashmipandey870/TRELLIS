"""Migration 0002: Skills Taxonomy & Cryptographic Evidence Ledger

Revision ID: 0002
Revises: 0001
Create Date: 2026-11-13 14:15:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. skills
    op.create_table(
        "skills",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "org_id",
            sa.String(36),
            sa.ForeignKey("organisations.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("code", sa.String(64), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("category", sa.String(64), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "decay_half_life_days", sa.Integer(), server_default=sa.text("365"), nullable=False
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("org_id", "code", name="uq_skills_org_code"),
    )
    op.create_index("ix_skills_org_id", "skills", ["org_id"])
    op.create_index("ix_skills_code", "skills", ["code"])
    op.create_index("ix_skills_category", "skills", ["category"])

    # 2. skill_levels
    op.create_table(
        "skill_levels",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "skill_id",
            sa.String(36),
            sa.ForeignKey("skills.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("level_number", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(128), nullable=False),
        sa.Column("rubric_text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("skill_id", "level_number", name="uq_skill_levels_skill_level"),
    )
    op.create_index("ix_skill_levels_skill_id", "skill_levels", ["skill_id"])

    # 3. skill_edges
    op.create_table(
        "skill_edges",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "org_id",
            sa.String(36),
            sa.ForeignKey("organisations.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "source_skill_id",
            sa.String(36),
            sa.ForeignKey("skills.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "target_skill_id",
            sa.String(36),
            sa.ForeignKey("skills.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("relationship_type", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "source_skill_id", "target_skill_id", "relationship_type", name="uq_skill_edges_pair"
        ),
    )
    op.create_index("ix_skill_edges_org_id", "skill_edges", ["org_id"])
    op.create_index("ix_skill_edges_source", "skill_edges", ["source_skill_id"])
    op.create_index("ix_skill_edges_target", "skill_edges", ["target_skill_id"])

    # 4. role_requirements
    op.create_table(
        "role_requirements",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "org_id",
            sa.String(36),
            sa.ForeignKey("organisations.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("role_code", sa.String(64), nullable=False),
        sa.Column(
            "skill_id",
            sa.String(36),
            sa.ForeignKey("skills.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("target_level", sa.Integer(), nullable=False),
        sa.Column("is_mandatory", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "org_id", "role_code", "skill_id", name="uq_role_requirements_role_skill"
        ),
    )
    op.create_index("ix_role_req_org_id", "role_requirements", ["org_id"])
    op.create_index("ix_role_req_role_code", "role_requirements", ["role_code"])

    # 5. evidence_records (Erasable for DPDP crypto-shredding)
    op.create_table(
        "evidence_records",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "org_id",
            sa.String(36),
            sa.ForeignKey("organisations.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "skill_id",
            sa.String(36),
            sa.ForeignKey("skills.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("evidence_type", sa.String(64), nullable=False),
        sa.Column("weight", sa.Float(), server_default=sa.text("1.0"), nullable=False),
        sa.Column("raw_payload_json", sa.JSON(), nullable=True),
        sa.Column("key_id", sa.String(64), nullable=True),
        sa.Column("is_shredded", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_evidence_records_user_id", "evidence_records", ["user_id"])
    op.create_index("ix_evidence_records_skill_id", "evidence_records", ["skill_id"])

    # 6. evidence_ledger (Immutable SHA-256 Hash Chaining)
    op.create_table(
        "evidence_ledger",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "org_id",
            sa.String(36),
            sa.ForeignKey("organisations.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("employee_pseudonym", sa.String(64), nullable=False),
        sa.Column("seq_num", sa.BigInteger(), nullable=False),
        sa.Column("prev_hash", sa.String(64), nullable=False),
        sa.Column("data_hash", sa.String(64), nullable=False),
        sa.Column("block_hash", sa.String(64), nullable=False),
        sa.Column(
            "record_id",
            sa.String(36),
            sa.ForeignKey("evidence_records.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "org_id", "employee_pseudonym", "seq_num", name="uq_ledger_employee_seq"
        ),
    )
    op.create_index("ix_ledger_pseudonym", "evidence_ledger", ["employee_pseudonym"])

    # 7. ledger_checkpoints (Immutable Root Checkpoints)
    op.create_table(
        "ledger_checkpoints",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "org_id",
            sa.String(36),
            sa.ForeignKey("organisations.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("checkpoint_seq", sa.BigInteger(), nullable=False),
        sa.Column("root_hash", sa.String(64), nullable=False),
        sa.Column("signature", sa.Text(), nullable=False),
        sa.Column("signing_key_id", sa.String(64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("org_id", "checkpoint_seq", name="uq_checkpoints_org_seq"),
    )


def downgrade() -> None:
    op.drop_table("ledger_checkpoints")
    op.drop_table("evidence_ledger")
    op.drop_table("evidence_records")
    op.drop_table("role_requirements")
    op.drop_table("skill_edges")
    op.drop_table("skill_levels")
    op.drop_table("skills")
