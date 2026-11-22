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
from app.services.ai_question_generator import call_llm_text

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

    # Gather learner's active context
    enrolment = (
        db.execute(
            select(Enrolment)
            .where(Enrolment.user_id == learner_id, Enrolment.status == "IN_PROGRESS")
        )
        .scalars()
        .first()
    )
    current_pathway = enrolment.pathway.title if enrolment and enrolment.pathway else "General Technology Onboarding"
    progress = round(float(enrolment.progress_percent), 1) if enrolment else 0.0

    recent_attempts = (
        db.execute(
            select(AssessmentAttempt)
            .where(AssessmentAttempt.learner_id == learner_id, AssessmentAttempt.status == "SUBMITTED")
            .order_by(AssessmentAttempt.submit_time.desc())
            .limit(3)
        )
        .scalars()
        .all()
    )
    recent_perf = [
        f"{a.assessment.title if a.assessment else 'Assessment'}: {a.score:.1f}/{a.total_marks:.1f} ({'PASSED' if a.passed else 'RETRY'})"
        for a in recent_attempts
    ]

    history_str = ""
    if history:
        for turn in history[-4:]:
            role = turn.get("role", "user")
            content = turn.get("content", "")
            history_str += f"{role.capitalize()}: {content}\n"

    system_prompt = (
        "You are 'The Gardener', the empathetic, expert AI Learning Coach on TRELLIS, "
        "the CSM Technologies Learning Platform.\n"
        f"Learner Name: {learner.full_name}\n"
        f"Current Pathway: {current_pathway} (Progress: {progress}%)\n"
        f"Climbing Streak: {learner.streak_days} days\n"
        f"Recent Performance: {', '.join(recent_perf) if recent_perf else 'No completed assessments yet'}\n\n"
        "Guidelines:\n"
        "1. Be encouraging, precise, and practical. Offer concrete code or architectural advice when asked.\n"
        "2. Ground your explanations in industry best practices and CSM Technologies platform standards.\n"
        "3. Protect privacy: never reference or compare against other specific students by name.\n"
        "4. Keep responses concise (2 to 4 paragraphs max) with clear next action steps."
    )

    full_prompt = (
        f"{system_prompt}\n\n"
        f"Conversation History:\n{history_str}\n"
        f"Learner Question: {user_message}\n\n"
        "The Gardener:"
    )

    ai_reply = call_llm_text(full_prompt, timeout=25)
    if not ai_reply:
        ai_reply = (
            f"Hello {learner.full_name}! I'm your learning companion here in {current_pathway}. "
            f"You're currently at {progress}% progress with a {learner.streak_days}-day climbing streak. "
            f"Regarding your query: '{user_message}' — continue practicing core concepts in your practice lab, "
            f"and feel free to test code directly in the code editor. How can I help clarify further?"
        )

    suggested_actions = [
        f"Practice {current_pathway.split(':')[0]} problems",
        "Review latest Growth Ring report",
        "Check scheduled mentor sessions",
    ]

    return {
        "reply": ai_reply,
        "remaining_queries": remaining,
        "suggested_actions": suggested_actions,
        "context_used": {
            "pathway": current_pathway,
            "progress_percent": progress,
            "streak_days": learner.streak_days,
        },
    }
