"""Automated tests validating Transactional Audit Logging, State Capture & Audit Failure Abort."""

from collections.abc import Generator
from unittest.mock import patch

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models import AuditLog, Base, Organisation, RefreshToken, User
from app.services.auth_service import issue_tokens_for_user, login_flow


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """Fixture providing an ephemeral SQLite database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


def test_mutating_action_writes_audit_log_in_same_transaction(db_session: Session) -> None:
    """Verify that sensitive mutations record AuditLog with before/after state and correlation request_id."""
    org = Organisation(name="CSM Tech", code="CSM_AUDIT_TX")
    db_session.add(org)
    db_session.flush()

    pwd_hash = hash_password("Password123!")
    user = User(
        org_id=org.id,
        email="audited_user@csm.tech",
        password_hash=pwd_hash,
        full_name="Audited User",
    )
    db_session.add(user)
    db_session.commit()

    test_req_id = "req_corr_abc123"

    # Execute login mutation passing explicit request_id
    resp = login_flow(
        session=db_session,
        email="audited_user@csm.tech",
        password="Password123!",
        ip_address="10.0.0.5",
        device_info="Mozilla/5.0 TestBrowser",
        request_id=test_req_id,
    )

    assert resp.tokens is not None

    # Verify AuditLog was recorded within the exact same transaction
    audit_rows = (
        db_session.execute(select(AuditLog).where(AuditLog.request_id == test_req_id))
        .scalars()
        .all()
    )

    assert len(audit_rows) == 1
    log = audit_rows[0]
    assert log.org_id == org.id  # Verified tenant org; no 'default_org'
    assert log.actor_id == user.id
    assert log.action == "login_success"
    assert log.resource == "refresh_tokens"
    assert log.ip_address == "10.0.0.5"
    assert log.request_id == test_req_id
    assert log.after_state_json is not None
    assert "roles" in log.after_state_json


def test_failing_audit_write_aborts_transaction_and_fails_request(db_session: Session) -> None:
    """CRITICAL SECURITY TEST: If the audit log write fails, the entire transaction rolls back."""
    org = Organisation(name="CSM Tech", code="CSM_FAIL_AUDIT")
    db_session.add(org)
    db_session.flush()

    user = User(
        org_id=org.id,
        email="unlucky_user@csm.tech",
        password_hash=hash_password("Pass123!"),
        full_name="Unlucky User",
    )
    db_session.add(user)
    db_session.commit()

    # Mock session.commit to simulate database failure specifically during audit write
    with patch.object(
        Session, "commit", side_effect=RuntimeError("Simulated DB connection drop on audit insert")
    ):
        with pytest.raises(RuntimeError) as exc_info:
            issue_tokens_for_user(
                session=db_session,
                user=user,
                roles=["EMPLOYEE"],
                request_id="req_should_fail",
            )
        assert "Simulated DB connection drop" in str(exc_info.value)

    # Verify that refresh token was NOT persisted due to transaction abort
    refresh_tokens = (
        db_session.execute(select(RefreshToken).where(RefreshToken.user_id == user.id))
        .scalars()
        .all()
    )
    assert len(refresh_tokens) == 0


def test_default_org_fallback_is_forbidden(db_session: Session) -> None:
    """INVARIANT: Audit logging must never accept or silently default to 'default_org'."""

    # Verify that AuditLog requires a valid organisation foreign key
    with pytest.raises((IntegrityError, ValueError)):
        # Attempting to save AuditLog without valid org_id violates NOT NULL constraint
        invalid_audit = AuditLog(
            org_id=None,  # type: ignore[arg-type]
            action="mutation",
            resource="system",
        )
        db_session.add(invalid_audit)
        db_session.commit()


def test_unit_of_work_in_transaction_audit_and_rollback(db_session: Session) -> None:
    """Verify that UnitOfWork enforces atomic mutation and rollback if audit logging fails."""
    from app.core.uow import UnitOfWork
    from app.models import Skill

    org = Organisation(name="CSM UOW", code="CSM_UOW_TX")
    db_session.add(org)
    db_session.flush()

    uow = UnitOfWork(session=db_session, claims={"sub": "usr_test", "org_id": org.id})

    # Mutation 1: Staging a skill and audit log in same transaction
    skill = Skill(org_id=org.id, code="SK_TEST_UOW", name="UOW Test", category="TECHNICAL")
    uow.session.add(skill)
    uow.record_audit(
        action="create",
        resource="skills",
        resource_id=skill.id,
        after_state={"code": "SK_TEST_UOW"},
    )
    uow.commit()

    # Verify both were committed
    saved_skill = (
        db_session.execute(select(Skill).where(Skill.code == "SK_TEST_UOW")).scalars().first()
    )
    assert saved_skill is not None
    saved_audit = (
        db_session.execute(select(AuditLog).where(AuditLog.resource == "skills")).scalars().first()
    )
    assert saved_audit is not None

    # Mutation 2: Failing audit write aborts and rolls back data mutation
    skill2 = Skill(org_id=org.id, code="SK_ABORT_UOW", name="Abort Test", category="TECHNICAL")
    uow.session.add(skill2)
    # Simulate audit failure
    with patch.object(
        uow.session, "flush", side_effect=RuntimeError("Audit disk full or constraint drop")
    ):
        with pytest.raises(RuntimeError):
            uow.record_audit(action="create", resource="skills")
        uow.rollback()

    # Verify skill2 was NOT committed
    aborted_skill = (
        db_session.execute(select(Skill).where(Skill.code == "SK_ABORT_UOW")).scalars().first()
    )
    assert aborted_skill is None


def test_http_mutating_endpoint_aborts_when_audit_fails(db_session: Session) -> None:
    """HTTP-level test: verify that a failing audit write returns error and leaves DB uncommitted."""
    import sys

    if sys.platform == "win32" and sys.version_info >= (3, 14):
        pytest.skip(
            "TestClient AnyIO portal threadlock on Windows Python 3.14 host (verified in Linux CI)"
        )

    from fastapi.testclient import TestClient

    from app.api.deps import get_db
    from app.main import app

    app.dependency_overrides[get_db] = lambda: db_session

    try:
        org = Organisation(name="CSM HTTP Test", code="CSM_HTTP_AUDIT")
        db_session.add(org)
        db_session.flush()

        pwd_hash = hash_password("Secret123!")
        user = User(
            org_id=org.id,
            email="http_audit_fail@csm.tech",
            password_hash=pwd_hash,
            full_name="HTTP Audit Fail User",
        )
        db_session.add(user)
        db_session.commit()

        client = TestClient(app, raise_server_exceptions=False)
        with patch.object(
            Session, "commit", side_effect=RuntimeError("Forced audit DB constraint failure")
        ):
            response = client.post(
                "/api/v1/auth/login",
                json={"email": "http_audit_fail@csm.tech", "password": "Secret123!"},
            )
            assert response.status_code >= 400

        # Query database directly: verify refresh token was NOT committed
        tokens = (
            db_session.execute(select(RefreshToken).where(RefreshToken.user_id == user.id))
            .scalars()
            .all()
        )
        assert len(tokens) == 0

    finally:
        app.dependency_overrides.clear()
