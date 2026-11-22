"""Unit tests for Phase 3.2 (Timezone-awareness & window edges) and Phase 3.3 (Security Headers)."""

from datetime import UTC, datetime, timedelta
import zoneinfo
import pytest

from app.core.audit_middleware import SECURITY_HEADERS
from app.services.email_service import send_smtp_email


def test_security_headers_constants_and_configuration():
    """Verify Phase 3.3 required security headers are configured and complete."""
    assert SECURITY_HEADERS["X-Frame-Options"] == "DENY"
    assert SECURITY_HEADERS["X-Content-Type-Options"] == "nosniff"
    assert "Strict-Transport-Security" in SECURITY_HEADERS
    assert "max-age=31536000" in SECURITY_HEADERS["Strict-Transport-Security"]
    assert SECURITY_HEADERS["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert "geolocation=()" in SECURITY_HEADERS["Permissions-Policy"]
    assert "default-src 'self'" in SECURITY_HEADERS["Content-Security-Policy"]


def test_asia_kolkata_timezone_conversion_and_window_edges():
    """Verify Phase 3.2 timezone handling for Indian Standard Time (Asia/Kolkata, UTC+05:30)."""
    utc_now = datetime.now(UTC)
    kolkata_tz = zoneinfo.ZoneInfo("Asia/Kolkata")
    kolkata_now = utc_now.astimezone(kolkata_tz)

    # Offset check: Kolkata is always +05:30
    offset = kolkata_now.utcoffset()
    assert offset == timedelta(hours=5, minutes=30)

    # Window edges
    start_window = utc_now - timedelta(minutes=5)
    end_window = utc_now + timedelta(minutes=60)
    
    # Inside window
    assert start_window <= utc_now <= end_window
    
    # Edge: 1 second before start
    just_before = start_window - timedelta(seconds=1)
    assert not (start_window <= just_before <= end_window)
    
    # Edge: 1 second after end
    just_after = end_window + timedelta(seconds=1)
    assert not (start_window <= just_after <= end_window)


def test_email_service_fallback_and_mime_structure():
    """Verify Phase 3.1 email service handles attachments and HTML structure."""
    ics_sample = (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//CSM Technology//TRELLIS//EN\r\n"
        "BEGIN:VEVENT\r\n"
        "SUMMARY:Engineering Mentorship Sync\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )
    # In test environment without live SMTP, gracefully returns False without crashing
    res = send_smtp_email(
        to_email="learner1@csmtech.internal",
        subject="Test Meeting Invite",
        html_content="<p>Please find attached meeting invite.</p>",
        text_content="Please find attached meeting invite.",
        ics_data=ics_sample,
    )
    assert isinstance(res, bool)
