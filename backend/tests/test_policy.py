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
    """Verify that TRAINER_MENTOR can grade responses under strict blind grading scope without PII."""
    trainer = UserContext(user_id="tr_vikram", org_id="org_csm", roles=["TRAINER_MENTOR"])

    # Negative test 1: Missing blind grading context returns False
    assert can(trainer, "grade", "responses", {}) is False

    # Negative test 2: Identifying candidate name in context returns False (PII breach)
    assert (
        can(
            trainer,
            "grade",
            "responses",
            {
                "is_blind_grading": True,
                "anonymized": True,
                "candidate_name": "Priya Sharma",
            },
        )
        is False
    )

    # Negative test 3: Identifying employee code in context returns False
    assert (
        can(
            trainer,
            "grade",
            "responses",
            {
                "is_blind_grading": True,
                "anonymized": True,
                "employee_code": "CSM-1029",
            },
        )
        is False
    )

    # Positive test: Truly anonymized context with no PII keys returns True
    assert (
        can(
            trainer,
            "grade",
            "responses",
            {
                "is_blind_grading": True,
                "anonymized": True,
            },
        )
        is True
    )


def test_anonymized_aggregate_scope_enforces_k_anonymity() -> None:
    """Verify that aggregate reports enforce k-anonymity (k >= 5) and forbid individual user IDs."""
    clo = UserContext(user_id="clo_deepak", org_id="org_csm", roles=["LK_HEAD_CLO"])

    # Negative test 1: Small group size (sample_size < 5) is rejected
    assert (
        can(
            clo,
            "read",
            "growth_ring",
            {
                "is_aggregate": True,
                "anonymized": True,
                "sample_size": 3,
            },
        )
        is False
    )

    # Negative test 2: Sample size >= 5 but individual user identifier present is rejected
    assert (
        can(
            clo,
            "read",
            "growth_ring",
            {
                "is_aggregate": True,
                "anonymized": True,
                "sample_size": 10,
                "target_user_id": "emp_identified_01",
            },
        )
        is False
    )

    # Positive test: Sample size >= 5, anonymized, and no PII passes
    assert (
        can(
            clo,
            "read",
            "growth_ring",
            {
                "is_aggregate": True,
                "anonymized": True,
                "sample_size": 12,
            },
        )
        is True
    )


def test_organization_scope_rejects_cross_tenant_access() -> None:
    """Verify that ORGANIZATION scope strictly compares target entity org_id with subject org_id."""
    emp = UserContext(user_id="emp_csm_01", org_id="org_csm", roles=["EMPLOYEE"])

    # Negative test: Target resource belongs to another tenant organisation
    assert (
        can(
            emp,
            "read",
            "skills",
            {"target_org_id": "org_external_tenant"},
        )
        is False
    )

    # Positive test: Target resource matches subject tenant organisation
    assert (
        can(
            emp,
            "read",
            "skills",
            {"target_org_id": "org_csm"},
        )
        is True
    )


def test_server_side_db_entity_context_resolution(db_session: Session) -> None:
    """Verify that entity context (org_id, direct report, author) is derived from the database."""
    from app.core.policy import resolve_server_side_context
    from app.models import EmploymentRecord, Organisation, Skill, User

    # Create Org A and Org B
    org_a = Organisation(name="CSM Org A", code="ORG_A_RES")
    org_b = Organisation(name="External Org B", code="ORG_B_RES")
    db_session.add_all([org_a, org_b])
    db_session.flush()

    manager = User(org_id=org_a.id, email="mgr@csm.tech", password_hash="h", full_name="Manager A")
    report = User(org_id=org_a.id, email="report@csm.tech", password_hash="h", full_name="Report A")
    external_user = User(
        org_id=org_b.id, email="ext@other.com", password_hash="h", full_name="External User"
    )
    db_session.add_all([manager, report, external_user])
    db_session.flush()

    # Link direct report hierarchy in DB
    emp_record = EmploymentRecord(
        user_id=report.id,
        org_id=org_a.id,
        employee_code="EMP-REP-01",
        department="Engineering",
        designation="Associate Software Engineer",
        reporting_line_id=manager.id,
    )
    db_session.add(emp_record)

    # Create Skill in Org A
    skill = Skill(
        org_id=org_a.id, code="SKILL_PYTHON", name="Python Programming", category="TECHNICAL"
    )
    db_session.add(skill)
    db_session.commit()

    mgr_ctx = UserContext(user_id=manager.id, org_id=org_a.id, roles=["MANAGER"])

    # 1. Resolve direct report user: is_direct_report MUST be True, target_org_id == org_a.id
    resolved_report = resolve_server_side_context(db_session, "users", report.id, mgr_ctx)
    assert resolved_report["is_direct_report"] is True
    assert resolved_report["target_org_id"] == org_a.id

    # 2. Resolve external user: target_org_id MUST be org_b.id, is_direct_report False
    resolved_external = resolve_server_side_context(db_session, "users", external_user.id, mgr_ctx)
    assert resolved_external["is_direct_report"] is False
    assert resolved_external["target_org_id"] == org_b.id
    # Assert policy engine denies access because target org does not match subject org
    assert can(mgr_ctx, "read", "users", resolved_external) is False

    # 3. Resolve skill org: target_org_id derived from DB record
    resolved_skill = resolve_server_side_context(db_session, "skills", skill.id, mgr_ctx)
    assert resolved_skill["target_org_id"] == org_a.id


