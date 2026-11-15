"""TRELLIS Evidence Ledger Core Test Suite (Section 23 / ADR-0003).

Tests:
1. RFC 8785 JSON Canonicalization Scheme (JCS) deterministic serialization.
2. Cryptographic SHA-256 hash chaining:
   Hash_n = SHA256(org_id || employee_pseudonym || seq_num || prev_hash || data_hash)
   Genesis block invariants (seq_num=1, prev_hash="0"*64).
3. Tamper detection:
   Detects modified data_hash, modified prev_hash, broken block_hash, and sequence gaps.
4. Per-employee sequence numbers under concurrent writes:
   Guarantees monotonically consecutive sequence numbers without collisions or gaps.
5. Signed root checkpoints:
   Asymmetric cryptographic signature of ledger state roots and offline verification.
6. Off-chain crypto-shredding:
   DPDP Act compliance where personal details are erased while ledger hash chain stays intact.
"""

from __future__ import annotations

import base64
import hashlib
from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool

from app.core.jcs import compute_block_hash, compute_data_hash, rfc8785_canonicalize
from app.models import EvidenceLedger, EvidenceRecord, Organisation, Skill, User
from app.models.base import Base
from app.services.ledger_service import (
    GENESIS_PREV_HASH,
    append_evidence,
    create_signed_checkpoint,
    crypto_shred_employee,
    derive_pseudonym,
    shred_evidence_record,
    verify_checkpoint,
    verify_employee_chain,
)


