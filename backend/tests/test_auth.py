"""Automated tests validating Asymmetric Auth, Token Family Rotation & TOTP MFA."""

from collections.abc import Generator

import pyotp
import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    decode_access_token,
    decrypt_field,
    generate_totp_secret,
    get_jwks,
    hash_password,
    verify_password,
    verify_totp,
)
from app.models import AuditLog, Base, Grant, Organisation, RefreshToken, Role, User
from app.services.auth_service import (
    complete_admin_mfa_enrolment,
    login_flow,
    logout_session,
    rotate_refresh_token,
    setup_totp_mfa,
    verify_mfa_challenge,
)
from app.services.rate_limiter import rate_limiter


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


def test_argon2id_password_hashing() -> None:
    """Verify that passwords are securely hashed using Argon2id."""
    password = "SuperSecretPassword2026!"
    hashed = hash_password(password)

    assert hashed.startswith("$argon2id$")
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False


def test_asymmetric_jwt_issuing_and_jwks() -> None:
    """Verify asymmetric RS256 token signing, verification, and JWKS exposure."""
    token = create_access_token(
        subject="usr_123",
        org_id="org_csm",
        roles=["EMPLOYEE"],
    )
    assert token is not None

    claims = decode_access_token(token)
    assert claims["sub"] == "usr_123"
    assert claims["org_id"] == "org_csm"
    assert claims["roles"] == ["EMPLOYEE"]
    assert claims["iss"] == "trellis-auth-server"

    # Verify JWKS structure
    jwks = get_jwks()
    assert "keys" in jwks
    assert len(jwks["keys"]) > 0
    key = jwks["keys"][0]
    assert key["kty"] == "RSA"
    assert key["alg"] == "RS256"
    assert "kid" in key
    assert "n" in key
    assert "e" in key


def test_standard_employee_login_flow(db_session: Session) -> None:
    """Verify that an EMPLOYEE user receives access and refresh tokens without MFA."""
    org = Organisation(name="CSM Technology", code="CSM_EMP_LOGIN")
    db_session.add(org)
    db_session.flush()

    pwd_hash = hash_password("LearnerPass123!")
    user = User(
        org_id=org.id,
        email="learner@csm.tech",
        password_hash=pwd_hash,
        full_name="Priya Sharma",
    )
    db_session.add(user)
    db_session.commit()

    resp = login_flow(
        session=db_session,
        email="learner@csm.tech",
        password="LearnerPass123!",
        ip_address="192.168.1.50",
    )

    assert resp.mfa_required is False
    assert resp.tokens is not None
    assert resp.tokens.access_token is not None
    assert resp.tokens.refresh_token is not None
    assert "EMPLOYEE" in resp.tokens.roles

    # Check audit log written
    audits = db_session.execute(select(AuditLog)).scalars().all()
    assert len(audits) >= 1
    assert any(a.action == "login_success" for a in audits)


