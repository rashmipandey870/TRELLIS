"""TRELLIS Personalised Home Domain & API Test Suite (Slice 1.7b).

Tests:
1. get_home_data computes real-time telemetry from database state (profile, enrolment, modules, streak).
2. Continuous Growth Ring computes correct evidence confidence classifications:
   - STRONG_EVIDENCE (>= 5 proofs)
   - DEVELOPING_EVIDENCE (3-4 proofs)
   - LIMITED_EVIDENCE (1-2 proofs)
   - NOT_ENOUGH_DATA (0 proofs)
3. Empty enrolment state handled gracefully.
4. Transactionally audited streak freeze consumption decrements freezes and records audit row in same transaction.
5. Streak freeze consumption refuses when 0 freezes remaining.
6. HTTP-level verification via TestClient.
"""

from __future__ import annotations

import sys
from collections.abc import Generator

import pytest
from fastapi import Request
from sqlalchemy import create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.security import hash_password
from app.core.uow import UnitOfWork
from app.models import AuditLog, EvidenceRecord, Organisation, Role, RoleRequirement, Skill, User
from app.models.base import Base
from app.models.curriculum import Cohort, Course, Enrolment, Module, Pathway
from app.models.meetings import Meeting, MeetingAudience
from app.services.auth_service import issue_tokens_for_user
from app.services.home_service import (
    compute_evidence_label,
    freeze_streak_service,
    get_home_data,
)