def test_policy_registry_fails_startup_when_matrix_missing() -> None:
    """Verify that PolicyMatrixRegistry strictly raises RuntimeError if the matrix is missing or invalid."""
    from pathlib import Path

    from app.core.policy import PolicyMatrixRegistry

    # Negative test: Non-existent matrix file fails startup
    with pytest.raises(RuntimeError) as exc_info:
        PolicyMatrixRegistry(matrix_path=Path("non_existent_matrix_file.json"))

    assert "could not be loaded" in str(exc_info.value)


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


def test_multi_role_evaluation_all_roles_evaluated_and_explicit_deny_wins() -> None:
    """Verify that a subject with multiple roles is evaluated against all of them, with explicit deny winning."""
    # 1. Subject with EMPLOYEE and TRAINER_MENTOR:
    # TRAINER_MENTOR has publish permission on pathways (scope ORGANIZATION, condition author != subject)
    user_multi = UserContext(
        user_id="user_trainer_1",
        org_id="org_csm",
        roles=["EMPLOYEE", "TRAINER_MENTOR"],
    )

    # When SoD condition holds (author != subject), user gets the grant from TRAINER_MENTOR role
    assert (
        can(
            user_multi,
            "publish",
            "pathways",
            {"author_id": "other_author", "target_org_id": "org_csm"},
        )
        is True
    )

    # 2. When SoD condition fails (author == subject), SoD deny wins immediately
    assert (
        can(
            user_multi,
            "publish",
            "pathways",
            {"author_id": "user_trainer_1", "target_org_id": "org_csm"},
        )
        is False
    )

    # 3. Explicit deny wins: if action is forbidden under strict default-deny or unallowed
    assert can(user_multi, "delete", "audit_log", {}) is False


def test_separation_of_duties_requires_real_db_author_and_denies_unknown_author(
    db_session: Session,
) -> None:
    """Verify SoD loads real author from DB and denies approve/publish when author cannot be determined."""
    from app.core.policy import resolve_server_side_context
    from app.models import EvidenceRecord, Organisation, Skill, User

    org = Organisation(name="CSM Tech", code="CSM_SOD_TEST")
    db_session.add(org)
    db_session.flush()

    user_author = User(
        org_id=org.id, email="author@csm.tech", password_hash="h", full_name="Author"
    )
    user_reviewer = User(
        org_id=org.id, email="reviewer@csm.tech", password_hash="h", full_name="Reviewer"
    )
    db_session.add_all([user_author, user_reviewer])
    db_session.flush()

    skill = Skill(org_id=org.id, code="SK_LEADERSHIP", name="Leadership", category="BEHAVIOURAL")
    db_session.add(skill)
    db_session.flush()

    # Create real EvidenceRecord authored by user_author
    ev_record = EvidenceRecord(
        org_id=org.id,
        user_id=user_author.id,
        skill_id=skill.id,
        evidence_type="ASSESSMENT_ATTEMPT",
    )
    db_session.add(ev_record)
    db_session.commit()

    reviewer_ctx = UserContext(user_id=user_reviewer.id, org_id=org.id, roles=["TRAINER_MENTOR"])
    author_ctx = UserContext(user_id=user_author.id, org_id=org.id, roles=["TRAINER_MENTOR"])

    # 1. Server-side context loads real author from DB
    ctx_loaded = resolve_server_side_context(
        db_session, "evidence_records", ev_record.id, reviewer_ctx
    )
    assert ctx_loaded["author_id"] == user_author.id
    assert ctx_loaded["target_org_id"] == org.id

    # Reviewer (different user) is allowed to publish (author != subject)
    assert can(reviewer_ctx, "publish", "pathways", ctx_loaded) is True

    # Author (same user) is strictly forbidden from self-publishing
    assert can(author_ctx, "publish", "pathways", ctx_loaded) is False

    # 2. Invariant: Deny approve/publish when author CANNOT be determined
    unknown_ctx = resolve_server_side_context(
        db_session, "evidence_records", "non_existent_record_id", reviewer_ctx
    )
    assert unknown_ctx["author_id"] is None
    assert can(reviewer_ctx, "approve", "greenhouse_ideas", unknown_ctx) is False
    assert can(reviewer_ctx, "publish", "pathways", unknown_ctx) is False