def test_admin_role_requires_totp_mfa(db_session: Session) -> None:
    """Verify LK_ADMIN requires TOTP MFA, bypass codes are rejected, and enrolment is enforced."""
    org = Organisation(name="CSM Technology", code="CSM_ADMIN_MFA")
    role = Role(code="LK_ADMIN", name="LK Administrator", is_system_role=True)
    db_session.add_all([org, role])
    db_session.flush()

    pwd_hash = hash_password("AdminSecret2026!")
    user = User(
        org_id=org.id,
        email="admin@csm.tech",
        password_hash=pwd_hash,
        full_name="Chief Admin",
    )
    db_session.add(user)
    db_session.flush()

    grant = Grant(user_id=user.id, role_id=role.id, org_id=org.id)
    db_session.add(grant)
    db_session.commit()

    # Step 1: Initial admin login requires MFA and detects missing TOTP enrolment
    resp = login_flow(
        session=db_session,
        email="admin@csm.tech",
        password="AdminSecret2026!",
    )

    assert resp.mfa_required is True
    assert resp.mfa_enrolment_required is True
    assert resp.mfa_ticket is not None
    assert resp.tokens is None

    # Step 2: Proving bypass codes (123456 / 000000) are REJECTED and cannot yield access tokens
    with pytest.raises(PermissionError) as exc_bypass1:
        verify_mfa_challenge(db_session, resp.mfa_ticket, "123456")
    assert "MFA_ENROLMENT_REQUIRED" in str(exc_bypass1.value)

    with pytest.raises(PermissionError) as exc_bypass2:
        verify_mfa_challenge(db_session, resp.mfa_ticket, "000000")
    assert "MFA_ENROLMENT_REQUIRED" in str(exc_bypass2.value)

    # Step 3: Admin completes forced TOTP enrolment
    totp_secret = generate_totp_secret()
    valid_code = pyotp.TOTP(totp_secret).now()

    tokens = complete_admin_mfa_enrolment(
        session=db_session,
        mfa_ticket=resp.mfa_ticket,
        totp_secret=totp_secret,
        totp_code=valid_code,
    )
    assert tokens.access_token is not None
    assert "LK_ADMIN" in tokens.roles

    # Verify secret is stored ENCRYPTED at rest in database
    db_session.expire_all()
    user_db = db_session.get(User, user.id)
    assert user_db is not None
    assert user_db.totp_secret != totp_secret  # Ciphertext, NOT plaintext
    assert decrypt_field(user_db.totp_secret) == totp_secret
    assert user_db.totp_enabled is True

    # Step 4: Subsequent login attempts prompt for TOTP code (enrolment already complete)
    resp2 = login_flow(
        session=db_session,
        email="admin@csm.tech",
        password="AdminSecret2026!",
    )
    assert resp2.mfa_required is True
    assert resp2.mfa_enrolment_required is False

    # Negative test: Submitting obsolete bypass code '123456' is strictly rejected
    with pytest.raises(ValueError) as exc_invalid:
        verify_mfa_challenge(db_session, resp2.mfa_ticket, "123456")
    assert "Invalid multi-factor authentication code" in str(exc_invalid.value)

    # Positive test: Genuine TOTP code succeeds
    real_code2 = pyotp.TOTP(totp_secret).now()
    tokens2 = verify_mfa_challenge(db_session, resp2.mfa_ticket, real_code2)
    assert tokens2.access_token is not None
    assert "LK_ADMIN" in tokens2.roles


def test_login_rate_limiting_and_account_lockout(db_session: Session) -> None:
    """Verify that 5 failed login attempts trigger account lockout and reject further attempts."""
    rate_limiter.reset_for_testing()

    org = Organisation(name="CSM Tech", code="CSM_LOCKOUT")
    db_session.add(org)
    db_session.flush()

    user = User(
        org_id=org.id,
        email="lockout_victim@csm.tech",
        password_hash=hash_password("CorrectPassword123!"),
        full_name="Lockout Victim",
    )
    db_session.add(user)
    db_session.commit()

    # Perform 4 consecutive failed login attempts
    for _ in range(4):
        with pytest.raises(ValueError) as exc:
            login_flow(db_session, "lockout_victim@csm.tech", "WrongPassword!")
        assert "Invalid email or password" in str(exc.value)

    # 5th failed attempt triggers account lockout
    with pytest.raises(ValueError):
        login_flow(db_session, "lockout_victim@csm.tech", "WrongPassword!")

    # 6th attempt (even with CORRECT password) is rejected with ACCOUNT_LOCKED
    with pytest.raises(PermissionError) as lock_exc:
        login_flow(db_session, "lockout_victim@csm.tech", "CorrectPassword123!")
    assert "ACCOUNT_LOCKED" in str(lock_exc.value)

    rate_limiter.reset_for_testing()


def test_refresh_token_rotation_and_single_use(db_session: Session) -> None:
    """Verify single-use refresh token rotation issuing new access and refresh tokens."""
    org = Organisation(name="CSM Tech", code="CSM_ROTATION")
    db_session.add(org)
    db_session.flush()

    user = User(
        org_id=org.id,
        email="rotator@csm.tech",
        password_hash=hash_password("Pass123!"),
        full_name="Rotation Test",
    )
    db_session.add(user)
    db_session.commit()

    # Initial login
    login_resp = login_flow(db_session, "rotator@csm.tech", "Pass123!")
    assert login_resp.tokens is not None
    token_v1 = login_resp.tokens.refresh_token

    # Rotate token v1 -> receives token v2
    token_v2_resp = rotate_refresh_token(db_session, token_v1)
    assert token_v2_resp.refresh_token != token_v1
    assert token_v2_resp.access_token is not None

    # Verify that v1 is now revoked in the database
    tokens = db_session.execute(select(RefreshToken)).scalars().all()
    assert len(tokens) == 2
    v1_rec = [t for t in tokens if t.replaced_by_token_id is not None][0]
    assert v1_rec.is_revoked is True


