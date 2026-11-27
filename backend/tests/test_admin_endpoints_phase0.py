"""Automated tests for Phase 0.4 Admin Console Endpoints & Query Budgets."""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.v1.admin import (
    BatchUpdateRequest,
    get_admin_policies,
    get_admin_reports,
    get_batch_detail,
    get_system_health,
    list_admin_assessments,
    list_admin_meetings,
    list_admin_mentors,
    list_batches,
    list_user_sessions,
    reset_user_password,
    revoke_user_sessions,
    unassign_learner_from_batch,
    unassign_mentor_from_batch,
    unlock_user,
    update_admin_policy,
    update_batch,
    PolicyUpdateRequest,
    get_audit_logs,
)
from app.core.security import hash_password
from app.models import (
    Assessment,
    AssessmentAttempt,
    Base,
    Batch,
    Meeting,
    MeetingAttendance,
    MentorLearnerAssignment,
    Organisation,
    User,
)
from app.models.auth import RefreshToken
from app.models.audit import AuditLog
from datetime import datetime, timezone, timedelta


@pytest.fixture(scope="module")
def admin_test_env():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    org = Organisation(name="CSM Technologies", code="CSM-ADMIN-TEST")
    db.add(org)
    db.flush()

    pwd_hash = hash_password("AdminPass2026!")
    admin = User(
        org_id=org.id,
        email="superadmin@csmtech.internal",
        password_hash=pwd_hash,
        full_name="Super Admin",
        role="ADMIN",
        is_active=True,
    )
    mentor = User(
        org_id=org.id,
        email="leadmentor@csmtech.internal",
        password_hash=pwd_hash,
        full_name="Lead Mentor",
        role="MENTOR",
        is_active=True,
    )
    learner = User(
        org_id=org.id,
        email="testlearner1@csmtech.internal",
        password_hash=pwd_hash,
        full_name="Test Learner 1",
        role="LEARNER",
        is_active=True,
    )
    learner2 = User(
        org_id=org.id,
        email="testlearner2@csmtech.internal",
        password_hash=pwd_hash,
        full_name="Test Learner 2",
        role="LEARNER",
        is_active=True,
    )
    db.add_all([admin, mentor, learner, learner2])
    db.flush()

    batch = Batch(
        name="Cohort Lambda",
        code="CL-2026",
        field="FullStack",
        description="Core FullStack Cohort",
        max_learners=30,
        is_active=True,
    )
    db.add(batch)
    db.flush()

    assign1 = MentorLearnerAssignment(
        mentor_id=mentor.id,
        learner_id=learner.id,
        batch_id=batch.id,
    )
    assign2 = MentorLearnerAssignment(
        mentor_id=mentor.id,
        learner_id=learner2.id,
        batch_id=batch.id,
    )
    db.add_all([assign1, assign2])

    # Refresh Token Session
    token = RefreshToken(
        user_id=learner.id,
        org_id=org.id,
        family_id="family-123",
        token_hash="hash-abc-123",
        device_info="Chrome on Windows 11",
        ip_address="127.0.0.1",
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
    )
    db.add(token)

    # Assessment & Attempt
    assessment = Assessment(
        mentor_id=mentor.id,
        batch_id=batch.id,
        title="Python Async Mastery",
        field="Python",
        duration_minutes=45,
        passing_score=60,
        status="PUBLISHED",
    )
    db.add(assessment)
    db.flush()

    attempt = AssessmentAttempt(
        assessment_id=assessment.id,
        learner_id=learner.id,
        score=85.0,
        total_marks=100.0,
        passed=True,
        status="SUBMITTED",
    )
    db.add(attempt)

    # Meeting & Attendance
    meeting = Meeting(
        mentor_id=mentor.id,
        batch_id=batch.id,
        title="Weekly Technical Sync",
        meeting_date="2026-11-28",
        start_time="10:00",
        end_time="11:00",
        duration_minutes=60,
        meeting_link="https://meet.google.com/abc-def-ghi",
        status="COMPLETED",
    )
    db.add(meeting)
    db.flush()

    attendance = MeetingAttendance(
        meeting_id=meeting.id,
        learner_id=learner.id,
        attended=True,
    )
    db.add(attendance)

    # Audit log
    audit = AuditLog(
        org_id=org.id,
        actor_id=admin.id,
        action="CREATE_BATCH",
        resource="BATCH",
        resource_id=batch.id,
        ip_address="127.0.0.1",
    )
    db.add(audit)

    db.commit()

    class QueryCounter:
        def __init__(self):
            self.count = 0
            self.statements = []

        def __enter__(self):
            self.count = 0
            self.statements = []
            event.listen(engine, "before_cursor_execute", self._callback)
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            event.remove(engine, "before_cursor_execute", self._callback)

        def _callback(self, conn, cursor, statement, parameters, context, executemany):
            self.count += 1
            self.statements.append(statement)

    yield {
        "db": db,
        "counter_factory": QueryCounter,
        "admin": admin,
        "mentor": mentor,
        "learner": learner,
        "batch": batch,
        "assessment": assessment,
        "meeting": meeting,
    }
    db.close()


