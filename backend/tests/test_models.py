"""Automated tests validating ORM Model entities, constraints, and relationships."""

from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models import (
    Base,
    Consent,
    EmploymentRecord,
    Grant,
    Organisation,
    Role,
    RoleRequirement,
    Skill,
    SkillEdge,
    SkillLevel,
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


def test_organisation_and_user_creation(db_session: Session) -> None:
    """Verify Organisation and User creation with relationships and default values."""
    org = Organisation(name="CSM Technology", code="CSM_MAIN", domain="csm.tech")
    db_session.add(org)
    db_session.commit()

    user = User(
        org_id=org.id,
        email="learner@csm.tech",
        password_hash="argon2id$mock_hash",
        full_name="Priya Sharma",
        preferences_json={"dyslexia_font_enabled": True, "theme": "dark"},
    )
    db_session.add(user)
    db_session.commit()

    saved_user = db_session.get(User, user.id)
    assert saved_user is not None
    assert saved_user.email == "learner@csm.tech"
    assert saved_user.preferences_json is not None
    assert saved_user.preferences_json.get("dyslexia_font_enabled") is True
    assert saved_user.organisation.code == "CSM_MAIN"


def test_employment_record_and_hierarchy(db_session: Session) -> None:
    """Verify EmploymentRecord links user to reporting line manager."""
    org = Organisation(name="CSM Tech", code="CSM_EMP")
    db_session.add(org)
    db_session.commit()

    mgr = User(org_id=org.id, email="mgr@csm.tech", password_hash="hash", full_name="Aarav Patel")
    emp = User(org_id=org.id, email="emp@csm.tech", password_hash="hash", full_name="Sneha Rao")
    db_session.add_all([mgr, emp])
    db_session.commit()

    record = EmploymentRecord(
        user_id=emp.id,
        org_id=org.id,
        employee_code="EMP_00123",
        department="Engineering",
        designation="Software Engineer",
        reporting_line_id=mgr.id,
    )
    db_session.add(record)
    db_session.commit()

    saved_emp = db_session.get(User, emp.id)
    assert saved_emp is not None
    assert saved_emp.employment_record is not None
    assert saved_emp.employment_record.reporting_manager is not None
    assert saved_emp.employment_record.reporting_manager.full_name == "Aarav Patel"


def test_role_and_grant_assignment(db_session: Session) -> None:
    """Verify Role definition and Grant assignment to user."""
    org = Organisation(name="CSM Tech", code="CSM_ROLES")
    role = Role(code="LK_ADMIN", name="Learning & Knowledge Administrator", is_system_role=True)
    db_session.add_all([org, role])
    db_session.commit()

    user = User(org_id=org.id, email="admin@csm.tech", password_hash="hash", full_name="Admin User")
    db_session.add(user)
    db_session.commit()

    grant = Grant(
        user_id=user.id,
        role_id=role.id,
        org_id=org.id,
        approval_ref="CHG-2026-001",
    )
    db_session.add(grant)
    db_session.commit()

    saved_user = db_session.get(User, user.id)
    assert saved_user is not None
    assert len(saved_user.grants) == 1
    assert saved_user.grants[0].role.code == "LK_ADMIN"


def test_consent_passport_tracking(db_session: Session) -> None:
    """Verify Consent creation and 1-click status revocation."""
    org = Organisation(name="CSM Tech", code="CSM_CONSENT")
    db_session.add(org)
    db_session.flush()

    user = User(
        org_id=org.id, email="consent_user@csm.tech", password_hash="hash", full_name="Consent User"
    )
    db_session.add(user)
    db_session.commit()

    consent = Consent(
        user_id=user.id,
        org_id=org.id,
        purpose_code="growth_ring_sharing",
        status="GRANTED",
    )
    db_session.add(consent)
    db_session.commit()

    # Revoke consent
    consent.status = "REVOKED"
    db_session.commit()

    saved = db_session.get(Consent, consent.id)
    assert saved is not None
    assert saved.status == "REVOKED"


def test_skills_taxonomy_and_edges(db_session: Session) -> None:
    """Verify Skill hierarchy with rubric levels and graph edges."""
    org = Organisation(name="CSM Tech", code="CSM_SKILLS")
    db_session.add(org)
    db_session.commit()

    s1 = Skill(org_id=org.id, code="SK_PY_CORE", name="Python Core", category="TECHNICAL")
    s2 = Skill(org_id=org.id, code="SK_FASTAPI", name="FastAPI Web Framework", category="TECHNICAL")
    db_session.add_all([s1, s2])
    db_session.commit()

    # Add levels to skill
    lvl1 = SkillLevel(
        skill_id=s1.id,
        level_number=1,
        title="Novice",
        rubric_text="Understands syntax and basic loops.",
    )
    lvl2 = SkillLevel(
        skill_id=s1.id,
        level_number=2,
        title="Competent",
        rubric_text="Writes idiomatic functions and modules.",
    )
    edge = SkillEdge(
        org_id=org.id,
        source_skill_id=s1.id,
        target_skill_id=s2.id,
        relationship_type="PREREQUISITE",
    )
    req = RoleRequirement(
        org_id=org.id,
        role_code="BACKEND_DEV_L1",
        skill_id=s1.id,
        target_level=2,
    )
    db_session.add_all([lvl1, lvl2, edge, req])
    db_session.commit()

    saved_skill = db_session.get(Skill, s1.id)
    assert saved_skill is not None
    assert len(saved_skill.levels) == 2
    assert saved_skill.levels[0].title == "Novice"