def test_require_permission_with_real_database_row_no_hand_supplied_author(
    db_session: Session,
) -> None:
    """Test require_permission dependency with a real database row, deriving author from DB only."""
    from fastapi import HTTPException
    from starlette.requests import Request

    from app.core.policy import require_permission
    from app.models import EvidenceRecord, Organisation, Skill, User

    org = Organisation(name="CSM Tech", code="CSM_REQ_PERM")
    db_session.add(org)
    db_session.flush()

    author = User(
        org_id=org.id, email="author_row@csm.tech", password_hash="h", full_name="Author Row"
    )
    reviewer = User(
        org_id=org.id, email="rev_row@csm.tech", password_hash="h", full_name="Reviewer Row"
    )
    db_session.add_all([author, reviewer])
    db_session.flush()

    skill = Skill(org_id=org.id, code="SK_ARCH", name="Architecture", category="TECHNICAL")
    db_session.add(skill)
    db_session.flush()

    # Real DB row
    record = EvidenceRecord(
        org_id=org.id,
        user_id=author.id,
        skill_id=skill.id,
        evidence_type="PROJECT_WORK",
    )
    db_session.add(record)
    db_session.commit()

    # Mock request with path_params referencing real record.id
    scope = {
        "type": "http",
        "method": "POST",
        "path": f"/api/v1/evidence/{record.id}/approve",
        "path_params": {"id": record.id},
        "headers": [],
    }
    request = Request(scope)

    # 1. Author attempting self-approval via require_permission: MUST raise 403 Forbidden
    author_claims = {"sub": author.id, "org_id": org.id, "roles": ["TRAINER_MENTOR"]}
    author_dep = require_permission("publish", "pathways")

    with pytest.raises(HTTPException) as exc_info:
        author_dep(request=request, claims=author_claims, db=db_session)
    assert exc_info.value.status_code == 403

    # 2. Reviewer calling require_permission: Succeeds because author != subject
    reviewer_claims = {"sub": reviewer.id, "org_id": org.id, "roles": ["TRAINER_MENTOR"]}
    reviewer_dep = require_permission("publish", "pathways")
    res_ctx = reviewer_dep(request=request, claims=reviewer_claims, db=db_session)
    assert res_ctx.user_id == reviewer.id

    # 3. Non-existent ID: Author cannot be determined -> MUST raise 403 Forbidden
    non_existent_scope = {
        "type": "http",
        "method": "POST",
        "path": "/api/v1/evidence/missing_id/approve",
        "path_params": {"id": "missing_id"},
        "headers": [],
    }
    missing_req = Request(non_existent_scope)
    with pytest.raises(HTTPException) as exc_info:
        reviewer_dep(request=missing_req, claims=reviewer_claims, db=db_session)
    assert exc_info.value.status_code == 403


def test_time_limited_grant_expiry_excludes_role(db_session: Session) -> None:
    """Verify that expired grants are excluded from active user roles."""
    from datetime import UTC, datetime, timedelta

    from app.models import Grant, Organisation, Role, User
    from app.services.auth_service import get_active_user_roles

    org = Organisation(name="CSM Tech", code="CSM_EXP_GRANT")
    db_session.add(org)
    db_session.flush()

    user = User(
        org_id=org.id, email="exp_user@csm.tech", password_hash="h", full_name="Expiring User"
    )
    db_session.add(user)
    db_session.flush()

    role_emp = Role(code="EMPLOYEE", name="Employee Role")
    role_trainer = Role(code="TRAINER_MENTOR", name="Trainer Role")
    db_session.add_all([role_emp, role_trainer])
    db_session.flush()

    now = datetime.now(UTC)

    # Permanent grant for EMPLOYEE
    grant_perm = Grant(
        user_id=user.id,
        role_id=role_emp.id,
        org_id=org.id,
        expires_at=None,
    )
    # Expired grant for TRAINER_MENTOR (expired 1 hour ago)
    grant_expired = Grant(
        user_id=user.id,
        role_id=role_trainer.id,
        org_id=org.id,
        expires_at=now - timedelta(hours=1),
    )
    db_session.add_all([grant_perm, grant_expired])
    db_session.commit()

    db_session.refresh(user)

    # Active roles strictly excludes expired grant
    active_roles = get_active_user_roles(user, as_of=now)
    assert "EMPLOYEE" in active_roles
    assert "TRAINER_MENTOR" not in active_roles

    # If evaluated prior to expiration, role was active
    past_roles = get_active_user_roles(user, as_of=now - timedelta(hours=2))
    assert "TRAINER_MENTOR" in past_roles
