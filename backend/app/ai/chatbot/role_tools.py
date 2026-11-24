"""Role-Scoped Grounded Fact Tools for TRELLIS AI Chatbot (Phase B).

Enforces server-side authorization:
- Tools strictly enforce current_user role and scope.
- Facts come entirely from real DB queries, never hallucinated or hard-coded.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.assessments import Answer, AssessmentAttempt
from app.models.audit import AuditLog
from app.models.batches import Batch, MentorLearnerAssignment
from app.models.curriculum import Enrolment
from app.models.meetings import Meeting, MeetingAudience
from app.models.practice import TalentAlert
from app.models.user import User

logger = logging.getLogger(__name__)


def get_learner_context(db: Session, user: User) -> dict[str, Any]:
    """Extract authoritative learner progress and schedule facts."""
    enrolment = (
        db.execute(
            select(Enrolment)
            .where(Enrolment.user_id == user.id)
            .order_by(Enrolment.created_at.desc())
        )
        .scalars()
        .first()
    )

    pathway_title = enrolment.pathway.title if (enrolment and enrolment.pathway) else "Core Engineering"
    progress = round(float(enrolment.progress_percent), 1) if enrolment else 0.0

    recent_attempts = (
        db.execute(
            select(AssessmentAttempt)
            .where(AssessmentAttempt.learner_id == user.id, AssessmentAttempt.status == "SUBMITTED")
            .order_by(AssessmentAttempt.submit_time.desc())
            .limit(3)
        )
        .scalars()
        .all()
    )

    attempts_summary = [
        {
            "assessment": a.assessment.title if a.assessment else "Assessment",
            "score": round(float(a.score), 1),
            "total_marks": round(float(a.total_marks), 1),
            "passed": bool(a.passed),
        }
        for a in recent_attempts
    ]

    now = datetime.now(UTC)
    now_date = now.strftime("%Y-%m-%d")
    meetings = (
        db.execute(
            select(Meeting)
            .join(MeetingAudience, MeetingAudience.meeting_id == Meeting.id)
            .where(
                MeetingAudience.learner_id == user.id,
                Meeting.status == "SCHEDULED",
                Meeting.meeting_date >= now_date,
            )
            .order_by(Meeting.meeting_date.asc(), Meeting.start_time.asc())
            .limit(3)
        )
        .scalars()
        .all()
    )

    upcoming_meetings = [
        {
            "title": m.title,
            "start_time": f"{m.meeting_date} {m.start_time}",
            "meeting_link": m.meeting_link,
        }
        for m in meetings
    ]

    return {
        "role": "LEARNER",
        "user_name": user.full_name,
        "pathway": pathway_title,
        "progress_percent": progress,
        "streak_days": user.streak_days,
        "recent_attempts": attempts_summary,
        "upcoming_meetings": upcoming_meetings,
    }


def get_mentor_context(db: Session, user: User) -> dict[str, Any]:
    """Extract authoritative mentor cohort and action queue facts."""
    # Batches assigned to mentor via MentorLearnerAssignment
    from app.models.batches import MentorLearnerAssignment
    assigned_bids = db.execute(
        select(MentorLearnerAssignment.batch_id).where(MentorLearnerAssignment.mentor_id == user.id)
    ).scalars().all()
    clean_bids = list(set([b for b in assigned_bids if b]))
    batches = db.execute(select(Batch).where(Batch.id.in_(clean_bids))).scalars().all() if clean_bids else []
    batch_names = [b.name for b in batches]

    # Learners count in mentor's assignments
    learners_count = db.scalar(
        select(func.count(MentorLearnerAssignment.learner_id.distinct())).where(MentorLearnerAssignment.mentor_id == user.id)
    ) or 0

    # Pending manual review attempts
    pending_grading_count = (
        db.scalar(
            select(func.count(AssessmentAttempt.id))
            .where(
                AssessmentAttempt.status == "SUBMITTED",
                AssessmentAttempt.grading_status == "PENDING_REVIEW",
            )
        )
        or 0
    )

    # Active talent alerts
    active_alerts_count = (
        db.scalar(
            select(func.count(TalentAlert.id))
            .where(TalentAlert.status == "ACTIVE")
        )
        or 0
    )

    # Upcoming mentor meetings
    now = datetime.now(UTC)
    now_date = now.strftime("%Y-%m-%d")
    meetings = (
        db.execute(
            select(Meeting)
            .where(
                Meeting.mentor_id == user.id,
                Meeting.status == "SCHEDULED",
                Meeting.meeting_date >= now_date,
            )
            .order_by(Meeting.meeting_date.asc(), Meeting.start_time.asc())
            .limit(3)
        )
        .scalars()
        .all()
    )

    upcoming_meetings = [
        {
            "title": m.title,
            "start_time": f"{m.meeting_date} {m.start_time}",
            "meeting_link": m.meeting_link,
        }
        for m in meetings
    ]

    return {
        "role": "MENTOR",
        "user_name": user.full_name,
        "batches": batch_names,
        "assigned_learners_count": learners_count,
        "pending_grading_count": pending_grading_count,
        "active_talent_alerts_count": active_alerts_count,
        "upcoming_meetings": upcoming_meetings,
    }


def get_admin_context(db: Session, user: User) -> dict[str, Any]:
    """Extract authoritative enterprise admin operational facts."""
    total_users = db.scalar(select(func.count(User.id))) or 0
    total_batches = db.scalar(select(func.count(Batch.id))) or 0
    total_attempts = db.scalar(select(func.count(AssessmentAttempt.id))) or 0
    total_alerts = db.scalar(select(func.count(TalentAlert.id))) or 0

    since_24h = datetime.now(UTC) - timedelta(hours=24)
    audit_events_24h = (
        db.scalar(
            select(func.count(AuditLog.id)).where(AuditLog.created_at >= since_24h)
        )
        or 0
    )

    return {
        "role": "ADMIN",
        "user_name": user.full_name,
        "total_users": total_users,
        "total_batches": total_batches,
        "total_attempts": total_attempts,
        "active_talent_alerts": total_alerts,
        "audit_events_24h": audit_events_24h,
    }
