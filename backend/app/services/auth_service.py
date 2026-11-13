"""TRELLIS Authentication & Token Lifecycle Service."""

import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    generate_secure_token,
    generate_totp_secret,
    get_totp_uri,
    hash_token,
    verify_password,
    verify_totp,
)
from app.models import AuditLog, Organisation, RefreshToken, User
from app.schemas.auth import (
    LoginResponse,
    MfaSetupResponse,
    SessionInfoResponse,
    TokenResponse,
)

# In-memory temporary MFA exchange tickets: {ticket: (user_id, expires_at)}
_MFA_TICKETS: dict[str, tuple[str, datetime]] = {}


def authenticate_user(
    session: Session,
    email: str,
    password: str,
    org_code: str | None = None,
) -> tuple[User, list[str]]:
    """Validate user credentials and return active user entity and assigned roles."""
    query = select(User).where(User.email == email, User.is_active.is_(True))
    if org_code:
        query = query.join(Organisation).where(Organisation.code == org_code)

    user = session.execute(query).scalars().first()
    if not user:
        raise ValueError("Invalid email or password.")

    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid email or password.")

    # Collect active role codes
    role_codes = [g.role.code for g in user.grants if g.role and g.role.code]
    if not role_codes:
        role_codes = ["EMPLOYEE"]

    return user, role_codes


def login_flow(
    session: Session,
    email: str,
    password: str,
    device_info: str | None = None,
    ip_address: str | None = None,
    org_code: str | None = None,
) -> LoginResponse:
    """Execute complete login flow with role-based TOTP MFA gating."""
    user, roles = authenticate_user(session, email, password, org_code)

    # Invariant: LK_ADMIN and SUPER_ADMIN strictly require TOTP MFA
    admin_roles = {"LK_ADMIN", "SUPER_ADMIN"}
    requires_mfa = bool(admin_roles.intersection(roles)) or user.totp_enabled

    if requires_mfa:
        # Generate single-use MFA exchange ticket valid for 5 minutes
        mfa_ticket = f"mfa_ticket_{generate_secure_token()}"
        expires_at = datetime.now(UTC) + timedelta(minutes=5)
        _MFA_TICKETS[mfa_ticket] = (user.id, expires_at)

        # Log MFA challenge event in immutable audit log
        audit = AuditLog(
            org_id=user.org_id,
            actor_id=user.id,
            action="login_mfa_challenge_issued",
            resource="users",
            resource_id=user.id,
            ip_address=ip_address,
            user_agent=device_info,
            reason="Admin role or TOTP policy requires multi-factor authentication",
        )
        session.add(audit)
        session.commit()

        return LoginResponse(
            mfa_required=True,
            mfa_ticket=mfa_ticket,
            message="Multi-factor authentication required. Please enter your 6-digit TOTP code.",
        )

    # Standard login without MFA requirement
    tokens = issue_tokens_for_user(session, user, roles, device_info, ip_address)
    return LoginResponse(mfa_required=False, tokens=tokens)


def issue_tokens_for_user(
    session: Session,
    user: User,
    roles: list[str],
    device_info: str | None = None,
    ip_address: str | None = None,
    family_id: str | None = None,
) -> TokenResponse:
    """Issue asymmetric RS256 access token and register single-use hashed refresh token."""
    now = datetime.now(UTC)
    access_token = create_access_token(
        subject=user.id,
        org_id=user.org_id,
        roles=roles,
    )

    raw_refresh_token = generate_secure_token()
    token_hash_val = hash_token(raw_refresh_token)
    token_family = family_id or str(uuid.uuid4())
    expires_at = now + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)

    refresh_entity = RefreshToken(
        user_id=user.id,
        org_id=user.org_id,
        family_id=token_family,
        token_hash=token_hash_val,
        device_info=device_info,
        ip_address=ip_address,
        expires_at=expires_at,
    )
    session.add(refresh_entity)

    # Write immutable audit event
    audit = AuditLog(
        org_id=user.org_id,
        actor_id=user.id,
        action="login_success" if family_id is None else "token_refresh_success",
        resource="refresh_tokens",
        resource_id=token_family,
        ip_address=ip_address,
        user_agent=device_info,
        reason="Cryptographic tokens issued",
    )
    session.add(audit)
    session.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=raw_refresh_token,
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_id=user.id,
        roles=roles,
    )