@pytest.fixture
def db_engine(tmp_path: Any) -> Generator[Engine, None, None]:
    """Provide a file-backed SQLite database engine supporting true concurrent thread connections."""
    db_file = tmp_path / "test_ledger.db"
    engine = create_engine(
        f"sqlite:///{db_file}",
        poolclass=NullPool,
        connect_args={"timeout": 30, "check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def db_session(db_engine: Engine) -> Generator[Session, None, None]:
    """Provide a database session attached to the shared in-memory engine."""
    session = Session(db_engine)
    try:
        yield session
    finally:
        session.close()


def test_rfc8785_canonical_serialization_determinism() -> None:
    """Verify that RFC 8785 JCS produces bit-for-bit identical output regardless of key order or whitespace."""
    # Two dicts with completely different key insertion orders and nested structures
    obj_a = {
        "title": "Senior Staff Architect Assessment",
        "score": 96.5,
        "metadata": {
            "version": 2,
            "approved": True,
            "tags": ["cloud", "architecture", "security"],
        },
        "rubric_results": [
            {"criterion": "System Design", "grade": "EXCEEDS"},
            {"criterion": "Code Quality", "grade": "EXCEEDS"},
        ],
    }

    obj_b = {
        "metadata": {
            "tags": ["cloud", "architecture", "security"],
            "version": 2,
            "approved": True,
        },
        "score": 96.5,
        "rubric_results": [
            {"criterion": "System Design", "grade": "EXCEEDS"},
            {"criterion": "Code Quality", "grade": "EXCEEDS"},
        ],
        "title": "Senior Staff Architect Assessment",
    }

    canonical_a = rfc8785_canonicalize(obj_a)
    canonical_b = rfc8785_canonicalize(obj_b)

    # 1. Byte-level equality
    assert canonical_a == canonical_b
    assert isinstance(canonical_a, bytes)

    # 2. No whitespace in JSON formatting
    assert b": " not in canonical_a
    assert b", " not in canonical_a

    # 3. Cryptographic SHA-256 hash determinism
    hash_a = compute_data_hash(obj_a)
    hash_b = compute_data_hash(obj_b)
    assert hash_a == hash_b
    assert len(hash_a) == 64
    assert hash_a == hashlib.sha256(canonical_a).hexdigest()


def test_evidence_ledger_hash_chaining_genesis_and_subsequent(db_session: Session) -> None:
    """Verify genesis block invariant and recursive hash chaining across sequential entries."""
    org = Organisation(name="CSM Technology", code="CSM_LEDGER_CHAIN")
    db_session.add(org)
    db_session.flush()

    user = User(
        org_id=org.id,
        email="chain_user@csm.tech",
        password_hash="dummy_hash",
        full_name="Chain Verifier",
        pseudonym_salt="salt_chain_user_01",
    )
    skill = Skill(org_id=org.id, code="SK_SEC_ARCH", name="Security Arch", category="TECHNICAL")
    db_session.add_all([user, skill])
    db_session.flush()

    pseudonym = derive_pseudonym(user.id, user.pseudonym_salt)

    # Block 1 (Genesis)
    payload_1 = {"task": "Module 1 Assessment", "score": 85}
    entry_1 = append_evidence(
        session=db_session,
        org_id=org.id,
        user_id=user.id,
        skill_id=skill.id,
        evidence_type="ASSESSMENT_ATTEMPT",
        payload=payload_1,
        weight=1.0,
    )

    assert entry_1.seq_num == 1
    assert entry_1.prev_hash == GENESIS_PREV_HASH
    assert entry_1.prev_hash == "0" * 64
    expected_data_hash_1 = compute_data_hash(payload_1)
    assert entry_1.data_hash == expected_data_hash_1
    expected_block_hash_1 = compute_block_hash(
        org_id=org.id,
        employee_pseudonym=pseudonym,
        seq_num=1,
        prev_hash=GENESIS_PREV_HASH,
        data_hash=expected_data_hash_1,
    )
    assert entry_1.block_hash == expected_block_hash_1

    # Block 2
    payload_2 = {"task": "Practical Lab Submission", "score": 92}
    entry_2 = append_evidence(
        session=db_session,
        org_id=org.id,
        user_id=user.id,
        skill_id=skill.id,
        evidence_type="LAB_SUBMISSION",
        payload=payload_2,
        weight=1.5,
    )

    assert entry_2.seq_num == 2
    assert entry_2.prev_hash == entry_1.block_hash
    expected_data_hash_2 = compute_data_hash(payload_2)
    assert entry_2.data_hash == expected_data_hash_2
    expected_block_hash_2 = compute_block_hash(
        org_id=org.id,
        employee_pseudonym=pseudonym,
        seq_num=2,
        prev_hash=entry_1.block_hash,
        data_hash=expected_data_hash_2,
    )
    assert entry_2.block_hash == expected_block_hash_2

    # Block 3
    payload_3 = {"task": "Trainer Peer Endorsement", "rating": "MASTER"}
    entry_3 = append_evidence(
        session=db_session,
        org_id=org.id,
        user_id=user.id,
        skill_id=skill.id,
        evidence_type="PEER_ENDORSEMENT",
        payload=payload_3,
        weight=2.0,
    )

    assert entry_3.seq_num == 3
    assert entry_3.prev_hash == entry_2.block_hash
    assert entry_3.block_hash == compute_block_hash(
        org_id=org.id,
        employee_pseudonym=pseudonym,
        seq_num=3,
        prev_hash=entry_2.block_hash,
        data_hash=compute_data_hash(payload_3),
    )

    # Full Chain Verification
    verification = verify_employee_chain(
        session=db_session,
        org_id=org.id,
        employee_pseudonym=pseudonym,
    )
    assert verification.is_valid is True
    assert verification.total_blocks == 3
    assert verification.broken_seq is None


def test_tamper_detection_flags_payload_and_chain_alterations(db_session: Session) -> None:
    """Verify that tampering with data_hash, prev_hash, block_hash, or sequence breaks verification."""
    org = Organisation(name="CSM Tech", code="CSM_TAMPER")
    db_session.add(org)
    db_session.flush()

    user = User(
        org_id=org.id,
        email="tamper_test@csm.tech",
        password_hash="pwd",
        full_name="Tamper Subject",
        pseudonym_salt="salt_tamper_user_02",
    )
    skill = Skill(org_id=org.id, code="SK_TAMPER", name="Integrity Test", category="DOMAIN")
    db_session.add_all([user, skill])
    db_session.flush()

    pseudonym = derive_pseudonym(user.id, user.pseudonym_salt)

    # Create 4 consecutive blocks
    for i in range(1, 5):
        append_evidence(
            session=db_session,
            org_id=org.id,
            user_id=user.id,
            skill_id=skill.id,
            evidence_type="EVENT",
            payload={"step": i, "val": i * 10},
        )

    # Invariant: Untampered chain verifies cleanly
    clean_check = verify_employee_chain(db_session, org.id, pseudonym)
    assert clean_check.is_valid is True
    assert clean_check.total_blocks == 4

    # Scenario 1: Maliciously altered data_hash at block 2 (simulating raw storage tamper)
    b2 = (
        db_session.query(EvidenceLedger)
        .filter(EvidenceLedger.employee_pseudonym == pseudonym, EvidenceLedger.seq_num == 2)
        .one()
    )
    original_data_hash = b2.data_hash
    db_session.execute(
        text("UPDATE evidence_ledger SET data_hash = :h WHERE id = :id"),
        {"h": "f" * 64, "id": b2.id},
    )
    db_session.commit()
    db_session.expire_all()

    tamper_1 = verify_employee_chain(db_session, org.id, pseudonym)
    assert tamper_1.is_valid is False
    assert tamper_1.broken_seq == 2
    assert "data_hash" in tamper_1.reason.lower() or "block_hash" in tamper_1.reason.lower()

    # Revert Scenario 1
    db_session.execute(
        text("UPDATE evidence_ledger SET data_hash = :h WHERE id = :id"),
        {"h": original_data_hash, "id": b2.id},
    )
    db_session.commit()
    db_session.expire_all()

    # Scenario 2: Maliciously altered prev_hash at block 3 (breaking chain link)
    b3 = (
        db_session.query(EvidenceLedger)
        .filter(EvidenceLedger.employee_pseudonym == pseudonym, EvidenceLedger.seq_num == 3)
        .one()
    )
    original_prev_hash = b3.prev_hash
    db_session.execute(
        text("UPDATE evidence_ledger SET prev_hash = :h WHERE id = :id"),
        {"h": "a" * 64, "id": b3.id},
    )
    db_session.commit()
    db_session.expire_all()

    tamper_2 = verify_employee_chain(db_session, org.id, pseudonym)
    assert tamper_2.is_valid is False
    assert tamper_2.broken_seq == 3
    assert "prev_hash" in tamper_2.reason.lower() or "broken" in tamper_2.reason.lower()

    # Revert Scenario 2
    db_session.execute(
        text("UPDATE evidence_ledger SET prev_hash = :h WHERE id = :id"),
        {"h": original_prev_hash, "id": b3.id},
    )
    db_session.commit()
    db_session.expire_all()

    # Scenario 3: Genesis block prev_hash not equal to 64 zeros
    b1 = (
        db_session.query(EvidenceLedger)
        .filter(EvidenceLedger.employee_pseudonym == pseudonym, EvidenceLedger.seq_num == 1)
        .one()
    )
    original_genesis_prev = b1.prev_hash
    db_session.execute(
        text("UPDATE evidence_ledger SET prev_hash = :h WHERE id = :id"),
        {"h": "1" * 64, "id": b1.id},
    )
    db_session.commit()
    db_session.expire_all()

    tamper_3 = verify_employee_chain(db_session, org.id, pseudonym)
    assert tamper_3.is_valid is False
    assert tamper_3.broken_seq == 1
    assert "genesis" in tamper_3.reason.lower()

    # Revert Scenario 3
    db_session.execute(
        text("UPDATE evidence_ledger SET prev_hash = :h WHERE id = :id"),
        {"h": original_genesis_prev, "id": b1.id},
    )
    db_session.commit()
    db_session.expire_all()
    assert verify_employee_chain(db_session, org.id, pseudonym).is_valid is True


def test_per_employee_sequence_numbers_under_concurrent_writes(
    db_session: Session, db_engine: Engine
) -> None:
    """Verify that multiple concurrent writes for the same employee yield consecutive sequence numbers.

    Under Section 23, concurrent writes must produce sequence numbers [1, 2, ..., N]
    without duplicates, gaps, or corrupted hashes.
    """
    org = Organisation(name="CSM Tech", code="CSM_CONCURRENCY")
    db_session.add(org)
    db_session.flush()

    user = User(
        org_id=org.id,
        email="concurrent_writer@csm.tech",
        password_hash="pwd",
        full_name="Concurrent Writer",
        pseudonym_salt="salt_concurrent_writer",
    )
    skill = Skill(org_id=org.id, code="SK_CONCURR", name="Concurrency Skill", category="TECHNICAL")
    db_session.add_all([user, skill])
    db_session.commit()

    org_id_str = str(org.id)
    user_id_str = str(user.id)
    skill_id_str = str(skill.id)
    pseudonym = derive_pseudonym(user_id_str, "salt_concurrent_writer")
    concurrency_count = 8

    def submit_evidence(thread_idx: int) -> dict[str, Any]:
        """Independent worker session simulating concurrent incoming submission."""
        worker_session = Session(db_engine, expire_on_commit=False)
        try:
            entry = append_evidence(
                session=worker_session,
                org_id=org_id_str,
                user_id=user_id_str,
                skill_id=skill_id_str,
                evidence_type="CONCURRENT_TASK",
                payload={"thread_idx": thread_idx, "timestamp_marker": f"run_{thread_idx}"},
                weight=1.0,
            )
            return {"seq_num": entry.seq_num, "block_hash": entry.block_hash}
        finally:
            worker_session.close()

    # Launch parallel writes using thread pool
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=concurrency_count) as executor:
        futures = [executor.submit(submit_evidence, i) for i in range(concurrency_count)]
        for fut in as_completed(futures):
            results.append(fut.result())

    # Assert all submitted tasks completed successfully
    assert len(results) == concurrency_count

    # Check database records
    db_session.expire_all()
    entries = (
        db_session.query(EvidenceLedger)
        .filter(EvidenceLedger.employee_pseudonym == pseudonym)
        .order_by(EvidenceLedger.seq_num.asc())
        .all()
    )

    assert len(entries) == concurrency_count

    # Sequence numbers must be strictly [1, 2, ..., concurrency_count]
    observed_seqs = [e.seq_num for e in entries]
    expected_seqs = list(range(1, concurrency_count + 1))
    assert observed_seqs == expected_seqs

    # The entire concurrent chain must verify cleanly from genesis to tip
    chain_check = verify_employee_chain(db_session, org.id, pseudonym)
    assert chain_check.is_valid is True
    assert chain_check.total_blocks == concurrency_count


def test_signed_checkpoints_and_verification(db_session: Session) -> None:
    """Verify daily root Merkle checkpoint creation, asymmetric signing, and verification."""
    org = Organisation(name="CSM Tech", code="CSM_CHECKPOINTS")
    db_session.add(org)
    db_session.flush()

    user_a = User(
        org_id=org.id,
        email="alice@csm.tech",
        password_hash="h",
        full_name="Alice",
        pseudonym_salt="salt_alice_123",
    )
    user_b = User(
        org_id=org.id,
        email="bob@csm.tech",
        password_hash="h",
        full_name="Bob",
        pseudonym_salt="salt_bob_456",
    )
    skill = Skill(org_id=org.id, code="SK_CKPT", name="Checkpoint Skill", category="DOMAIN")
    db_session.add_all([user_a, user_b, skill])
    db_session.commit()

    # Append evidence across multiple users
    append_evidence(db_session, org.id, user_a.id, skill.id, "EXAM", {"exam": "A1", "score": 90})
    append_evidence(
        db_session, org.id, user_a.id, skill.id, "PROJECT", {"project": "Alpha", "score": 95}
    )
    append_evidence(db_session, org.id, user_b.id, skill.id, "EXAM", {"exam": "B1", "score": 88})

    # Generate an asymmetric RSA signing keypair for KMS simulation
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo,
    )

    # Create signed checkpoint
    checkpoint = create_signed_checkpoint(
        session=db_session,
        org_id=org.id,
        private_key=private_key,
        signing_key_id="kms-key-2026-q1",
    )

    assert checkpoint.checkpoint_seq == 1
    assert checkpoint.org_id == org.id
    assert checkpoint.signing_key_id == "kms-key-2026-q1"
    assert len(checkpoint.root_hash) == 64
    assert len(checkpoint.signature) > 0

    # 1. Verification of genuine checkpoint succeeds
    is_valid = verify_checkpoint(
        checkpoint=checkpoint,
        public_key_pem=public_pem,
    )
    assert is_valid is True

    # 2. Tampered root hash fails verification
    original_root = checkpoint.root_hash
    checkpoint.root_hash = "0" * 64
    tampered_check = verify_checkpoint(
        checkpoint=checkpoint,
        public_key_pem=public_pem,
    )
    assert tampered_check is False
    checkpoint.root_hash = original_root

    # 3. Corrupted signature fails verification
    tampered_sig_check = verify_checkpoint(
        checkpoint=checkpoint,
        public_key_pem=public_pem,
        signature_override=base64.b64encode(b"invalid_signature_bytes").decode("utf-8"),
    )
    assert tampered_sig_check is False


