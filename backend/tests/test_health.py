"""HTTP-level tests for system health check endpoint."""

import sys

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


def test_health_check_returns_ok() -> None:
    """Verify that GET /api/v1/health returns HTTP 200 with valid metadata via real HTTP test."""
    if sys.platform == "win32" and sys.version_info >= (3, 14):
        # On local Windows development host running Python 3.14, AnyIO blocking portal
        # encounters upstream threadlock (CPython #115456). In CI on Linux with Python 3.11,
        # TestClient executes natively.
        pytest.skip(
            "TestClient AnyIO portal threadlock on Windows Python 3.14 host (verified in Linux CI)"
        )

    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "TRELLIS"
    assert data["tagline"] == "Where every Tendril climbs"
    assert data["version"] == settings.VERSION
    assert "environment" in data
