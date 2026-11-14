"""TRELLIS Pathways & Curriculum Domain Test Suite (Slice 1.6).

Tests:
1. Prerequisite DAG acyclicity validation (rejects circular dependency loops).
2. Pathway creation with courses and modules hierarchy via UnitOfWork.
3. Separation of duties enforcement: author cannot self-publish; reviewer can publish.
4. First-90-Days onboarding pathway resolution and enrolment progress telemetry.
5. In-transaction transactional audit log generation for mutating curriculum operations.
6. HTTP-level endpoint validation via FastAPI router and dependencies.
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
from app.models import AuditLog, Organisation, Role, User
from app.models.base import Base
from app.models.curriculum import Course, Module, Pathway
from app.services.auth_service import issue_tokens_for_user
from app.services.pathway_service import (
    calculate_enrolment_progress,
    create_pathway_service,
    enrol_user_in_pathway_service,
    estimate_time_to_productivity,
    publish_pathway_service,
    validate_course_prerequisites_dag,
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


def test_prerequisite_dag_acyclicity_validation() -> None:
    """Verify that prerequisite validation accepts acyclic DAGs and rejects circular loops."""
    # 1. Valid acyclic DAG: C1 -> C2 -> C3, C1 -> C4
    valid_courses = [
        {"id": "c1", "code": "ENG_101", "prerequisite_id": None},
        {"id": "c2", "code": "ENG_201", "prerequisite_id": "c1"},
        {"id": "c3", "code": "ENG_301", "prerequisite_id": "c2"},
        {"id": "c4", "code": "ENG_202", "prerequisite_id": "c1"},
    ]
    assert validate_course_prerequisites_dag(valid_courses) is True

    # 2. Direct cycle: C1 -> C2 -> C1
    direct_cycle = [
        {"id": "c1", "code": "CYC_1", "prerequisite_id": "c2"},
        {"id": "c2", "code": "CYC_2", "prerequisite_id": "c1"},
    ]
    with pytest.raises(ValueError) as exc_direct:
        validate_course_prerequisites_dag(direct_cycle)
    assert "Cycle detected" in str(exc_direct.value)

    # 3. Indirect cycle: C1 -> C2 -> C3 -> C4 -> C1
    indirect_cycle = [
        {"id": "c1", "code": "LOOP_1", "prerequisite_id": "c4"},
        {"id": "c2", "code": "LOOP_2", "prerequisite_id": "c1"},
        {"id": "c3", "code": "LOOP_3", "prerequisite_id": "c2"},
        {"id": "c4", "code": "LOOP_4", "prerequisite_id": "c3"},
    ]
    with pytest.raises(ValueError) as exc_loop:
        validate_course_prerequisites_dag(indirect_cycle)
    assert "Cycle detected" in str(exc_loop.value)


def test_pathway_domain_service_creation_and_courses(db_session: Session) -> None:
    """Verify pathway creation with courses and modules hierarchy, and in-transaction audit."""
    org = Organisation(name="CSM Tech", code="CSM_PW_DOM")
    author_role = Role(code="CONTENT_AUTHOR", name="Content Author", is_system_role=True)
    db_session.add_all([org, author_role])
    db_session.flush()

    author = User(
        org_id=org.id,
        email="author_dom@csm.tech",
        password_hash=hash_password("Pass123!"),
        full_name="Pathway Author",
    )
    db_session.add(author)
    db_session.commit()

    dummy_request = Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/api/v1/pathways",
            "headers": [(b"x-request-id", b"req_pw_create_123")],
        }
    )
    uow = UnitOfWork(
        session=db_session, request=dummy_request, claims={"sub": author.id, "org_id": org.id}
    )

    courses_payload = [
        {
            "code": "CRS_DIST_SYS",
            "title": "Distributed Systems",
            "sequence_order": 1,
            "modules": [
                {
                    "title": "Consensus & Raft",
                    "module_type": "LESSON",
                    "sequence_order": 1,
                    "estimated_minutes": 45,
                },
                {
                    "title": "Fault Injection Lab",
                    "module_type": "LAB",
                    "sequence_order": 2,
                    "estimated_minutes": 90,
                },
            ],
        }
    ]

    pathway = create_pathway_service(
        uow=uow,
        org_id=org.id,
        author_id=author.id,
        code="PW_DIST_ENG",
        title="Distributed Systems Engineering",
        description="Comprehensive distributed systems journey",
        target_role_code="STAFF_ENGINEER",
        estimated_hours=60.0,
        is_first_90_days=False,
        courses_data=courses_payload,
        request_id="req_pw_create_123",
    )

    assert pathway.id is not None
    assert pathway.code == "PW_DIST_ENG"
    assert pathway.is_published is False
    assert pathway.author_id == author.id

    # Verify courses and modules were persisted
    db_session.expire_all()
    courses = (
        db_session.execute(select(Course).where(Course.pathway_id == pathway.id)).scalars().all()
    )
    assert len(courses) == 1
    assert courses[0].code == "CRS_DIST_SYS"

    modules = (
        db_session.execute(select(Module).where(Module.course_id == courses[0].id)).scalars().all()
    )
    assert len(modules) == 2

    # Verify in-transaction audit was written
    audit = (
        db_session.query(AuditLog)
        .filter(AuditLog.resource == "pathways", AuditLog.resource_id == pathway.id)
        .one_or_none()
    )
    assert audit is not None
    assert audit.action == "create"
    assert audit.actor_id == author.id
    assert audit.request_id == "req_pw_create_123"


def test_pathway_publish_separation_of_duties_service(db_session: Session) -> None:
    """Verify separation of duties: Author cannot publish own pathway; Reviewer can publish."""
    org = Organisation(name="CSM Tech", code="CSM_PW_PUB")
    db_session.add(org)
    db_session.flush()

    author = User(
        org_id=org.id,
        email="pw_author@csm.tech",
        password_hash=hash_password("Pass123!"),
        full_name="Pathway Author",
    )
    reviewer = User(
        org_id=org.id,
        email="pw_reviewer@csm.tech",
        password_hash=hash_password("Pass123!"),
        full_name="Trainer Reviewer",
    )
    db_session.add_all([author, reviewer])
    db_session.flush()

    pathway = Pathway(
        org_id=org.id,
        code="PW_CLOUD_PUB",
        title="Cloud Architecture",
        author_id=author.id,
        is_published=False,
    )
    db_session.add(pathway)
    db_session.commit()

    dummy_request = Request(
        {
            "type": "http",
            "method": "POST",
            "path": f"/api/v1/pathways/{pathway.id}/publish",
            "headers": [(b"x-request-id", b"req_pub_456")],
        }
    )

    # 1. Author attempting to publish own pathway: Strictly Forbidden
    uow_author = UnitOfWork(
        session=db_session, request=dummy_request, claims={"sub": author.id, "org_id": org.id}
    )
    with pytest.raises(PermissionError) as exc_sod:
        publish_pathway_service(
            uow=uow_author,
            pathway_id=pathway.id,
            publisher_id=author.id,
            org_id=org.id,
        )
    assert "SEPARATION_OF_DUTIES" in str(exc_sod.value)

    # 2. Reviewer publishing: Allowed
    uow_reviewer = UnitOfWork(
        session=db_session, request=dummy_request, claims={"sub": reviewer.id, "org_id": org.id}
    )
    published_pw = publish_pathway_service(
        uow=uow_reviewer,
        pathway_id=pathway.id,
        publisher_id=reviewer.id,
        org_id=org.id,
        request_id="req_pub_456",
    )
    assert published_pw.is_published is True

    # Verify audit log recorded for publish action
    db_session.expire_all()
    audit = (
        db_session.query(AuditLog)
        .filter(AuditLog.resource == "pathways", AuditLog.action == "publish")
        .one_or_none()
    )
    assert audit is not None
    assert audit.actor_id == reviewer.id
    assert audit.request_id == "req_pub_456"


def test_first_90_days_pathway_and_enrolment_progress(db_session: Session) -> None:
    """Verify First-90-Days onboarding pathway resolution and progress telemetry."""
    org = Organisation(name="CSM Tech", code="CSM_90_ENROL")
    db_session.add(org)
    db_session.flush()

    author = User(
        org_id=org.id,
        email="author_90@csm.tech",
        password_hash=hash_password("Pass123!"),
        full_name="Author 90",
    )
    learner = User(
        org_id=org.id,
        email="learner_90@csm.tech",
        password_hash=hash_password("Pass123!"),
        full_name="New Engineer",
    )
    db_session.add_all([author, learner])
    db_session.flush()

    p90 = Pathway(
        org_id=org.id,
        code="PW_FIRST_90_DAYS",
        title="CSM Engineering: First 90 Days",
        author_id=author.id,
        is_published=True,
        is_first_90_days=True,
        estimated_hours=90.0,
    )
    db_session.add(p90)
    db_session.commit()

    # Enrol learner
    dummy_request = Request(
        {
            "type": "http",
            "method": "POST",
            "path": f"/api/v1/pathways/{p90.id}/enrol",
            "headers": [],
        }
    )
    uow = UnitOfWork(
        session=db_session, request=dummy_request, claims={"sub": learner.id, "org_id": org.id}
    )

    enrolment = enrol_user_in_pathway_service(
        uow=uow,
        pathway_id=p90.id,
        user_id=learner.id,
        org_id=org.id,
        request_id="req_enrol_789",
    )
    assert enrolment.status == "ENROLLED"
    assert enrolment.progress_percent == 0.0

    # Progress Calculation Telemetry
    assert calculate_enrolment_progress(total_modules=10, completed_modules=0) == 0.0
    assert calculate_enrolment_progress(total_modules=10, completed_modules=5) == 50.0
    assert calculate_enrolment_progress(total_modules=10, completed_modules=10) == 100.0

    # Time-to-Productivity Estimation
    telemetry = estimate_time_to_productivity(estimated_hours=90.0, hours_per_week=10.0)
    assert telemetry["estimated_total_hours"] == 90.0
    assert telemetry["estimated_weeks_to_completion"] == 9.0
    assert telemetry["estimated_days_to_productivity"] == 63.0


def test_http_pathways_endpoints_with_testclient(db_session: Session) -> None:
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
        org = Organisation(name="CSM Tech", code="CSM_HTTP_PW")
        author_role = Role(code="CONTENT_AUTHOR", name="Content Author", is_system_role=True)
        db_session.add_all([org, author_role])
        db_session.flush()

        user = User(
            org_id=org.id,
            email="http_pw@csm.tech",
            password_hash=hash_password("Pass123!"),
            full_name="HTTP Author",
        )
        db_session.add(user)
        db_session.commit()

        tokens = issue_tokens_for_user(db_session, user, ["CONTENT_AUTHOR"])
        headers = {"Authorization": f"Bearer {tokens.access_token}"}

        resp = client.post(
            "/api/v1/pathways",
            json={"code": "PW_HTTP_TEST", "title": "HTTP Pathway", "courses": []},
            headers=headers,
        )
        assert resp.status_code == 201
        assert resp.json()["code"] == "PW_HTTP_TEST"
    finally:
        app.dependency_overrides.pop(get_db, None)