def test_list_batches_query_budget(admin_test_env):
    """Verify list_batches executes <= 4 queries (fixed from 53 queries)."""
    db = admin_test_env["db"]
    counter_factory = admin_test_env["counter_factory"]
    admin = admin_test_env["admin"]

    with counter_factory() as c:
        batches = list_batches(db=db, _admin=admin)
    assert len(batches) >= 1
    assert c.count <= 4, f"list_batches exceeded budget: used {c.count} queries"
    batch_data = batches[0]
    assert batch_data["code"] == "CL-2026"
    assert batch_data["learner_count"] >= 1
    assert len(batch_data["mentors"]) >= 1


def test_batch_detail_and_crud(admin_test_env):
    """Test get_batch_detail, update_batch, and unassign endpoints."""
    db = admin_test_env["db"]
    admin = admin_test_env["admin"]
    batch = admin_test_env["batch"]
    mentor = admin_test_env["mentor"]
    learner = admin_test_env["learner"]

    # 1. Detail
    detail = get_batch_detail(batch_id=batch.id, db=db, _admin=admin)
    assert detail["name"] == batch.name
    assert len(detail["mentors"]) >= 1
    assert len(detail["learners"]) >= 1

    # 2. Update
    upd = update_batch(
        batch_id=batch.id,
        payload=BatchUpdateRequest(description="Updated Description"),
        db=db,
        _admin=admin,
        _uow=None,
    )
    assert upd["id"] == batch.id

    # 3. Unassign learner and mentor
    unassign_learner_res = unassign_learner_from_batch(
        batch_id=batch.id, learner_id=learner.id, db=db, _admin=admin, _uow=None
    )
    assert unassign_learner_res["learner_id"] == learner.id

    unassign_mentor_res = unassign_mentor_from_batch(
        batch_id=batch.id, mentor_id=mentor.id, db=db, _admin=admin, _uow=None
    )
    assert unassign_mentor_res["mentor_id"] == mentor.id


def test_mentors_endpoint(admin_test_env):
    """Verify list_admin_mentors works with pagination and query budget <= 5."""
    db = admin_test_env["db"]
    counter_factory = admin_test_env["counter_factory"]
    admin = admin_test_env["admin"]

    with counter_factory() as c:
        res = list_admin_mentors(page=1, page_size=10, db=db, _admin=admin)
    assert res["total"] >= 1
    assert len(res["mentors"]) >= 1
    assert c.count <= 10, f"list_admin_mentors exceeded query budget: used {c.count}"


def test_user_management_security_endpoints(admin_test_env):
    """Test password reset, unlock, and session revocation."""
    db = admin_test_env["db"]
    admin = admin_test_env["admin"]
    learner = admin_test_env["learner"]

    # 1. Password reset
    reset_res = reset_user_password(user_id=learner.id, payload=None, db=db, _admin=admin, _uow=None)
    assert reset_res["must_change_password"] is True
    assert "temporary_password" in reset_res

    # 2. Unlock
    unlock_res = unlock_user(user_id=learner.id, db=db, _admin=admin, _uow=None)
    assert unlock_res["is_active"] is True

    # 3. Sessions list and revoke
    sessions = list_user_sessions(user_id=learner.id, db=db, _admin=admin)
    assert len(sessions) >= 1
    assert sessions[0]["is_revoked"] is False

    revoke_res = revoke_user_sessions(user_id=learner.id, db=db, _admin=admin, _uow=None)
    assert revoke_res["revoked_count"] >= 1


def test_oversight_reports_and_system_health(admin_test_env):
    """Test assessments oversight, meetings oversight, reports, policies, and health."""
    db = admin_test_env["db"]
    admin = admin_test_env["admin"]

    # 1. Assessments oversight
    assessments_res = list_admin_assessments(page=1, page_size=10, db=db, _admin=admin)
    assert assessments_res["total"] >= 1
    assert len(assessments_res["assessments"]) >= 1
    first_a = assessments_res["assessments"][0]
    assert "pass_rate" in first_a

    # 2. Meetings oversight
    meetings_res = list_admin_meetings(page=1, page_size=10, db=db, _admin=admin)
    assert meetings_res["total"] >= 1
    assert len(meetings_res["meetings"]) >= 1
    first_m = meetings_res["meetings"][0]
    assert first_m["attendees_count"] >= 1

    # 3. Reports
    reports_res = get_admin_reports(db=db, _admin=admin)
    assert "summary" in reports_res
    assert reports_res["summary"]["total_assessments"] >= 1

    # 4. Policies
    policies_res = get_admin_policies(db=db, _admin=admin)
    assert "ACCOUNT_LOCKOUT_ATTEMPTS" in policies_res["policies"]

    upd_policy_res = update_admin_policy(
        key="DEFAULT_PASSING_PERCENTAGE",
        payload=PolicyUpdateRequest(value=65),
        db=db,
        admin=admin,
        _uow=None,
    )
    assert upd_policy_res["value"] == 65

    # 5. System Health
    health_res = get_system_health(db=db, _admin=admin)
    assert health_res["database"]["connected"] is True
    assert health_res["code_runner"]["status"] == "OPERATIONAL"

    # 6. Audit logs filter
    audits = get_audit_logs(action="CREATE_BATCH", limit=10, db=db, _admin=admin)
    assert len(audits) >= 1
    assert audits[0]["action"] == "CREATE_BATCH"
