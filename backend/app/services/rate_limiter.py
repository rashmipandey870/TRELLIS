"""TRELLIS Rate Limiter & Account Lockout Service.

Tracks failed authentication attempts and enforces temporary account lockout
via Redis. Outside TRELLIS_ENV=dev, Redis is strictly mandatory; if unavailable,
the service fails closed and raises a loud operational alert.
"""

from __future__ import annotations

import contextlib
from datetime import UTC, datetime, timedelta

import redis

from app.core.config import settings

# In-memory fallback used strictly in TRELLIS_ENV=dev for headless testing
_IN_MEMORY_ATTEMPTS: dict[str, tuple[int, datetime]] = {}
_IN_MEMORY_LOCKOUTS: dict[str, datetime] = {}


def _get_redis_client() -> redis.Redis | None:
    """Attempt connection to configured Redis instance."""
    try:
        client = redis.Redis.from_url(
            settings.REDIS_URL,
            socket_connect_timeout=0.5,
            socket_timeout=0.5,
            decode_responses=True,
        )
        client.ping()
        return client
    except Exception:
        return None


class LoginRateLimiter:
    """Manages login attempt counting and account lockout enforcement.

    Invariants:
    1. Outside TRELLIS_ENV=dev, rate limiting MUST fail closed if Redis is unavailable.
       Silent in-memory fallback in staging/production is forbidden.
    2. Accounts are locked for lockout_seconds after exceeding max_attempts.
    """

    def __init__(self, max_attempts: int = 5, lockout_seconds: int = 900) -> None:
        self.max_attempts = max_attempts
        self.lockout_seconds = lockout_seconds

    def check_login_allowed(self, identifier: str) -> None:
        """Check if account is currently locked out; raises PermissionError if locked."""
        client = _get_redis_client()
        lockout_key = f"trellis:lockout:{identifier.lower()}"

        if not client and settings.ENVIRONMENT != "dev":
            raise RuntimeError(
                "REDIS_UNAVAILABLE: Production rate limiting requires an operational Redis cluster. "
                "Silent in-memory fallback is forbidden outside TRELLIS_ENV=dev."
            )

        if client:
            try:
                ttl = client.ttl(lockout_key)
                if ttl > 0:
                    raise PermissionError(
                        f"ACCOUNT_LOCKED: Account is temporarily locked due to excessive failed attempts. "
                        f"Try again in {ttl} seconds."
                    )
                return
            except PermissionError:
                raise
            except Exception as exc:
                if settings.ENVIRONMENT != "dev":
                    raise RuntimeError(
                        f"REDIS_ERROR: Failed communicating with Redis rate limiting cluster: {exc}"
                    ) from exc

        # In-memory check (permitted in TRELLIS_ENV=dev only)
        now = datetime.now(UTC)
        locked_until = _IN_MEMORY_LOCKOUTS.get(identifier.lower())
        if locked_until and locked_until > now:
            remaining = int((locked_until - now).total_seconds())
            raise PermissionError(
                f"ACCOUNT_LOCKED: Account is temporarily locked due to excessive failed attempts. "
                f"Try again in {remaining} seconds."
            )

    def record_login_failure(self, identifier: str) -> int:
        """Record a failed login attempt. Returns current consecutive failure count."""
        client = _get_redis_client()
        key = f"trellis:attempts:{identifier.lower()}"
        lockout_key = f"trellis:lockout:{identifier.lower()}"

        if not client and settings.ENVIRONMENT != "dev":
            raise RuntimeError(
                "REDIS_UNAVAILABLE: Production rate limiting requires an operational Redis cluster. "
                "Silent in-memory fallback is forbidden outside TRELLIS_ENV=dev."
            )

        if client:
            try:
                attempts = client.incr(key)
                if attempts == 1:
                    client.expire(key, self.lockout_seconds)
                if attempts >= self.max_attempts:
                    client.setex(lockout_key, self.lockout_seconds, "locked")
                    client.delete(key)
                return attempts
            except Exception as exc:
                if settings.ENVIRONMENT != "dev":
                    raise RuntimeError(
                        f"REDIS_ERROR: Failed communicating with Redis rate limiting cluster: {exc}"
                    ) from exc

        # In-memory record (permitted in TRELLIS_ENV=dev only)
        now = datetime.now(UTC)
        current = _IN_MEMORY_ATTEMPTS.get(identifier.lower())
        attempts = 1 if not current or current[1] < now else current[0] + 1

        _IN_MEMORY_ATTEMPTS[identifier.lower()] = (
            attempts,
            now + timedelta(seconds=self.lockout_seconds),
        )

        if attempts >= self.max_attempts:
            _IN_MEMORY_LOCKOUTS[identifier.lower()] = now + timedelta(seconds=self.lockout_seconds)
            _IN_MEMORY_ATTEMPTS.pop(identifier.lower(), None)

        return attempts

    def record_login_success(self, identifier: str) -> None:
        """Clear failed attempts and lockout state upon successful authentication."""
        client = _get_redis_client()
        key = f"trellis:attempts:{identifier.lower()}"
        lockout_key = f"trellis:lockout:{identifier.lower()}"

        if client:
            with contextlib.suppress(Exception):
                client.delete(key, lockout_key)

        _IN_MEMORY_ATTEMPTS.pop(identifier.lower(), None)
        _IN_MEMORY_LOCKOUTS.pop(identifier.lower(), None)

    def reset_for_testing(self) -> None:
        """Clear all in-memory lockouts for unit tests."""
        _IN_MEMORY_ATTEMPTS.clear()
        _IN_MEMORY_LOCKOUTS.clear()


rate_limiter = LoginRateLimiter()
