"""Tests for system health check endpoint."""

from app.core.config import settings
from app.main import health_check


def test_health_check_returns_ok() -> None:
    """Verify that health_check endpoint returns valid status and metadata."""
    coro = health_check()
    try:
        coro.send(None)
        raise AssertionError("Coroutine did not complete")
    except StopIteration as exc:
        data = exc.value

    assert data["status"] == "ok"
    assert data["app"] == "TRELLIS"
    assert data["tagline"] == "Where every Tendril climbs"
    assert data["version"] == settings.VERSION
    assert "environment" in data
