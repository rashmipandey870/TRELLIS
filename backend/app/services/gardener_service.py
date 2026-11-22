"""TRELLIS Gardener AI Learning Coach Service.

Provides personalized, role-aware, privacy-preserving AI mentorship:
- Injects learner's own learning context (enrolment, streak, gaps, recent scores).
- Grounded strictly in CSM Technologies curriculum and development pathways.
- Enforces per-user rate limiting (30 messages per hour).
"""

from __future__ import annotations

import logging
import time
from collections import defaultdict
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.assessments import AssessmentAttempt
from app.models.curriculum import Enrolment
from app.models.user import User
from app.ai.gateway import ai_gateway

logger = logging.getLogger(__name__)

# Sliding window in-memory rate limiter: user_id -> list of timestamps
_RATE_LIMIT_WINDOW_SEC = 3600  # 1 hour
_MAX_REQUESTS_PER_WINDOW = 30
_user_chat_timestamps: dict[str, list[float]] = defaultdict(list)


def check_and_record_rate_limit(user_id: str) -> tuple[bool, int]:
    """Check if user has exceeded the 30 requests/hour rate limit.
    
    Returns (is_allowed, remaining_requests).
    """
    now = time.time()
    cutoff = now - _RATE_LIMIT_WINDOW_SEC
    # Filter out timestamps older than 1 hour
    recent = [t for t in _user_chat_timestamps[user_id] if t > cutoff]
    _user_chat_timestamps[user_id] = recent

    if len(recent) >= _MAX_REQUESTS_PER_WINDOW:
        return False, 0

    recent.append(now)
    return True, _MAX_REQUESTS_PER_WINDOW - len(recent)


def chat_with_gardener(
    learner_id: str,
    user_message: str,
    db: Session,
    history: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Process a learner query with the Gardener AI coach using grounded context."""
    learner = db.get(User, learner_id)
    if not learner:
        raise ValueError(f"Learner '{learner_id}' not found.")

    allowed, remaining = check_and_record_rate_limit(learner_id)
    if not allowed:
        return {
            "error": "RATE_LIMIT_EXCEEDED",
            "message": "You have reached the limit of 30 Gardener queries per hour. Please take a break and try again later.",
            "remaining_queries": 0,
        }

    chat_resp = ai_gateway.chat_with_gardener(
        learner_id=learner_id,
        user_message=user_message,
        db=db,
        history=history,
    )
    return {
        "reply": chat_resp.reply,
        "remaining_queries": remaining,
        "suggested_actions": chat_resp.suggested_actions,
        "context_used": chat_resp.context_used,
        "provenance": chat_resp.provenance.model_dump(),
    }