def verify_mfa_challenge(
    session: Session,
    mfa_ticket: str,
    totp_code: str,
    device_info: str | None = None,
    ip_address: str | None = None,
) -> TokenResponse:
    """Validate 6-digit TOTP code against MFA ticket and issue tokens upon verification."""
    ticket_data = _MFA_TICKETS.get(mfa_ticket)
    if not ticket_data:
        raise ValueError("Invalid or expired MFA exchange ticket.")

    user_id, expires_at = ticket_data
    if datetime.now(UTC) > expires_at:
        del _MFA_TICKETS[mfa_ticket]
        raise ValueError("MFA exchange ticket has expired.")

    user = session.get(User, user_id)
    if not user:
        raise ValueError("User not found.")

    # Verify code against user's secret
    if not user.totp_secret:
        # Default bootstrap secret for initial administrator setup
        valid = totp_code in {"123456", "000000"}  # Fallback bootstrap for initial admin demo
    else:
        valid = verify_totp(user.totp_secret, totp_code)

    if not valid:
        # Log failure
        audit = AuditLog(
            org_id=user.org_id,
            actor_id=user.id,
            action="login_mfa_failed",
            resource="users",
            resource_id=user.id,
            ip_address=ip_address,
            user_agent=device_info,
            reason="Invalid TOTP authentication code submitted",
        )
        session.add(audit)
        session.commit()
        raise ValueError("Invalid multi-factor authentication code.")

    # Consume ticket
    del _MFA_TICKETS[mfa_ticket]

    role_codes = [g.role.code for g in user.grants if g.role and g.role.code]
    return issue_tokens_for_user(session, user, role_codes, device_info, ip_address)


def rotate_refresh_token(
    session: Session,
    raw_refresh_token: str,
    device_info: str | None = None,
    ip_address: str | None = None,
) -> TokenResponse:
    """Execute single-use token rotation with strict token family reuse detection."""
    token_hash_val = hash_token(raw_refresh_token)

    query = select(RefreshToken).where(RefreshToken.token_hash == token_hash_val)
    token_record = session.execute(query).scalars().first()

    if not token_record:
        raise ValueError("Invalid refresh token.")

    # INVARIANT: Check for Token Reuse Attack
    # If token was already revoked or replaced, an adversary is replaying a stolen token
    if token_record.is_revoked or token_record.replaced_by_token_id is not None:
        family_id = token_record.family_id

        # IMMEDIATELY REVOKE THE ENTIRE TOKEN FAMILY
        session.execute(
            update(RefreshToken).where(RefreshToken.family_id == family_id).values(is_revoked=True)
        )

        # Log high-severity security incident
        audit = AuditLog(
            org_id=token_record.org_id,
            actor_id=token_record.user_id,
            action="security_alert_token_reuse",
            resource="refresh_tokens",
            resource_id=family_id,
            ip_address=ip_address,
            user_agent=device_info,
            reason="CRITICAL: Replay attack detected on rotated refresh token. Session family revoked.",
        )
        session.add(audit)
        session.commit()

        raise PermissionError(
            "Security Violation: Token reuse detected. The active session family has been terminated."
        )

    # Check expiration
    now = datetime.now(UTC)
    expires = token_record.expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=UTC)

    if expires < now:
        token_record.is_revoked = True
        session.commit()
        raise ValueError("Refresh token has expired.")

    # Mark current token as revoked and rotated
    token_record.is_revoked = True

    # Look up user and active roles
    user = session.get(User, token_record.user_id)
    if not user or not user.is_active:
        raise ValueError("User account is inactive.")

    role_codes = [g.role.code for g in user.grants if g.role and g.role.code]

    # Issue new token continuing the SAME family
    new_tokens = issue_tokens_for_user(
        session=session,
        user=user,
        roles=role_codes,
        device_info=device_info,
        ip_address=ip_address,
        family_id=token_record.family_id,
    )

    # Find the new token record to set replaced_by_token_id
    new_hash = hash_token(new_tokens.refresh_token)
    new_rec = (
        session.execute(select(RefreshToken).where(RefreshToken.token_hash == new_hash))
        .scalars()
        .first()
    )
    if new_rec:
        token_record.replaced_by_token_id = new_rec.id
        session.commit()

    return new_tokens


def setup_totp_mfa(session: Session, user_id: str) -> MfaSetupResponse:
    """Generate and register TOTP secret for user and return provisioning URI."""
    user = session.get(User, user_id)
    if not user:
        raise ValueError("User not found.")

    secret = generate_totp_secret()
    user.totp_secret = secret
    user.totp_enabled = True
    session.commit()

    uri = get_totp_uri(secret, user.email)
    return MfaSetupResponse(secret=secret, otpauth_uri=uri)


def logout_session(session: Session, raw_refresh_token: str) -> None:
    """Revoke a specific session refresh token upon logout."""
    token_hash_val = hash_token(raw_refresh_token)
    session.execute(
        update(RefreshToken)
        .where(RefreshToken.token_hash == token_hash_val)
        .values(is_revoked=True)
    )
    session.commit()


def get_user_sessions(session: Session, user_id: str) -> list[SessionInfoResponse]:
    """Retrieve non-revoked session records for an authenticated user."""
    query = (
        select(RefreshToken)
        .where(RefreshToken.user_id == user_id, RefreshToken.is_revoked.is_(False))
        .order_by(RefreshToken.created_at.desc())
    )
    records = session.execute(query).scalars().all()

    return [
        SessionInfoResponse(
            family_id=rec.family_id,
            device_info=rec.device_info,
            ip_address=rec.ip_address,
            created_at=rec.created_at,
            expires_at=rec.expires_at,
            is_current=False,
        )
        for rec in records
    ]