def test_token_family_reuse_detection_and_revocation(db_session: Session) -> None:
    """CRITICAL SECURITY TEST: Replaying an already-rotated token revokes the entire token family."""
    org = Organisation(name="CSM Tech", code="CSM_REPLAY")
    db_session.add(org)
    db_session.flush()

    user = User(
        org_id=org.id,
        email="victim@csm.tech",
        password_hash=hash_password("VictimPass123!"),
        full_name="Victim User",
    )
    db_session.add(user)
    db_session.commit()

    # Step 1: Legit user logs in and obtains token v1
    login_resp = login_flow(db_session, "victim@csm.tech", "VictimPass123!")
    assert login_resp.tokens is not None
    stolen_token_v1 = login_resp.tokens.refresh_token

    # Step 2: Legit user legitimately rotates token v1 -> obtains token v2
    rotate_resp = rotate_refresh_token(db_session, stolen_token_v1)
    token_v2 = rotate_resp.refresh_token

    # Step 3: Attacker replays stolen_token_v1 (TOKEN REUSE ATTACK)
    with pytest.raises(PermissionError) as exc_info:
        rotate_refresh_token(db_session, stolen_token_v1)

    assert "Security Violation: Token reuse detected" in str(exc_info.value)

    # Step 4: Verify the entire session family (including token v2) has been terminated
    all_tokens = db_session.execute(select(RefreshToken)).scalars().all()
    assert len(all_tokens) >= 2
    assert all(t.is_revoked is True for t in all_tokens)

    # Step 5: Verify security incident was recorded in immutable audit log
    alerts = (
        db_session.execute(select(AuditLog).where(AuditLog.action == "security_alert_token_reuse"))
        .scalars()
        .all()
    )
    assert len(alerts) == 1
    assert "Replay attack detected" in str(alerts[0].reason)

    # Step 6: Even legit token v2 is now revoked and cannot be used
    with pytest.raises(PermissionError):
        rotate_refresh_token(db_session, token_v2)


def test_totp_setup_and_verification(db_session: Session) -> None:
    """Verify TOTP secret generation, provisioning URI, and code verification."""
    org = Organisation(name="CSM Tech", code="CSM_TOTP")
    db_session.add(org)
    db_session.flush()

    user = User(
        org_id=org.id,
        email="totp_user@csm.tech",
        password_hash="hash",
        full_name="TOTP User",
    )
    db_session.add(user)
    db_session.commit()

    # Setup MFA
    setup = setup_totp_mfa(db_session, user.id)
    assert len(setup.secret) >= 16
    assert setup.otpauth_uri.startswith("otpauth://totp/")
    assert "totp_user%40csm.tech" in setup.otpauth_uri or "totp_user@csm.tech" in setup.otpauth_uri

    # Generate current code using user's secret
    import pyotp

    totp = pyotp.TOTP(setup.secret)
    current_code = totp.now()

    # Verify code
    assert verify_totp(setup.secret, current_code) is True
    assert verify_totp(setup.secret, "000000") is False


def test_logout_revokes_session(db_session: Session) -> None:
    """Verify that logging out revokes the refresh token."""
    org = Organisation(name="CSM Tech", code="CSM_LOGOUT")
    db_session.add(org)
    db_session.flush()

    user = User(
        org_id=org.id,
        email="logout_user@csm.tech",
        password_hash=hash_password("Pass123!"),
        full_name="Logout User",
    )
    db_session.add(user)
    db_session.commit()

    resp = login_flow(db_session, "logout_user@csm.tech", "Pass123!")
    assert resp.tokens is not None
    token = resp.tokens.refresh_token

    logout_session(db_session, token)

    # Attempting to rotate revoked token fails
    with pytest.raises(PermissionError):
        rotate_refresh_token(db_session, token)
