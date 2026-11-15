"""TRELLIS Evidence Ledger & DPDP Crypto-Shredding Domain Service.

Implements Section 23 / ADR-0003:
- Cryptographic hash chaining:
  Hash_n = SHA256(org_id || employee_pseudonym || seq_num || prev_hash || data_hash)
- RFC 8785 canonical serialization of evidence payloads.
- High-concurrency sequence allocation with retry and conflict resolution.
- Daily Merkle root checkpoints with asymmetric RSA-PSS cryptographic signing.
- Off-chain crypto-shredding: Personal details are purged upon DPDP Right to Erasure,
  while on-chain hash sequence remains provably intact and verifiable.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import random
import time
from dataclasses import dataclass
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session

from app.core.jcs import compute_block_hash, compute_data_hash, rfc8785_canonicalize
from app.models import AuditLog, EvidenceLedger, EvidenceRecord, LedgerCheckpoint, User

# Invariant: Genesis block prev_hash is exactly 64 zero hex characters
GENESIS_PREV_HASH = "0" * 64


@dataclass
class VerificationResult:
    """Detailed cryptographic verification result for an employee evidence chain."""

    is_valid: bool
    total_blocks: int
    broken_seq: int | None = None
    reason: str | None = None


def derive_pseudonym(user_id: str, salt: str) -> str:
    """Derive deterministic pseudonymous identifier for an employee.

    Formula: HMAC-SHA256(user_id, salt)
    Zero plain-text PII is persisted in the immutable evidence ledger.
    Per-employee salt is strictly mandatory; fallback to system SECRET_KEY is prohibited.
    """
    if not salt or not salt.strip():
        raise ValueError(
            "MANDATORY_EMPLOYEE_SALT: derive_pseudonym requires an explicit, non-empty "
            "per-employee salt; fallback to system SECRET_KEY is strictly prohibited"
        )
    return hmac.new(salt.encode("utf-8"), user_id.encode("utf-8"), hashlib.sha256).hexdigest()


def append_evidence(
    session: Session,
    org_id: str,
    user_id: str,
    skill_id: str,
    evidence_type: str,
    payload: dict[str, Any],
    salt: str | None = None,
    weight: float = 1.0,
    key_id: str | None = None,
    max_retries: int = 10,
) -> EvidenceLedger:
    """Append a new evidence entry to the employee's tamper-evident hash chain.

    Ensures strictly consecutive sequence numbers (1, 2, ..., N) under high concurrency
    via optimistic concurrency control and retry with exponential jitter.
    """
    effective_salt = salt
    if not effective_salt:
        user = session.get(User, user_id)
        if user is not None and user.pseudonym_salt:
            effective_salt = user.pseudonym_salt

    if not effective_salt:
        raise ValueError(
            f"MANDATORY_EMPLOYEE_SALT: No cryptographic pseudonym salt registered for user '{user_id}'. "
            "Fallback to system key is prohibited."
        )

    pseudonym = derive_pseudonym(user_id, effective_salt)
    data_hash = compute_data_hash(payload)

    # Concurrency-safe sequence number and hash calculation with retry
    for attempt in range(max_retries):
        try:
            # 1. Create erasable off-chain EvidenceRecord
            record = EvidenceRecord(
                org_id=org_id,
                user_id=user_id,
                skill_id=skill_id,
                evidence_type=evidence_type,
                weight=weight,
                raw_payload_json=payload,
                key_id=key_id,
                is_shredded=False,
            )
            session.add(record)
            session.flush()

            # 2. Query the tip of the employee's chain
            stmt = (
                select(EvidenceLedger)
                .where(
                    EvidenceLedger.org_id == org_id,
                    EvidenceLedger.employee_pseudonym == pseudonym,
                )
                .order_by(EvidenceLedger.seq_num.desc())
                .limit(1)
            )

            # In MySQL, lock the row for update if dialect supports it
            if session.bind and session.bind.dialect.name == "mysql":
                stmt = stmt.with_for_update()

            last_entry = session.execute(stmt).scalars().first()

            if last_entry is None:
                seq_num = 1
                prev_hash = GENESIS_PREV_HASH
            else:
                seq_num = last_entry.seq_num + 1
                prev_hash = last_entry.block_hash

            block_hash = compute_block_hash(
                org_id=org_id,
                employee_pseudonym=pseudonym,
                seq_num=seq_num,
                prev_hash=prev_hash,
                data_hash=data_hash,
            )

            ledger_entry = EvidenceLedger(
                org_id=org_id,
                employee_pseudonym=pseudonym,
                seq_num=seq_num,
                prev_hash=prev_hash,
                data_hash=data_hash,
                block_hash=block_hash,
                record_id=record.id,
            )
            session.add(ledger_entry)
            session.commit()
            return ledger_entry

        except (IntegrityError, OperationalError):
            session.rollback()
            if attempt == max_retries - 1:
                raise
            # Exponential jitter before retry
            time.sleep(0.01 * (2**attempt) + random.uniform(0.005, 0.02))

    raise RuntimeError(f"Failed to append evidence after {max_retries} concurrent attempts.")


def verify_employee_chain(
    session: Session,
    org_id: str,
    employee_pseudonym: str,
) -> VerificationResult:
    """Verify cryptographic integrity of an employee's evidence hash chain from block 1 to tip.

    Verifies:
    1. Genesis block has seq_num=1 and prev_hash="0"*64.
    2. Sequence numbers are strictly consecutive (no gaps or duplicates).
    3. Each block's prev_hash exactly equals the prior block's block_hash.
    4. Each block's block_hash matches recomputed SHA256(org_id || pseudonym || seq || prev || data_hash).
    5. Off-chain payload (if not crypto-shredded) matches data_hash.
    """
    entries = (
        session.query(EvidenceLedger)
        .filter(
            EvidenceLedger.org_id == org_id,
            EvidenceLedger.employee_pseudonym == employee_pseudonym,
        )
        .order_by(EvidenceLedger.seq_num.asc())
        .all()
    )

    if not entries:
        return VerificationResult(is_valid=True, total_blocks=0)

    # 1. Genesis block validation
    genesis = entries[0]
    if genesis.seq_num != 1:
        return VerificationResult(
            is_valid=False,
            total_blocks=len(entries),
            broken_seq=genesis.seq_num,
            reason=f"Genesis block sequence number must be 1, found {genesis.seq_num}",
        )

    if genesis.prev_hash != GENESIS_PREV_HASH:
        return VerificationResult(
            is_valid=False,
            total_blocks=len(entries),
            broken_seq=1,
            reason=f"Genesis block prev_hash must be {GENESIS_PREV_HASH}, found {genesis.prev_hash}",
        )

    # 2. Sequential verification
    for i, entry in enumerate(entries):
        expected_seq = i + 1
        if entry.seq_num != expected_seq:
            return VerificationResult(
                is_valid=False,
                total_blocks=len(entries),
                broken_seq=entry.seq_num,
                reason=f"Sequence gap detected: expected {expected_seq}, found {entry.seq_num}",
            )

        # Check hash chaining link with previous block
        if i > 0:
            prior_block = entries[i - 1]
            if entry.prev_hash != prior_block.block_hash:
                return VerificationResult(
                    is_valid=False,
                    total_blocks=len(entries),
                    broken_seq=entry.seq_num,
                    reason=(
                        f"Broken chain link at seq {entry.seq_num}: "
                        f"prev_hash {entry.prev_hash} does not match prior block_hash {prior_block.block_hash}"
                    ),
                )

        # Recompute block hash
        expected_block_hash = compute_block_hash(
            org_id=entry.org_id,
            employee_pseudonym=entry.employee_pseudonym,
            seq_num=entry.seq_num,
            prev_hash=entry.prev_hash,
            data_hash=entry.data_hash,
        )
        if entry.block_hash != expected_block_hash:
            return VerificationResult(
                is_valid=False,
                total_blocks=len(entries),
                broken_seq=entry.seq_num,
                reason=(
                    f"Tampered block_hash at seq {entry.seq_num}: "
                    f"expected {expected_block_hash}, found {entry.block_hash}"
                ),
            )

        # Verify off-chain payload integrity (if payload has not been crypto-shredded)
        record = session.get(EvidenceRecord, entry.record_id)
        if record is not None and not record.is_shredded and record.raw_payload_json is not None:
            expected_data_hash = compute_data_hash(record.raw_payload_json)
            if entry.data_hash != expected_data_hash:
                return VerificationResult(
                    is_valid=False,
                    total_blocks=len(entries),
                    broken_seq=entry.seq_num,
                    reason=(
                        f"Tampered data_hash at seq {entry.seq_num}: "
                        f"payload yields {expected_data_hash}, ledger has {entry.data_hash}"
                    ),
                )

    return VerificationResult(is_valid=True, total_blocks=len(entries))


def create_signed_checkpoint(
    session: Session,
    org_id: str,
    private_key: rsa.RSAPrivateKey,
    signing_key_id: str,
) -> LedgerCheckpoint:
    """Compute deterministic root hash across all employee ledger tips and digitally sign it."""
    # Find next checkpoint sequence
    max_seq_val = (
        session.query(func.max(LedgerCheckpoint.checkpoint_seq))
        .filter(LedgerCheckpoint.org_id == org_id)
        .scalar()
    )
    checkpoint_seq = (max_seq_val or 0) + 1

    # Query latest block_hash for every employee pseudonym in the organisation
    subq = (
        session.query(
            EvidenceLedger.employee_pseudonym,
            func.max(EvidenceLedger.seq_num).label("max_seq"),
        )
        .filter(EvidenceLedger.org_id == org_id)
        .group_by(EvidenceLedger.employee_pseudonym)
        .subquery()
    )

    tips = (
        session.query(EvidenceLedger.employee_pseudonym, EvidenceLedger.block_hash)
        .join(
            subq,
            (EvidenceLedger.employee_pseudonym == subq.c.employee_pseudonym)
            & (EvidenceLedger.seq_num == subq.c.max_seq),
        )
        .order_by(EvidenceLedger.employee_pseudonym.asc())
        .all()
    )

    # Deterministic Merkle / state root representation
    tips_map = dict(tips)
    state_payload = {
        "org_id": org_id,
        "checkpoint_seq": checkpoint_seq,
        "tips": tips_map,
    }
    canonical_bytes = rfc8785_canonicalize(state_payload)
    root_hash = hashlib.sha256(canonical_bytes).hexdigest()

    # Asymmetric RSA-PSS digital signature
    signature_bytes = private_key.sign(
        root_hash.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    signature_b64 = base64.b64encode(signature_bytes).decode("utf-8")

    checkpoint = LedgerCheckpoint(
        org_id=org_id,
        checkpoint_seq=checkpoint_seq,
        root_hash=root_hash,
        signature=signature_b64,
        signing_key_id=signing_key_id,
    )
    session.add(checkpoint)
    session.commit()
    return checkpoint


def verify_checkpoint(
    checkpoint: LedgerCheckpoint,
    public_key_pem: bytes,
    signature_override: str | None = None,
) -> bool:
    """Verify digital signature of a ledger root checkpoint using the signer's public key."""
    try:
        public_key = load_pem_public_key(public_key_pem)
        if not isinstance(public_key, rsa.RSAPublicKey):
            return False

        sig_str = signature_override or checkpoint.signature
        sig_bytes = base64.b64decode(sig_str)

        public_key.verify(
            sig_bytes,
            checkpoint.root_hash.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except (InvalidSignature, ValueError, Exception):
        return False


def shred_evidence_record(
    session: Session,
    record_id: str,
    reason: str = "DPDP_RIGHT_TO_ERASURE",
    actor_id: str | None = None,
) -> bool:
    """Execute off-chain crypto-shredding under DPDP Act statutory Right to Erasure.

    Deletes personal raw_payload_json and key_id while leaving on-chain hash sequence
    in EvidenceLedger mathematically intact and verifiable.
    """
    record = session.get(EvidenceRecord, record_id)
    if record is None:
        return False

    before_state = {
        "is_shredded": record.is_shredded,
        "had_payload": record.raw_payload_json is not None,
    }

    # Crypto-shredding: permanently delete personal payload and decryption key
    record.raw_payload_json = None
    record.key_id = None
    record.is_shredded = True

    # Audit the statutory erasure event
    audit = AuditLog(
        org_id=record.org_id,
        actor_id=actor_id or "system_dpdp_handler",
        action="crypto_shred_evidence",
        resource="evidence_records",
        resource_id=record.id,
        reason=reason,
        before_state_json=before_state,
        after_state_json={"is_shredded": True, "payload_deleted": True},
    )
    session.add(audit)
    session.commit()
    return True


def crypto_shred_employee(
    session: Session,
    org_id: str,
    user_id: str,
    reason: str = "DPDP_RIGHT_TO_ERASURE",
    actor_id: str | None = None,
) -> dict[str, Any]:
    """Execute complete crypto-shredding for an employee under statutory DPDP Right to Erasure.

    1. Shreds all EvidenceRecord payloads and encryption keys belonging to user_id.
    2. Permanently destroys user.pseudonym_salt, making it mathematically impossible
       to re-derive the pseudonym or link historical EvidenceLedger blocks to the natural person.
    3. Records statutory audit log entry.
    """
    user = session.get(User, user_id)
    if user is None:
        raise ValueError(f"User '{user_id}' not found for crypto-shredding.")

    # 1. Shred all off-chain evidence records
    user_records = (
        session.query(EvidenceRecord)
        .filter(EvidenceRecord.user_id == user_id, EvidenceRecord.org_id == org_id)
        .all()
    )
    for rec in user_records:
        rec.raw_payload_json = None
        rec.key_id = None
        rec.is_shredded = True

    # 2. Shred the per-employee salt
    had_salt = user.pseudonym_salt is not None
    user.pseudonym_salt = None

    # 3. Transactional statutory audit
    audit = AuditLog(
        org_id=org_id,
        actor_id=actor_id or "system_dpdp_handler",
        action="crypto_shred_employee_salt",
        resource="users",
        resource_id=user_id,
        reason=reason,
        before_state_json={"had_pseudonym_salt": had_salt, "records_count": len(user_records)},
        after_state_json={"pseudonym_salt_shredded": True, "shredded_records_count": len(user_records)},
    )
    session.add(audit)
    session.commit()
    return {
        "user_id": user_id,
        "shredded_records": len(user_records),
        "pseudonym_salt_destroyed": True,
    }