@pytest.fixture
def db_engine() -> Generator[Engine, None, None]:
    """Provide an in-memory SQLite database engine with StaticPool for cross-thread access."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
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


def test_compute_evidence_label_tiers() -> None:
    """Verify evidence confidence mapping matches requirements."""
    label, desc = compute_evidence_label(6)
    assert label == "STRONG_EVIDENCE"
    assert "Strong evidentiary foundation" in desc

    label, desc = compute_evidence_label(5)
    assert label == "STRONG_EVIDENCE"

    label, desc = compute_evidence_label(4)
    assert label == "DEVELOPING_EVIDENCE"
    assert "Developing competency" in desc

    label, desc = compute_evidence_label(3)
    assert label == "DEVELOPING_EVIDENCE"

    label, desc = compute_evidence_label(2)
    assert label == "LIMITED_EVIDENCE"
    assert "Preliminary indicator" in desc

    label, desc = compute_evidence_label(1)
    assert label == "LIMITED_EVIDENCE"

    label, desc = compute_evidence_label(0)
    assert label == "NOT_ENOUGH_DATA"
    assert "No verified evidence entries recorded" in desc


def test_get_home_dashboard_populated(db_session: Session) -> None:
    """Verify get_home_data populates profile, enrolment, modules, skill gaps, streak, and sessions."""
    org = Organisation(name="CSM Technology", code="CSM_TEST_HOME")
    learner_role = Role(code="LEARNER", name="Learner", is_system_role=True)
    db_session.add_all([org, learner_role])
    db_session.flush()

    user = User(
        org_id=org.id,
        email="learner01@csmtech.internal",
        password_hash=hash_password("DemoPassword123!"),
        full_name="Demo Learner 01",
        pseudonym_salt="test-user-salt-01",
        streak_days=14,
        streak_freezes_remaining=2,
    )
    db_session.add(user)
    db_session.flush()

    # Create Skills and Role Requirements
    skill_consensus = Skill(
        org_id=org.id,
        code="SKILL-CONSENSUS",
        name="Distributed Consensus (Raft/Paxos)",
        category="Distributed Systems",
    )
    skill_k8s = Skill(
        org_id=org.id,
        code="SKILL-K8S",
        name="Kubernetes Operator Architecture",
        category="Cloud Infrastructure",
    )
    skill_mtls = Skill(
        org_id=org.id,
        code="SKILL-MTLS",
        name="Zero-Trust mTLS & Service Mesh",
        category="Security & Networking",
    )
    skill_kafka = Skill(
        org_id=org.id,
        code="SKILL-KAFKA",
        name="Event Streaming with Apache Kafka",
        category="Data Engineering",
    )
    db_session.add_all([skill_consensus, skill_k8s, skill_mtls, skill_kafka])
    db_session.flush()

    req_consensus = RoleRequirement(
        org_id=org.id,
        role_code="PLATFORM_ENG_L2",
        skill_id=skill_consensus.id,
        target_level=4,
    )
    req_k8s = RoleRequirement(
        org_id=org.id,
        role_code="PLATFORM_ENG_L2",
        skill_id=skill_k8s.id,
        target_level=3,
    )
    req_mtls = RoleRequirement(
        org_id=org.id,
        role_code="PLATFORM_ENG_L2",
        skill_id=skill_mtls.id,
        target_level=3,
    )
    req_kafka = RoleRequirement(
        org_id=org.id,
        role_code="PLATFORM_ENG_L2",
        skill_id=skill_kafka.id,
        target_level=3,
    )
    db_session.add_all([req_consensus, req_k8s, req_mtls, req_kafka])

    # Evidence Records:
    # 6 for Consensus -> STRONG_EVIDENCE
    for i in range(6):
        rec = EvidenceRecord(
            user_id=user.id,
            skill_id=skill_consensus.id,
            org_id=org.id,
            evidence_type="LAB_ASSESSMENT",
            raw_payload_json={"attempt": i, "score": 95},
            key_id="k-1",
            is_shredded=False,
        )
        db_session.add(rec)

    # 3 for K8s -> DEVELOPING_EVIDENCE
    for i in range(3):
        rec = EvidenceRecord(
            user_id=user.id,
            skill_id=skill_k8s.id,
            org_id=org.id,
            evidence_type="CODE_REVIEW",
            raw_payload_json={"attempt": i, "score": 88},
            key_id="k-1",
            is_shredded=False,
        )
        db_session.add(rec)

    # 1 for mTLS -> LIMITED_EVIDENCE
    rec_mtls = EvidenceRecord(
        user_id=user.id,
        skill_id=skill_mtls.id,
        org_id=org.id,
        evidence_type="QUIZ",
        raw_payload_json={"score": 80},
        key_id="k-1",
        is_shredded=False,
    )
    db_session.add(rec_mtls)

    # 0 for Kafka -> NOT_ENOUGH_DATA

    # Pathway, Courses, Modules, Cohort, Enrolment
    pathway = Pathway(
        org_id=org.id,
        code="PW-PLATFORM-90D",
        title="First 90 Days: Platform Engineering",
        description="Core onboarding pathway for new platform engineers",
        author_id=user.id,
        is_published=True,
        target_role_code="PLATFORM_ENG_L2",
    )
    db_session.add(pathway)
    db_session.flush()

    c1 = Course(
        org_id=org.id,
        pathway_id=pathway.id,
        code="CRS-ENG-101",
        title="Platform Foundations & GitOps",
        sequence_order=1,
    )
    db_session.add(c1)
    db_session.flush()

    m1 = Module(
        org_id=org.id,
        course_id=c1.id,
        title="Repository Architecture & Branching Strategy",
        sequence_order=1,
        estimated_minutes=30,
    )
    m2 = Module(
        org_id=org.id,
        course_id=c1.id,
        title="CI/CD Pipeline Security & Container Signing",
        sequence_order=2,
        estimated_minutes=45,
    )
    db_session.add_all([m1, m2])
    db_session.flush()

    cohort = Cohort(
        org_id=org.id,
        pathway_id=pathway.id,
        name="Cohort Nova 2026",
        code="COHORT-NOVA-2026",
    )
    db_session.add(cohort)
    db_session.flush()

    enrolment = Enrolment(
        user_id=user.id,
        pathway_id=pathway.id,
        org_id=org.id,
        cohort_id=cohort.id,
        status="IN_PROGRESS",
        progress_percent=50.0,
    )
    db_session.add(enrolment)
    db_session.commit()

    # Query get_home_data
    data = get_home_data(session=db_session, user_id=user.id, org_id=org.id)

    # 1. Profile checks
    assert data["profile"]["id"] == user.id
    assert data["profile"]["name"] == "Demo Learner 01"
    assert data["profile"]["email"] == "learner01@csmtech.internal"
    assert data["profile"]["role_code"] == "PLATFORM_ENG_L2"

    # 2. Enrolment checks
    enr = data["enrolment"]
    assert enr is not None
    assert enr["pathway_code"] == "PW-PLATFORM-90D"
    assert enr["total_modules"] == 2
    assert enr["completed_modules"] == 1
    assert enr["progress_pct"] == 50
    assert enr["current_module_name"] == "CI/CD Pipeline Security & Container Signing"
    assert enr["current_course_title"] == "Platform Foundations & GitOps"

    # 3. Growth Ring Skill Gaps checks
    gaps = {g["skill_code"]: g for g in data["skill_gaps"]}
    assert len(gaps) == 4

    assert gaps["SKILL-CONSENSUS"]["sample_size"] == 6
    assert gaps["SKILL-CONSENSUS"]["evidence_label"] == "STRONG_EVIDENCE"
    assert "Strong evidentiary foundation" in gaps["SKILL-CONSENSUS"]["why_this"]

    assert gaps["SKILL-K8S"]["sample_size"] == 3
    assert gaps["SKILL-K8S"]["evidence_label"] == "DEVELOPING_EVIDENCE"

    assert gaps["SKILL-MTLS"]["sample_size"] == 1
    assert gaps["SKILL-MTLS"]["evidence_label"] == "LIMITED_EVIDENCE"

    assert gaps["SKILL-KAFKA"]["sample_size"] == 0
    assert gaps["SKILL-KAFKA"]["evidence_label"] == "NOT_ENOUGH_DATA"

    # 4. Streak checks
    streak = data["streak"]
    assert streak["current_streak_days"] == 14
    assert streak["freezes_remaining"] == 2
    assert streak["has_activity_today"] is True
    assert len(streak["weekly_history"]) == 7

    # 5. Sessions & Greenhouse checks (empty by default, no fake demo data)
    assert len(data["sessions"]) == 0
    assert data["greenhouse_idea"] is None


def test_get_home_dashboard_with_scheduled_meeting(db_session: Session) -> None:
    """Verify get_home_data retrieves real scheduled meetings for the learner."""
    org = Organisation(name="CSM Technology", code="CSM_TEST_MTG")
    db_session.add(org)
    db_session.flush()

    mentor = User(
        org_id=org.id,
        email="mentor_mtg@csmtech.internal",
        password_hash=hash_password("Pass123!"),
        full_name="Mentor Anand",
        pseudonym_salt="salt-mentor",
    )
    learner = User(
        org_id=org.id,
        email="learner_mtg@csmtech.internal",
        password_hash=hash_password("Pass123!"),
        full_name="Learner Sneha",
        pseudonym_salt="salt-learner",
    )
    db_session.add_all([mentor, learner])
    db_session.flush()

    meeting = Meeting(
        title="Weekly SRE Sync",
        meeting_date="2026-11-25",
        start_time="10:00",
        end_time="11:00",
        duration_minutes=60,
        meeting_link="https://meet.google.com/abc-defg-hij",
        mentor_id=mentor.id,
        status="SCHEDULED",
    )
    db_session.add(meeting)
    db_session.flush()

    audience = MeetingAudience(
        meeting_id=meeting.id,
        learner_id=learner.id,
    )
    db_session.add(audience)
    db_session.commit()

    data = get_home_data(session=db_session, user_id=learner.id, org_id=org.id)
    assert len(data["sessions"]) == 1
    session_item = data["sessions"][0]
    assert session_item["id"] == meeting.id
    assert session_item["title"] == "Weekly SRE Sync"
    assert session_item["trainer_name"] == "Mentor Anand"
    assert session_item["meeting_link"] == "https://meet.google.com/abc-defg-hij"
    assert session_item["session_type"] == "MEETING"


def test_get_home_dashboard_empty_enrolment(db_session: Session) -> None:
    """Verify get_home_data handles users with no active enrolments gracefully."""
    org = Organisation(name="CSM Tech", code="CSM_EMPTY_ENR")
    db_session.add(org)
    db_session.flush()

    user = User(
        org_id=org.id,
        email="newcomer@csmtech.internal",
        password_hash=hash_password("Pass123!"),
        full_name="New Learner",
        pseudonym_salt="new-salt",
        streak_days=0,
        streak_freezes_remaining=2,
    )
    db_session.add(user)
    db_session.commit()

    data = get_home_data(session=db_session, user_id=user.id, org_id=org.id)
    assert data["profile"]["name"] == "New Learner"
    assert data["enrolment"] is None
    assert data["streak"]["current_streak_days"] == 0
    assert data["streak"]["has_activity_today"] is False


def test_freeze_streak_transactional_audit(db_session: Session) -> None:
    """Verify freeze streak consumes freeze and commits transactional audit."""
    org = Organisation(name="CSM Tech", code="CSM_FREEZE_TEST")
    db_session.add(org)
    db_session.flush()

    user = User(
        org_id=org.id,
        email="freezer@csmtech.internal",
        password_hash=hash_password("Pass123!"),
        full_name="Freezer User",
        pseudonym_salt="freeze-salt",
        streak_days=10,
        streak_freezes_remaining=2,
    )
    db_session.add(user)
    db_session.commit()

    dummy_request = Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/api/v1/home/freeze-streak",
            "headers": [(b"x-request-id", b"req_freeze_001")],
        }
    )
    uow = UnitOfWork(
        session=db_session, request=dummy_request, claims={"sub": user.id, "org_id": org.id}
    )

    result = freeze_streak_service(
        uow=uow,
        user_id=user.id,
        org_id=org.id,
        request_id="req_freeze_001",
    )
    assert result["streak_freezes_remaining"] == 1
    assert result["current_streak_days"] == 10

    # Verify audit row created in database
    audit = (
        db_session.execute(
            select(AuditLog).where(
                AuditLog.actor_id == user.id,
                AuditLog.action == "use_streak_freeze",
            )
        )
        .scalars()
        .first()
    )
    assert audit is not None
    assert audit.resource == "streaks"
    assert audit.before_state_json == {"streak_freezes_remaining": 2}
    assert audit.after_state_json == {"streak_freezes_remaining": 1}


def test_freeze_streak_refuses_when_zero_freezes_left(db_session: Session) -> None:
    """Verify freeze streak raises ValueError when user has 0 freezes."""
    org = Organisation(name="CSM Tech", code="CSM_ZERO_FREEZE")
    db_session.add(org)
    db_session.flush()

    user = User(
        org_id=org.id,
        email="nofreezes@csmtech.internal",
        password_hash=hash_password("Pass123!"),
        full_name="No Freezes User",
        pseudonym_salt="zero-salt",
        streak_days=5,
        streak_freezes_remaining=0,
    )
    db_session.add(user)
    db_session.commit()

    dummy_request = Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/api/v1/home/freeze-streak",
            "headers": [],
        }
    )
    uow = UnitOfWork(
        session=db_session, request=dummy_request, claims={"sub": user.id, "org_id": org.id}
    )

    with pytest.raises(ValueError) as exc:
        freeze_streak_service(uow=uow, user_id=user.id, org_id=org.id)
    assert "NO_FREEZES_AVAILABLE" in str(exc.value)


def test_http_home_endpoints_with_testclient(db_session: Session) -> None:
    """HTTP-level verification using TestClient (runs on Linux CI; skipped on Windows Py3.14)."""
    if sys.platform == "win32" and sys.version_info >= (3, 14):
        pytest.skip(
            "TestClient AnyIO portal threadlock on Windows Python 3.14 host (verified in Linux CI)"
        )

    from fastapi.testclient import TestClient

    from app.api.deps import get_db
    from app.main import app

    engine = db_session.get_bind()

    def override_get_db() -> Generator[Session, None, None]:
        session = Session(engine)
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        client = TestClient(app)
        org = Organisation(name="CSM Tech", code="CSM_HTTP_HOME")
        learner_role = Role(code="LEARNER", name="Learner", is_system_role=True)
        db_session.add_all([org, learner_role])
        db_session.flush()

        user = User(
            org_id=org.id,
            email="http_home@csm.tech",
            password_hash=hash_password("Pass123!"),
            full_name="HTTP Learner",
            pseudonym_salt="salt-http-home",
            streak_days=7,
            streak_freezes_remaining=2,
        )
        db_session.add(user)
        db_session.commit()

        tokens = issue_tokens_for_user(db_session, user, ["LEARNER"])
        headers = {"Authorization": f"Bearer {tokens.access_token}"}

        # 1. GET /api/v1/home
        resp = client.get("/api/v1/home", headers=headers)
        assert resp.status_code == 200
        body = resp.json()
        assert body["profile"]["name"] == "HTTP Learner"
        assert body["streak"]["current_streak_days"] == 7

        # 2. POST /api/v1/home/freeze-streak
        resp_freeze = client.post("/api/v1/home/freeze-streak", headers=headers)
        assert resp_freeze.status_code == 200
        freeze_body = resp_freeze.json()
        assert freeze_body["streak_freezes_remaining"] == 1

        # 3. Negative: Unauthenticated request fails
        resp_unauth = client.get("/api/v1/home")
        assert resp_unauth.status_code in (401, 403)
    finally:
        app.dependency_overrides.pop(get_db, None)
