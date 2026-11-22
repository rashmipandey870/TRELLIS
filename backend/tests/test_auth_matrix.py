"""Unit and integration tests for TRELLIS Authorization Matrix & Security Hardening (Phase E).

Verifies:
- Strict role isolation: Admin, Mentor, Learner.
- Admin CANNOT create mentor assessments or schedule mentor meetings (403 Forbidden).
- Learner CANNOT access admin endpoints or mentor endpoints (403 Forbidden).
- Mentor CANNOT manage admin users or modify system settings (403 Forbidden).
- Unauthenticated requests fail with 401 Unauthorized.
- must_change_password enforcement blocks protected endpoints until password is changed.
"""

from __future__ import annotations

from unittest.mock import MagicMock
import pytest
from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api.deps import (
    get_current_user,
    get_current_user_claims,
    require_admin,
    require_learner,
    require_mentor,
    require_role,
)
from app.models.base import Base
from app.models.tenancy import Organisation
from app.models.user import User


@pytest.fixture
def auth_db_session():
    """In-memory SQLite database session with all models."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        org = Organisation(name="CSM Technology", code="CSM_MAIN")
        session.add(org)
        session.flush()

        admin = User(
            org_id=org.id,
            email="admin@csmtech.internal",
            password_hash="argon2_fake",
            full_name="Rajesh Mohanty",
            role="ADMIN",
            is_active=True,
            must_change_password=False,
        )
        mentor = User(
            org_id=org.id,
            email="soumya.p@csmtech.internal",
            password_hash="argon2_fake",
            full_name="Soumya Patnaik",
            role="MENTOR",
            is_active=True,
            must_change_password=False,
        )
        learner = User(
            org_id=org.id,
            email="learner1@csmtech.internal",
            password_hash="argon2_fake",
            full_name="Priya Sharma",
            role="LEARNER",
            is_active=True,
            must_change_password=False,
        )
        session.add_all([admin, mentor, learner])
        session.commit()
        yield session, admin, mentor, learner


def test_admin_cannot_access_mentor_exclusive_endpoints(auth_db_session):
    """Admin must NOT possess Mentor-exclusive privileges (e.g. creating mentor assessments)."""
    _, admin, _, _ = auth_db_session

    check_mentor = require_mentor
    with pytest.raises(HTTPException) as exc:
        check_mentor(current_user=admin, claims={"roles": ["ADMIN"]})
    assert exc.value.status_code == status.HTTP_403_FORBIDDEN
    assert "Access denied" in exc.value.detail


def test_mentor_cannot_access_admin_exclusive_endpoints(auth_db_session):
    """Mentor must NOT possess Admin privileges (e.g. system settings, bulk import)."""
    _, _, mentor, _ = auth_db_session

    check_admin = require_admin
    with pytest.raises(HTTPException) as exc:
        check_admin(current_user=mentor, claims={"roles": ["MENTOR"]})
    assert exc.value.status_code == status.HTTP_403_FORBIDDEN
    assert "Access denied" in exc.value.detail


def test_learner_cannot_access_admin_or_mentor_endpoints(auth_db_session):
    """Learners must NOT possess Admin or Mentor privileges."""
    _, _, _, learner = auth_db_session

    with pytest.raises(HTTPException) as exc1:
        require_admin(current_user=learner, claims={"roles": ["LEARNER"]})
    assert exc1.value.status_code == status.HTTP_403_FORBIDDEN

    with pytest.raises(HTTPException) as exc2:
        require_mentor(current_user=learner, claims={"roles": ["LEARNER"]})
    assert exc2.value.status_code == status.HTTP_403_FORBIDDEN


def test_unauthenticated_request_fails():
    """Missing bearer token credentials must raise 401 Unauthorized."""
    with pytest.raises(HTTPException) as exc:
        get_current_user_claims(credentials=None)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Missing authentication credentials" in exc.value.detail


def test_must_change_password_enforcement(auth_db_session):
    """Users with must_change_password=True are forbidden from accessing standard resources."""
    session, _, _, learner = auth_db_session
    learner.must_change_password = True
    session.commit()

    mock_request = MagicMock()
    mock_request.url.path = "/api/v1/learner/dashboard"

    claims = {"sub": learner.id, "roles": ["LEARNER"]}
    with pytest.raises(HTTPException) as exc:
        get_current_user(request=mock_request, claims=claims, db=session)
    assert exc.value.status_code == status.HTTP_403_FORBIDDEN
    assert "MUST_CHANGE_PASSWORD" in exc.value.detail

    # Allowed paths must pass without 403
    mock_request.url.path = "/api/v1/auth/change-password"
    user = get_current_user(request=mock_request, claims=claims, db=session)
    assert user.id == learner.id
