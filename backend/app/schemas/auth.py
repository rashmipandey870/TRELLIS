"""TRELLIS Authentication Pydantic Schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    """Payload for credentials login."""

    email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=1)
    org_code: str | None = None


class TokenResponse(BaseModel):
    """Access and refresh token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str
    roles: list[str]


class LoginResponse(BaseModel):
    """Response returned upon login attempt, signaling MFA requirement if user holds admin roles."""

    mfa_required: bool = False
    mfa_enrolment_required: bool = False
    mfa_ticket: str | None = None
    tokens: TokenResponse | None = None
    message: str | None = None


class MfaChallengeRequest(BaseModel):
    """Payload to solve MFA challenge using 6-digit TOTP code."""

    mfa_ticket: str
    totp_code: str = Field(..., min_length=6, max_length=12)


class MfaEnrolmentRequest(BaseModel):
    """Payload to complete forced admin MFA enrolment."""

    mfa_ticket: str
    totp_secret: str
    totp_code: str = Field(..., min_length=6, max_length=6)


class MfaSetupResponse(BaseModel):
    """Response containing secret and provisioning URI for authenticator app configuration."""

    secret: str
    otpauth_uri: str


class TokenRefreshRequest(BaseModel):
    """Payload for single-use refresh token rotation."""

    refresh_token: str


class SessionInfoResponse(BaseModel):
    """Information regarding an active user session."""

    model_config = ConfigDict(from_attributes=True)

    family_id: str
    device_info: str | None = None
    ip_address: str | None = None
    created_at: datetime
    expires_at: datetime
    is_current: bool = False


class UserMeResponse(BaseModel):
    """Authenticated user profile response."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    org_id: str
    email: str
    full_name: str
    avatar_url: str | None = None
    roles: list[str]
    role: str = "LEARNER"
    preferences_json: dict[str, Any] | None = None
