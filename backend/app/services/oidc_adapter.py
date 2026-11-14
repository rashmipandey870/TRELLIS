"""TRELLIS OIDC Authentication Adapter & Development Mock."""

from abc import ABC, abstractmethod
from typing import Any

from app.core.config import settings


class OidcAuthAdapter(ABC):
    """Abstract interface for Microsoft Entra ID and OIDC SSO identity providers."""

    @abstractmethod
    def get_authorization_url(self, state: str, redirect_uri: str) -> str:
        """Construct identity provider login redirect URL."""
        pass

    @abstractmethod
    def authenticate_callback(self, code: str, redirect_uri: str) -> dict[str, Any]:
        """Exchange authorization code for validated user profile claims."""
        pass


class MockOidcAdapter(OidcAuthAdapter):
    """Deterministic mock OIDC adapter gated strictly to TRELLIS_ENV=dev."""

    def __init__(self) -> None:
        if settings.ENVIRONMENT != "dev":
            raise RuntimeError(
                "MOCK_OIDC_FORBIDDEN: MockOidcAdapter is strictly gated to TRELLIS_ENV=dev "
                "and cannot be instantiated in staging or production environments."
            )

    def get_authorization_url(self, state: str, redirect_uri: str) -> str:
        return f"{redirect_uri}?code=mock_auth_code_csm_2026&state={state}"

    def authenticate_callback(self, code: str, redirect_uri: str) -> dict[str, Any]:
        if code != "mock_auth_code_csm_2026":
            raise ValueError("Invalid mock authorization code")

        return {
            "sub": "entra-mock-user-001",
            "email": "priya.sharma@csm.tech",
            "name": "Priya Sharma",
            "roles": ["EMPLOYEE"],
            "tid": "csm-technology-tenant-id",
        }


def get_oidc_adapter() -> OidcAuthAdapter:
    """Retrieve active OIDC adapter gated by runtime environment."""
    if settings.ENVIRONMENT == "dev":
        return MockOidcAdapter()
    raise RuntimeError(
        "PRODUCTION_OIDC_UNCONFIGURED: Microsoft Entra ID production tenant credentials "
        "have not been configured by CSM IT."
    )
