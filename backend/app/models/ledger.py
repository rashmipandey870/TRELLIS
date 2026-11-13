"""TRELLIS Cryptographic Evidence Ledger & Crypto-Shredding ORM Models."""

from typing import Any

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    Float,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, ImmutableMixin, TimestampMixin, UUIDPrimaryKeyMixin


class EvidenceLedger(Base, ImmutableMixin):
    """Append-only cryptographic hash chain recording employee skill evidence events.

    Hash Invariant (RFC 8785 JCS + SHA-256):
    Hash_n = SHA256(org_id || employee_pseudonym || seq_num || prev_hash || data_hash)

    Database invariant: No UPDATE or DELETE privileges are granted on this table.
    """

    __tablename__ = "evidence_ledger"
    __immutable__ = True

    org_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organisations.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    employee_pseudonym: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    seq_num: Mapped[int] = mapped_column(BigInteger, nullable=False)
    prev_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    data_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    block_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    record_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("evidence_records.id", ondelete="RESTRICT"), nullable=False
    )

    # Relationships
    record: Mapped["EvidenceRecord"] = relationship("EvidenceRecord", back_populates="ledger_entry")

    __table_args__ = (
        UniqueConstraint("org_id", "employee_pseudonym", "seq_num", name="uq_ledger_employee_seq"),
        Index("ix_ledger_employee_pseudonym", "employee_pseudonym"),
    )


class EvidenceRecord(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Off-chain erasable evidence payload supporting DPDP crypto-shredding.

    Upon Right to Erasure, raw_payload_json and key_id are deleted (crypto-shredded)
    and is_shredded is set to True, while EvidenceLedger hash chain remains intact.
    """

    __tablename__ = "evidence_records"

    org_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organisations.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    skill_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("skills.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    evidence_type: Mapped[str] = mapped_column(
        String(64), index=True, nullable=False
    )  # ASSESSMENT_ATTEMPT, COURSE_COMPLETION, etc.
    weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    raw_payload_json: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    key_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_shredded: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    ledger_entry: Mapped["EvidenceLedger | None"] = relationship(
        "EvidenceLedger",
        back_populates="record",
        uselist=False,
    )


class LedgerCheckpoint(Base, ImmutableMixin):
    """Periodic cryptographically signed checkpoint of ledger roots for external auditability.

    Database invariant: No UPDATE or DELETE privileges are granted on this table.
    """

    __tablename__ = "ledger_checkpoints"
    __immutable__ = True

    org_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organisations.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    checkpoint_seq: Mapped[int] = mapped_column(BigInteger, nullable=False)
    root_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    signature: Mapped[str] = mapped_column(Text, nullable=False)
    signing_key_id: Mapped[str] = mapped_column(String(64), nullable=False)

    __table_args__ = (UniqueConstraint("org_id", "checkpoint_seq", name="uq_checkpoints_org_seq"),)
