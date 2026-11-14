"""TRELLIS Authentication & Token Lifecycle Service."""

import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    decrypt_field,
    encrypt_field,
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
from app.services.rate_limiter import rate_limiter

# In-memory temporary MFA exchange tickets: {ticket: (user_id, expires_at, is_enrolment)}
_MFA_TICKETS: dict[str, tuple[str, datetime, bool]] = {}


def get_active_user_roles(user: User, as_of: datetime | None = None) -> list[str]:
    """Derive active role codes, strictly excluding expired time-limited grants."""
    now = as_of or datetime.now(UTC)
    active_roles: list[str] = []
    for g in user.grants:
        if not g.role or not g.role.code:
            continue
        if getattr(g, "status", "GRANTED") != "GRANTED":
            continue
        if g.expires_at is not None:
            exp = g.expires_at
            if exp.tzinfo is None:
                exp = exp.replace(tzinfo=UTC)
            if exp <= now:
                continue
        active_roles.append(g.role.code)
    return active_roles or ["EMPLOYEE"]


def authenticate_user(
    session: Session,
    email: str,
    password: str,
    org_code: str | None = None,
) -> tuple[User, list[str]]:
    """Validate user credentials and return active user entity and assigned roles."""
    # Check rate limiter / account lockout first
    rate_limiter.check_login_allowed(email)

    query = select(User).where(User.email == email, User.is_active.is_(True))
    if org_code:
        query = query.join(Organisation).where(Organisation.code == org_code)

    user = session.execute(query).scalars().first()
    if not user:
        rate_limiter.record_login_failure(email)
        raise ValueError("Invalid email or password.")

    if not verify_password(password, user.password_hash):
        rate_limiter.record_login_failure(email)
        raise ValueError("Invalid email or password.")

    # Successful authentication clears failed attempt counts
    rate_limiter.record_login_success(email)

    # Collect active role codes strictly excluding expired grants
    role_codes = get_active_user_roles(user)

    return user, role_codes


def login_flow(
    session: Session,
    email: str,
    password: str,
    device_info: str | None = None,
    ip_address: str | None = None,
    org_code: str | None = None,
    request_id: str | None = None,
) -> LoginResponse:
    """Execute complete login flow with role-based TOTP MFA gating and forced enrolment."""
    user, roles = authenticate_user(session, email, password, org_code)

    # Invariant: LK_ADMIN and SUPER_ADMIN strictly require TOTP MFA
    admin_roles = {"LK_ADMIN", "SUPER_ADMIN"}
    is_admin = bool(admin_roles.intersection(roles))
    requires_mfa = is_admin or user.totp_enabled

    if requires_mfa:
        # Check if admin has NOT enrolled a TOTP secret yet
        is_enrolment_required = is_admin and (not user.totp_secret or not user.totp_enabled)

        # Generate single-use MFA exchange ticket valid for 5 minutes
        mfa_ticket = f"mfa_ticket_{generate_secure_token()}"
        expires_at = datetime.now(UTC) + timedelta(minutes=5)
        _MFA_TICKETS[mfa_ticket] = (user.id, expires_at, is_enrolment_required)

        # Log MFA challenge event in immutable audit log within the transaction
        audit = AuditLog(
            org_id=user.org_id,
            actor_id=user.id,
            action="login_mfa_enrolment_required"
            if is_enrolment_required
            else "login_mfa_challenge_issued",
            resource="users",
            resource_id=user.id,
            ip_address=ip_address,
            user_agent=device_info,
            reason="Admin role requires multi-factor authentication; forced enrolment active"
            if is_enrolment_required
            else "Admin role or TOTP policy requires multi-factor authentication",
            before_state_json={"totp_enabled": user.totp_enabled},
            after_state_json={
                "mfa_ticket": mfa_ticket[:16] + "...",
                "enrolment_required": is_enrolment_required,
            },
            request_id=request_id,
        )
        try:
            session.add(audit)
            session.commit()
        except Exception:
            session.rollback()
            raise

        if is_enrolment_required:
            return LoginResponse(
                mfa_required=True,
                mfa_enrolment_required=True,
                mfa_ticket=mfa_ticket,
                message="Administrator MFA enrolment required. You must configure an authenticator app before access tokens can be issued.",
            )

        return LoginResponse(
            mfa_required=True,
            mfa_enrolment_required=False,
            mfa_ticket=mfa_ticket,
            message="Multi-factor authentication required. Please enter your 6-digit TOTP code.",
        )

    # Standard login without MFA requirement
    tokens = issue_tokens_for_user(
        session, user, roles, device_info, ip_address, request_id=request_id
    )
    return LoginResponse(mfa_required=False, tokens=tokens)


