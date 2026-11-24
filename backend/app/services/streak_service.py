"""TRELLIS Runtime Activity & Streak Derivation Engine.

Computes active days, continuous streaks, and dedication score dynamically
from raw event history (PracticeAttempt, AssessmentAttempt, Submission).
"""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.assessments import AssessmentAttempt, Submission
from app.models.practice import PracticeAttempt


def derive_learner_streak_and_activity(
    learner_id: str,
    db: Session,
    reference_date: datetime | None = None,
) -> dict[str, Any]:
    """Compute true streak, active days, and dedication score from raw event history."""
    ref_dt = reference_date or datetime.now(UTC)
    ref_date = ref_dt.date()

    # Query distinct activity dates from practice attempts
    p_dates = (
        db.execute(
            select(func.date(PracticeAttempt.created_at))
            .where(PracticeAttempt.learner_id == learner_id)
            .distinct()
        )
        .scalars()
        .all()
    )

    # Query distinct activity dates from assessment attempts
    a_dates = (
        db.execute(
            select(func.date(AssessmentAttempt.submit_time))
            .where(
                AssessmentAttempt.learner_id == learner_id,
                AssessmentAttempt.status == "SUBMITTED",
                AssessmentAttempt.submit_time.is_not(None),
            )
            .distinct()
        )
        .scalars()
        .all()
    )

    # Query distinct activity dates from code submissions
    s_dates = (
        db.execute(
            select(func.date(Submission.created_at))
            .where(Submission.learner_id == learner_id)
            .distinct()
        )
        .scalars()
        .all()
    )

    # Merge and parse into set of date objects
    raw_date_strings = set(filter(None, list(p_dates) + list(a_dates) + list(s_dates)))
    activity_dates: set[date] = set()
    for d_str in raw_date_strings:
        if isinstance(d_str, date) and not isinstance(d_str, datetime):
            activity_dates.add(d_str)
        elif isinstance(d_str, datetime):
            activity_dates.add(d_str.date())
        elif isinstance(d_str, str):
            try:
                activity_dates.add(datetime.strptime(d_str[:10], "%Y-%m-%d").date())
            except ValueError:
                pass

    active_days_count = len(activity_dates)

    # Calculate consecutive streak
    streak = 0
    curr = ref_date
    if curr in activity_dates:
        while curr in activity_dates:
            streak += 1
            curr -= timedelta(days=1)
    elif (curr - timedelta(days=1)) in activity_dates:
        curr -= timedelta(days=1)
        while curr in activity_dates:
            streak += 1
            curr -= timedelta(days=1)

    dedication_score = round(min(100.0, float(active_days_count * 1.8 + streak * 2.2)), 1)

    return {
        "streak_days": streak,
        "active_days": active_days_count,
        "dedication_score": dedication_score,
        "activity_dates_count": active_days_count,
    }
