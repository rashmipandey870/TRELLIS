"""TRELLIS Test Suite: Redis-Backed MFA Exchange Tickets & Invariants."""

from unittest.mock import patch

import pytest

from app.core.config import settings
from app.services.auth_service import consume_mfa_ticket, store_mfa_ticket


def test_mfa_ticket_single_use_and_consumption() -> None:
    ticket = "test_ticket_single_use_123456"
    user_id = "user_mfa_target_1"

    # 1. Store ticket with 300s TTL
    store_mfa_ticket(ticket=ticket, user_id=user_id, is_enrolment=True, ttl_seconds=300)

    # 2. First consumption: succeeds and returns data
    consumed = consume_mfa_ticket(ticket)
    assert consumed is not None
    consumed_user_id, is_enrolment = consumed
    assert consumed_user_id == user_id
    assert is_enrolment is True

    # 3. Second consumption (single-use invariant): MUST return None (ticket already burned)
    second_consumed = consume_mfa_ticket(ticket)
    assert second_consumed is None


def test_mfa_ticket_fails_closed_outside_dev_when_redis_unavailable() -> None:
    original_env = settings.ENVIRONMENT
    ticket = "test_ticket_prod_fail_closed"
    try:
        settings.ENVIRONMENT = "production"

        with patch("app.services.auth_service._get_redis_client", return_value=None):
            # Storing ticket without Redis in production MUST raise RuntimeError
            with pytest.raises(RuntimeError) as exc_info:
                store_mfa_ticket(ticket=ticket, user_id="u1", is_enrolment=False)
            assert "REDIS_UNAVAILABLE: MFA exchange ticket operations require an operational Redis cluster" in str(
                exc_info.value
            )

            # Consuming ticket without Redis in production MUST raise RuntimeError
            with pytest.raises(RuntimeError) as exc_info:
                consume_mfa_ticket(ticket)
            assert "REDIS_UNAVAILABLE: MFA exchange ticket operations require an operational Redis cluster" in str(
                exc_info.value
            )

    finally:
        settings.ENVIRONMENT = original_env
