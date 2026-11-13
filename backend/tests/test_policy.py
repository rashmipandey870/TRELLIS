"""Automated tests validating Centralized Policy Engine (can()) and Default-Deny enforcement."""

from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.audit_middleware import record_access_receipt
from app.core.policy import UserContext, can
from app.models import AccessReceipt, Base


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


def test_strict_default_deny() -> None:
    """Verify that any unlisted tuple is strictly forbidden under Default-Deny."""
    user = UserContext(user_id="usr_01", org_id="org_csm", roles=["EMPLOYEE"])

    # Unlisted resources and actions
    assert can(user, "destroy", "infrastructure") is False
    assert can(user, "drop_table", "users") is False
    assert can(user, "bypass", "audit_log") is False
    assert can(user, "read", "unknown_resource") is False


def test_employee_own_scope_permissions() -> None:
    """Verify that EMPLOYEE can read/update OWN data but is denied for other users."""
    emp = UserContext(user_id="emp_priya", org_id="org_csm", roles=["EMPLOYEE"])

    # Reading own profile is allowed
    assert can(emp, "read", "users", {"target_user_id": "emp_priya"}) is True
    # Reading another employee's profile directly is denied
    assert can(emp, "read", "users", {"target_user_id": "emp_aarav"}) is False

    # Updating own preferences is allowed
    assert can(emp, "update", "users", {"target_user_id": "emp_priya"}) is True
    # Updating another user's preferences is denied
    assert can(emp, "update", "users", {"target_user_id": "emp_aarav"}) is False

    # Consent management
    assert can(emp, "create", "consents", {"target_user_id": "emp_priya"}) is True
    assert can(emp, "update", "consents", {"target_user_id": "emp_priya"}) is True


def test_separation_of_duties_author_self_approval_forbidden() -> None:
    """INVARIANT: Authors cannot self-approve their own submissions (Separation of Duties)."""
    trainer = UserContext(
        user_id="tr_rahul", org_id="org_csm", roles=["TRAINER_MENTOR"], cohort_id="cohort_alpha"
    )

    # Trainer approving an idea from a cohort learner: ALLOWED
    assert (
        can(
            trainer,
            "approve",
            "greenhouse_ideas",
            {"author_id": "emp_learner_01", "cohort_id": "cohort_alpha"},
        )
        is True
    )

    # Trainer attempting to approve their OWN idea: FORBIDDEN
    assert (
        can(
            trainer,
            "approve",
            "greenhouse_ideas",
            {"author_id": "tr_rahul", "cohort_id": "cohort_alpha"},
        )
        is False
    )


def test_trainer_blind_grading_scope() -> None:
    """Verify that TRAINER_MENTOR can grade responses under blind grading scope."""
    trainer = UserContext(user_id="tr_vikram", org_id="org_csm", roles=["TRAINER_MENTOR"])
    assert can(trainer, "grade", "responses") is True


def test_manager_team_direct_scope() -> None:
    """Verify that MANAGER can access direct reports but is denied for non-reports."""
    mgr = UserContext(user_id="mgr_sunita", org_id="org_csm", roles=["MANAGER"])

    # Accessing direct report's growth ring: ALLOWED
    assert can(mgr, "read", "growth_ring", {"is_direct_report": True}) is True

    # Accessing non-direct report's growth ring: FORBIDDEN
    assert (
        can(
            mgr,
            "read",
            "growth_ring",
            {"is_direct_report": False, "target_user_id": "other_emp"},
        )
        is False
    )


def test_super_admin_immutability_invariants() -> None:
    """INVARIANT: Super admin CANNOT update or delete audit_log or evidence_ledger."""
    super_admin = UserContext(user_id="admin_root", org_id="org_csm", roles=["SUPER_ADMIN"])

    # Super admin cannot alter audit logs
    assert can(super_admin, "update", "audit_log") is False
    assert can(super_admin, "delete", "audit_log") is False

    # Super admin cannot alter evidence ledger hash chains
    assert can(super_admin, "update", "evidence_ledger") is False
    assert can(super_admin, "delete", "evidence_ledger") is False


def test_access_receipt_recording(db_session: Session) -> None:
    """Verify that cross-user data access generates an immutable Access Receipt."""
    receipt = record_access_receipt(
        session=db_session,
        org_id="org_csm",
        accessor_id="mgr_sunita",
        subject_id="emp_priya",
        resource_type="growth_ring",
        purpose="Quarterly Career Growth Review",
    )

    assert receipt.id is not None
    assert receipt.accessor_id == "mgr_sunita"
    assert receipt.subject_id == "emp_priya"
    assert receipt.purpose == "Quarterly Career Growth Review"

    saved = db_session.get(AccessReceipt, receipt.id)
    assert saved is not None
    assert saved.resource_type == "growth_ring"
