"""Automated tests proving Database Immutability Invariant for Audit Logs & Evidence Ledgers."""

from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models import (
    AccessReceipt,
    AuditLog,
    Base,
    EvidenceLedger,
    EvidenceRecord,
    Organisation,
    Skill,
    User,
)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Fixture providing an ephemeral in-memory SQLite database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


def test_audit_log_insert_succeeds(db_session: Session) -> None:
    """Verify that inserting a new immutable audit record succeeds."""
    org = Organisation(name="CSM Tech", code="CSM_TEST")
    db_session.add(org)
    db_session.commit()

    entry = AuditLog(
        org_id=org.id,
        action="login",
        resource="users",
        resource_id="usr_123",
        ip_address="127.0.0.1",
        reason="User authenticated",
    )
    db_session.add(entry)
    db_session.commit()

    saved = db_session.get(AuditLog, entry.id)
    assert saved is not None
    assert saved.action == "login"
    assert saved.org_id == org.id


def test_audit_log_update_raises_immutability_error(db_session: Session) -> None:
    """Verify that attempting to UPDATE an existing AuditLog record is strictly refused."""
    org = Organisation(name="CSM Tech", code="CSM_TEST_2")
    db_session.add(org)
    db_session.commit()

    entry = AuditLog(
        org_id=org.id,
        action="login",
        resource="users",
        resource_id="usr_123",
    )
    db_session.add(entry)
    db_session.commit()

    # Attempt to tamper with the audit row
    entry.action = "tampered_login"
    with pytest.raises(PermissionError) as exc_info:
        db_session.flush()

    assert "IMMUTABILITY_VIOLATION" in str(exc_info.value)
    assert "audit_log" in str(exc_info.value)
    assert "UPDATE operations are strictly forbidden" in str(exc_info.value)


def test_audit_log_delete_raises_immutability_error(db_session: Session) -> None:
    """Verify that attempting to DELETE an existing AuditLog record is strictly refused."""
    org = Organisation(name="CSM Tech", code="CSM_TEST_3")
    db_session.add(org)
    db_session.commit()

    entry = AuditLog(
        org_id=org.id,
        action="delete_request",
        resource="users",
        resource_id="usr_999",
    )
    db_session.add(entry)
    db_session.commit()

    # Attempt to delete the audit row
    db_session.delete(entry)
    with pytest.raises(PermissionError) as exc_info:
        db_session.flush()

    assert "IMMUTABILITY_VIOLATION" in str(exc_info.value)
    assert "audit_log" in str(exc_info.value)
    assert "DELETE operations are strictly forbidden" in str(exc_info.value)


def test_access_receipt_immutability(db_session: Session) -> None:
    """Verify that AccessReceipt records cannot be updated or deleted."""
    org = Organisation(name="CSM Tech", code="CSM_TEST_4")
    db_session.add(org)
    db_session.commit()

    u1 = User(org_id=org.id, email="u1@csm.tech", password_hash="hash", full_name="User One")
    u2 = User(org_id=org.id, email="u2@csm.tech", password_hash="hash", full_name="User Two")
    db_session.add_all([u1, u2])
    db_session.commit()

    receipt = AccessReceipt(
        org_id=org.id,
        accessor_id=u1.id,
        subject_id=u2.id,
        resource_type="growth_ring",
        purpose="1:1 review",
    )
    db_session.add(receipt)
    db_session.commit()

    # Attempt update
    receipt.purpose = "tampered purpose"
    with pytest.raises(PermissionError) as exc_info:
        db_session.flush()
    assert "access_receipts" in str(exc_info.value)

    # Rollback to clean state
    db_session.rollback()

    # Attempt delete
    saved_receipt = db_session.get(AccessReceipt, receipt.id)
    assert saved_receipt is not None
    db_session.delete(saved_receipt)
    with pytest.raises(PermissionError) as exc_info:
        db_session.flush()
    assert "access_receipts" in str(exc_info.value)


def test_evidence_ledger_immutability(db_session: Session) -> None:
    """Verify that EvidenceLedger hash chain rows cannot be updated or deleted."""
    org = Organisation(name="CSM Tech", code="CSM_TEST_5")
    db_session.add(org)
    db_session.commit()

    user = User(org_id=org.id, email="emp@csm.tech", password_hash="hash", full_name="Learner")
    skill = Skill(org_id=org.id, code="PYTHON_L1", name="Python Core", category="TECHNICAL")
    db_session.add_all([user, skill])
    db_session.commit()

    record = EvidenceRecord(
        org_id=org.id,
        user_id=user.id,
        skill_id=skill.id,
        evidence_type="ASSESSMENT_ATTEMPT",
        weight=1.0,
    )
    db_session.add(record)
    db_session.commit()

    ledger = EvidenceLedger(
        org_id=org.id,
        employee_pseudonym="pseudo_abc123",
        seq_num=1,
        prev_hash="0" * 64,
        data_hash="a" * 64,
        block_hash="b" * 64,
        record_id=record.id,
    )
    db_session.add(ledger)
    db_session.commit()

    # Attempt update
    ledger.prev_hash = "f" * 64
    with pytest.raises(PermissionError) as exc_info:
        db_session.flush()
    assert "evidence_ledger" in str(exc_info.value)

    db_session.rollback()

    # Attempt delete
    saved_ledger = db_session.get(EvidenceLedger, ledger.id)
    assert saved_ledger is not None
    db_session.delete(saved_ledger)
    with pytest.raises(PermissionError) as exc_info:
        db_session.flush()
    assert "evidence_ledger" in str(exc_info.value)


def test_standard_entities_allow_mutations(db_session: Session) -> None:
    """Verify that standard mutable entities (User, Organisation, Skill) permit updates and deletes."""
    org = Organisation(name="Mutable Org", code="MUT_ORG")
    db_session.add(org)
    db_session.commit()

    org.name = "Updated Org Name"
    db_session.flush()
    db_session.commit()

    updated = db_session.get(Organisation, org.id)
    assert updated is not None
    assert updated.name == "Updated Org Name"

    # Deletion should also succeed
    db_session.delete(updated)
    db_session.flush()
    db_session.commit()

    assert db_session.get(Organisation, org.id) is None