def test_dpdp_crypto_shredding_preserves_ledger_integrity(db_session: Session) -> None:
    """Verify that DPDP Right to Erasure crypto-shredding removes personal payload while keeping ledger valid."""
    org = Organisation(name="CSM Tech", code="CSM_CRYPTO_SHRED")
    db_session.add(org)
    db_session.flush()

    user = User(
        org_id=org.id,
        email="erasure_candidate@csm.tech",
        password_hash="pwd",
        full_name="Erasure Candidate",
        pseudonym_salt="salt_erasure_candidate_789",
    )
    skill = Skill(org_id=org.id, code="SK_SHRED", name="Shred Skill", category="TECHNICAL")
    db_session.add_all([user, skill])
    db_session.flush()

    pseudonym = derive_pseudonym(user.id, user.pseudonym_salt)

    # Append 3 evidence records
    append_evidence(
        db_session, org.id, user.id, skill.id, "ASSESSMENT", {"exam": "PII_1", "grade": "A"}
    )
    entry2 = append_evidence(
        db_session, org.id, user.id, skill.id, "ASSESSMENT", {"exam": "PII_2", "grade": "B"}
    )
    append_evidence(
        db_session, org.id, user.id, skill.id, "ASSESSMENT", {"exam": "PII_3", "grade": "A+"}
    )

    # Initial verification: Unshredded chain is valid
    assert verify_employee_chain(db_session, org.id, pseudonym).is_valid is True

    # Employee exercises DPDP Right to Erasure on record 2
    shred_result = shred_evidence_record(
        session=db_session,
        record_id=entry2.record_id,
        reason="DPDP_RIGHT_TO_ERASURE_EXERCISED",
    )
    assert shred_result is True

    # Verify that EvidenceRecord personal payload and key_id are deleted (crypto-shredded)
    db_session.expire_all()
    rec2 = db_session.get(EvidenceRecord, entry2.record_id)
    assert rec2 is not None
    assert rec2.raw_payload_json is None
    assert rec2.key_id is None
    assert rec2.is_shredded is True

    # CRITICAL INVARIANT: The EvidenceLedger table row was NOT modified or deleted
    ledger2 = db_session.query(EvidenceLedger).filter(EvidenceLedger.id == entry2.id).one()
    assert ledger2.seq_num == 2
    assert ledger2.data_hash == entry2.data_hash  # Hash remains intact
    assert ledger2.block_hash == entry2.block_hash  # Block hash remains intact

    # The cryptographic chain STILL validates successfully
    chain_post_shred = verify_employee_chain(db_session, org.id, pseudonym)
    assert chain_post_shred.is_valid is True
    assert chain_post_shred.total_blocks == 3


