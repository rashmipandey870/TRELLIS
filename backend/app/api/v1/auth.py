"""TRELLIS Authentication API Endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_user_claims, get_db
from app.core.security import get_jwks
from app.models import User
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    MfaChallengeRequest,
    MfaSetupResponse,
    SessionInfoResponse,
    TokenRefreshRequest,
    TokenResponse,
    UserMeResponse,
)
from app.services.auth_service import (
    get_user_sessions,
    login_flow,
    logout_session,
    rotate_refresh_token,
    setup_totp_mfa,
    verify_mfa_challenge,
)
from app.services.oidc_adapter import get_oidc_adapter

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
def login(
    payload: LoginRequest,
    request: Request,
    user_agent: str | None = Header(None),
    db: Session = Depends(get_db),
) -> LoginResponse:
    """Authenticate user with email and password, gating admin roles behind TOTP MFA."""
    client_ip = request.client.host if request.client else "127.0.0.1"
    try:
        return login_flow(
            session=db,
            email=payload.email,
            password=payload.password,
            device_info=user_agent,
            ip_address=client_ip,
            org_code=payload.org_code,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.post("/mfa/challenge", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def challenge_mfa(
    payload: MfaChallengeRequest,
    request: Request,
    user_agent: str | None = Header(None),
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Solve MFA challenge with 6-digit TOTP code or recovery code."""
    client_ip = request.client.host if request.client else "127.0.0.1"
    try:
        return verify_mfa_challenge(
            session=db,
            mfa_ticket=payload.mfa_ticket,
            totp_code=payload.totp_code,
            device_info=user_agent,
            ip_address=client_ip,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.post("/mfa/setup", response_model=MfaSetupResponse, status_code=status.HTTP_200_OK)
def setup_mfa(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MfaSetupResponse:
    """Provision Base32 TOTP secret and otpauth URI for user authenticator app."""
    try:
        return setup_totp_mfa(session=db, user_id=current_user.id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def refresh_token_endpoint(
    payload: TokenRefreshRequest,
    request: Request,
    user_agent: str | None = Header(None),
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Single-use refresh token rotation with token family reuse revocation."""
    client_ip = request.client.host if request.client else "127.0.0.1"
    try:
        return rotate_refresh_token(
            session=db,
            raw_refresh_token=payload.refresh_token,
            device_info=user_agent,
            ip_address=client_ip,
        )
    except PermissionError as exc:
        # Replay attack token reuse detection
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    payload: TokenRefreshRequest,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Revoke active refresh token session."""
    logout_session(session=db, raw_refresh_token=payload.refresh_token)
    return {"message": "Session successfully logged out."}


@router.get("/me", response_model=UserMeResponse, status_code=status.HTTP_200_OK)
def get_me(
    current_user: User = Depends(get_current_user),
    claims: dict[str, Any] = Depends(get_current_user_claims),
) -> UserMeResponse:
    """Retrieve profile and assigned roles for currently authenticated user."""
    roles = claims.get("roles", ["EMPLOYEE"])
    return UserMeResponse(
        id=current_user.id,
        org_id=current_user.org_id,
        email=current_user.email,
        full_name=current_user.full_name,
        avatar_url=current_user.avatar_url,
        roles=roles,
        preferences_json=current_user.preferences_json,
    )


@router.get("/sessions", response_model=list[SessionInfoResponse], status_code=status.HTTP_200_OK)
def list_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[SessionInfoResponse]:
    """List active devices and login sessions for current user."""
    return get_user_sessions(session=db, user_id=current_user.id)


@router.get("/.well-known/jwks.json", tags=["Security"], status_code=status.HTTP_200_OK)
def public_jwks() -> dict[str, Any]:
    """Expose RFC 7517 JSON Web Key Set (JWKS) for asymmetric token validation and rotation."""
    return get_jwks()


@router.get("/oidc/login", tags=["SSO"])
def oidc_login_redirect(
    state: str = "default_state", redirect_uri: str = "http://localhost:4200/auth/callback"
) -> dict[str, str]:
    """Return Microsoft Entra ID authorization redirect URL."""
    adapter = get_oidc_adapter()
    url = adapter.get_authorization_url(state, redirect_uri)
    return {"authorization_url": url}