def issue_tokens_for_user(
    session: Session,
    user: User,
    roles: list[str],
    device_info: str | None = None,
    ip_address: str | None = None,
    family_id: str | None = None,
    request_id: str | None = None,
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

    # Write immutable audit event in the same transaction
    audit = AuditLog(
        org_id=user.org_id,
        actor_id=user.id,
        action="login_success" if family_id is None else "token_refresh_success",
        resource="refresh_tokens",
        resource_id=token_family,
        ip_address=ip_address,
        user_agent=device_info,
        reason="Cryptographic tokens issued",
        after_state_json={"family_id": token_family, "roles": roles},
        request_id=request_id,
    )
    try:
        try:
            session.add(audit)
            session.commit()
        except Exception:
            session.rollback()
            raise
    except Exception:
        session.rollback()
        raise

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
    request_id: str | None = None,
) -> TokenResponse:
    """Validate 6-digit TOTP code against registered secret; bypass codes are strictly forbidden."""
    ticket_data = _MFA_TICKETS.get(mfa_ticket)
    if not ticket_data:
        raise ValueError("Invalid or expired MFA exchange ticket.")

    user_id, expires_at, is_enrolment = ticket_data
    if datetime.now(UTC) > expires_at:
        del _MFA_TICKETS[mfa_ticket]
        raise ValueError("MFA exchange ticket has expired.")

    user = session.get(User, user_id)
    if not user:
        raise ValueError("User not found.")

    # Invariant: An admin without a registered TOTP secret CANNOT receive access tokens
    if is_enrolment or not user.totp_secret or not user.totp_enabled:
        raise PermissionError(
            "MFA_ENROLMENT_REQUIRED: Administrator has not enrolled a TOTP secret. "
            "You must complete enrolment before access tokens can be issued."
        )

    # Decrypt TOTP secret from encrypted-at-rest storage
    plain_secret = decrypt_field(user.totp_secret)
    valid = verify_totp(plain_secret, totp_code)

    if not valid:
        # Log failure in audit log
        audit = AuditLog(
            org_id=user.org_id,
            actor_id=user.id,
            action="login_mfa_failed",
            resource="users",
            resource_id=user.id,
            ip_address=ip_address,
            user_agent=device_info,
            reason="Invalid TOTP authentication code submitted; bypass codes rejected",
            request_id=request_id,
        )
        try:
            session.add(audit)
            session.commit()
        except Exception:
            session.rollback()
            raise
        raise ValueError("Invalid multi-factor authentication code.")

    # Consume ticket
    del _MFA_TICKETS[mfa_ticket]

    role_codes = get_active_user_roles(user)
    return issue_tokens_for_user(
        session, user, role_codes, device_info, ip_address, request_id=request_id
    )


def complete_admin_mfa_enrolment(
    session: Session,
    mfa_ticket: str,
    totp_secret: str,
    totp_code: str,
    device_info: str | None = None,
    ip_address: str | None = None,
    request_id: str | None = None,
) -> TokenResponse:
    """Complete forced TOTP enrolment for an admin and issue tokens upon verified code."""
    ticket_data = _MFA_TICKETS.get(mfa_ticket)
    if not ticket_data:
        raise ValueError("Invalid or expired MFA exchange ticket.")

    user_id, expires_at, _ = ticket_data
    if datetime.now(UTC) > expires_at:
        del _MFA_TICKETS[mfa_ticket]
        raise ValueError("MFA exchange ticket has expired.")

    user = session.get(User, user_id)
    if not user:
        raise ValueError("User not found.")

    # Verify the code against the secret to prove the user scanned the QR code
    if not verify_totp(totp_secret, totp_code):
        raise ValueError("Invalid verification code for TOTP enrolment.")

    before_state = {"totp_enabled": user.totp_enabled}

    # Encrypt secret at rest before saving
    user.totp_secret = encrypt_field(totp_secret)
    user.totp_enabled = True

    # Write audit log in same transaction
    audit = AuditLog(
        org_id=user.org_id,
        actor_id=user.id,
        action="mfa_enrolment_completed",
        resource="users",
        resource_id=user.id,
        ip_address=ip_address,
        user_agent=device_info,
        reason="Admin completed forced TOTP enrolment",
        before_state_json=before_state,
        after_state_json={"totp_enabled": True},
        request_id=request_id,
    )
    try:
        try:
            session.add(audit)
            session.commit()
        except Exception:
            session.rollback()
            raise
    except Exception:
        session.rollback()
        raise

    # Consume ticket
    del _MFA_TICKETS[mfa_ticket]

    role_codes = get_active_user_roles(user)
    return issue_tokens_for_user(
        session, user, role_codes, device_info, ip_address, request_id=request_id
    )


def rotate_refresh_token(
    session: Session,
    raw_refresh_token: str,
    device_info: str | None = None,
    ip_address: str | None = None,
    request_id: str | None = None,
) -> TokenResponse:
    """Execute single-use token rotation with strict token family reuse detection."""
    token_hash_val = hash_token(raw_refresh_token)

    query = select(RefreshToken).where(RefreshToken.token_hash == token_hash_val)
    token_record = session.execute(query).scalars().first()

    if not token_record:
        raise ValueError("Invalid refresh token.")

    # INVARIANT: Check for Token Reuse Attack
    if token_record.is_revoked or token_record.replaced_by_token_id is not None:
        family_id = token_record.family_id

        # IMMEDIATELY REVOKE THE ENTIRE TOKEN FAMILY
        session.execute(
            update(RefreshToken).where(RefreshToken.family_id == family_id).values(is_revoked=True)
        )

        # Log high-severity security incident in the same transaction
        audit = AuditLog(
            org_id=token_record.org_id,
            actor_id=token_record.user_id,
            action="security_alert_token_reuse",
            resource="refresh_tokens",
            resource_id=family_id,
            ip_address=ip_address,
            user_agent=device_info,
            reason="CRITICAL: Replay attack detected on rotated refresh token. Session family revoked.",
            request_id=request_id,
        )
        try:
            session.add(audit)
            session.commit()
        except Exception:
            session.rollback()
            raise

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

    role_codes = get_active_user_roles(user)

    # Issue new token continuing the SAME family
    new_tokens = issue_tokens_for_user(
        session=session,
        user=user,
        roles=role_codes,
        device_info=device_info,
        ip_address=ip_address,
        family_id=token_record.family_id,
        request_id=request_id,
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
    """Generate TOTP secret and return provisioning URI for authenticator apps."""
    user = session.get(User, user_id)
    if not user:
        raise ValueError("User not found.")

    secret = generate_totp_secret()
    # Note: store encrypted in DB
    user.totp_secret = encrypt_field(secret)
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
