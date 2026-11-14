"""TRELLIS Test Suite: Rate Limiting & Gating Security Invariants."""

import pytest

from app.core.config import settings
from app.services.oidc_adapter import MockOidcAdapter, get_oidc_adapter
from app.services.rate_limiter import LoginRateLimiter


def test_rate_limiter_fails_closed_outside_dev_when_redis_unavailable() -> None:
    original_env = settings.ENVIRONMENT
    limiter = LoginRateLimiter(max_attempts=5, lockout_seconds=60)
    try:
        # Switch environment to production
        settings.ENVIRONMENT = "production"

        # Attempting check_login_allowed without a live Redis cluster MUST raise loud RuntimeError
        with pytest.raises(RuntimeError) as exc_info:
            limiter.check_login_allowed("target_user@csm.tech")
        assert (
            "REDIS_UNAVAILABLE: Production rate limiting requires an operational Redis cluster"
            in str(exc_info.value)
        )

        with pytest.raises(RuntimeError) as exc_info:
            limiter.record_login_failure("target_user@csm.tech")
        assert (
            "REDIS_UNAVAILABLE: Production rate limiting requires an operational Redis cluster"
            in str(exc_info.value)
        )

    finally:
        settings.ENVIRONMENT = original_env


def test_mock_oidc_adapter_strictly_refuses_to_load_outside_dev() -> None:
    original_env = settings.ENVIRONMENT
    try:
        # 1. In dev, adapter loads cleanly
        settings.ENVIRONMENT = "dev"
        adapter = get_oidc_adapter()
        assert isinstance(adapter, MockOidcAdapter)

        # 2. Outside dev, MockOidcAdapter instantiation is forbidden
        settings.ENVIRONMENT = "production"
        with pytest.raises(RuntimeError) as exc_info:
            MockOidcAdapter()
        assert "MOCK_OIDC_FORBIDDEN" in str(exc_info.value)

        with pytest.raises(RuntimeError) as exc_info:
            get_oidc_adapter()
        assert "PRODUCTION_OIDC_UNCONFIGURED" in str(exc_info.value)

    finally:
        settings.ENVIRONMENT = original_env