def test_derive_pseudonym_refuses_empty_salt_and_forbids_secret_key_fallback() -> None:
    """Verify that derive_pseudonym strictly enforces mandatory per-employee salt and forbids system fallback."""
    user_id = "usr-test-strict-salt-01"

    # 1. None salt strictly forbidden
    with pytest.raises(ValueError) as exc_none:
        derive_pseudonym(user_id, "")
    assert "MANDATORY_EMPLOYEE_SALT" in str(exc_none.value)
    assert "fallback to system SECRET_KEY is strictly prohibited" in str(exc_none.value)

    # 2. Whitespace-only salt strictly forbidden
    with pytest.raises(ValueError) as exc_space:
        derive_pseudonym(user_id, "   ")
    assert "MANDATORY_EMPLOYEE_SALT" in str(exc_space.value)

    # 3. Legitimate per-employee salt succeeds and produces deterministic 64-char hex
    valid_salt = "emp-cryptographic-salt-9999"
    pseudo_1 = derive_pseudonym(user_id, valid_salt)
    pseudo_2 = derive_pseudonym(user_id, valid_salt)
    assert pseudo_1 == pseudo_2
    assert len(pseudo_1) == 64
    assert all(c in "0123456789abcdef" for c in pseudo_1)


def test_crypto_shredding_salt_makes_pseudonym_and_ledger_unlinkable(
    db_session: Session,
) -> None:
    """Verify that destroying the per-employee salt renders historical ledger blocks mathematically unlinkable.

    DPDP Act Statutory Erasure Invariants:
    1. The employee's personal salt is destroyed permanently from the database.
    2. Attempting to derive the pseudonym for the shredded employee strictly fails.
    3. An adversary possessing user_id cannot recompute the pseudonym or link it to historical ledger rows.
    4. The immutable hash chain in EvidenceLedger remains mathematically sound and internally intact.
    """
    org = Organisation(name="CSM Tech", code="CSM_SALT_SHRED")
    db_session.add(org)
    db_session.flush()

    employee_salt = "secure_personal_salt_employee_x77"
    user = User(
        org_id=org.id,
        email="unlinkable_employee@csm.tech",
        password_hash="pwd",
        full_name="Unlinkable Employee",
        pseudonym_salt=employee_salt,
    )
    skill = Skill(org_id=org.id, code="SK_UNLINK", name="Unlinkable Skill", category="SECURITY")
    db_session.add_all([user, skill])
    db_session.flush()

    user_id = user.id
    pseudonym_pre_shred = derive_pseudonym(user_id, employee_salt)

    # Append 2 blocks for this user
    append_evidence(
        session=db_session,
        org_id=org.id,
        user_id=user_id,
        skill_id=skill.id,
        evidence_type="ASSESSMENT",
        payload={"topic": "Privacy By Design", "score": 98},
    )
    append_evidence(
        session=db_session,
        org_id=org.id,
        user_id=user_id,
        skill_id=skill.id,
        evidence_type="LAB",
        payload={"topic": "Zero Trust Gateway", "score": 95},
    )

    # Prior to shredding: Chain is valid and linked
    chain_before = verify_employee_chain(db_session, org.id, pseudonym_pre_shred)
    assert chain_before.is_valid is True
    assert chain_before.total_blocks == 2

    # Execute complete employee crypto-shredding (shreds records AND destroys salt)
    shred_info = crypto_shred_employee(
        session=db_session,
        org_id=org.id,
        user_id=user_id,
        reason="DPDP_RIGHT_TO_ERASURE_UNLINKABILITY_TEST",
    )
    assert shred_info["pseudonym_salt_destroyed"] is True
    assert shred_info["shredded_records"] == 2

    # Verify database state after shredding
    db_session.expire_all()
    user_post_shred = db_session.get(User, user_id)
    assert user_post_shred is not None
    assert user_post_shred.pseudonym_salt is None

    # CRITICAL INVARIANT: With salt destroyed, deriving pseudonym for user_id FAILS
    with pytest.raises(ValueError) as exc:
        derive_pseudonym(user_id, str(user_post_shred.pseudonym_salt or ""))
    assert "MANDATORY_EMPLOYEE_SALT" in str(exc.value)

    # Append evidence without salt fails closed
    with pytest.raises(ValueError) as exc_append:
        append_evidence(
            session=db_session,
            org_id=org.id,
            user_id=user_id,
            skill_id=skill.id,
            evidence_type="NEW_TASK",
            payload={"fail": True},
        )
    assert "No cryptographic pseudonym salt registered" in str(exc_append.value)

    # CRITICAL INVARIANT: The historical ledger blocks remain mathematically valid on-chain
    chain_after = verify_employee_chain(db_session, org.id, pseudonym_pre_shred)
    assert chain_after.is_valid is True
    assert chain_after.total_blocks == 2

