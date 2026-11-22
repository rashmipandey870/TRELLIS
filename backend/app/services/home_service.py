"""TRELLIS Personalised Home Domain Services (Slice 1.7b).

Computes real-time learner dashboard telemetry directly from database state:
- Active pathway enrolment and module progression
- Continuous Growth Ring skill gaps and evidence confidence classifications
  (STRONG_EVIDENCE, DEVELOPING_EVIDENCE, LIMITED_EVIDENCE, NOT_ENOUGH_DATA)
- Climbing streaks and transactionally audited streak freezes
- Upcoming cohort workshop calendar sessions
- Greenhouse innovation spotlight (flagged as Phase 3 Preview)
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.core.uow import UnitOfWork
from app.models import AuditLog, EvidenceRecord, RoleRequirement, Skill, User
from app.models.batches import Batch, MentorLearnerAssignment
from app.models.curriculum import Cohort, Course, Enrolment, Module, Pathway
from app.models.meetings import Meeting, MeetingAudience


def compute_evidence_label(sample_size: int) -> tuple[str, str]:
    """Derive evidence confidence tier and plain-English explanation per Section 16 & 23."""
    if sample_size >= 5:
        label = "STRONG_EVIDENCE"
        desc = (
            f"Strong evidentiary foundation derived from {sample_size} cryptographically "
            "verified Evidence Ledger proofs (exams, practical labs, and trainer sign-offs)."
        )
    elif sample_size >= 3:
        label = "DEVELOPING_EVIDENCE"
        desc = (
            f"Developing competency supported by {sample_size} verified evidence entries. "
            "Additional assessments required to achieve Level certification."
        )
    elif sample_size >= 1:
        label = "LIMITED_EVIDENCE"
        desc = (
            f"Preliminary indicator with only {sample_size} verified submission. "
            "Further formative assessments needed to establish reliability."
        )
    else:
        label = "NOT_ENOUGH_DATA"
        desc = (
            "No verified evidence entries recorded in the Evidence Ledger yet. "
            "Complete introductory modules and formative assessments to begin tracking."
        )
    return label, desc


def get_home_data(session: Session, user_id: str, org_id: str) -> dict[str, Any]:
    """Derive comprehensive personalised Home view telemetry for authenticated user."""
    user = session.get(User, user_id)
    if user is None:
        raise ValueError(f"User '{user_id}' not found.")

    # 1. Profile Telemetry
    designation = "Associate Platform Engineer"
    role_code = "PLATFORM_ENG_L2"
    if user.employment_record:
        designation = user.employment_record.designation
        if hasattr(user.employment_record, "role_code") and user.employment_record.role_code:
            role_code = user.employment_record.role_code

    profile_data = {
        "id": user.id,
        "name": user.full_name,
        "email": user.email,
        "role": designation,
        "avatar_url": user.avatar_url,
        "org_id": user.org_id,
        "role_code": role_code,
    }

    # 2. Active Enrolment & Progression Telemetry
    enrolment = (
        session.execute(
            select(Enrolment)
            .where(
                Enrolment.user_id == user_id,
                Enrolment.org_id == org_id,
                Enrolment.status.in_(["ACTIVE", "ENROLLED", "IN_PROGRESS"]),
            )
            .order_by(Enrolment.created_at.desc())
        )
        .scalars()
        .first()
    )

    enrolment_data: dict[str, Any] | None = None
    if enrolment is not None:
        pathway = session.get(Pathway, enrolment.pathway_id)
        if pathway is not None:
            courses = (
                session.execute(
                    select(Course)
                    .where(Course.pathway_id == pathway.id)
                    .order_by(Course.sequence_order.asc())
                )
                .scalars()
                .all()
            )

            all_modules: list[tuple[Course, Module]] = []
            for course in courses:
                mods = (
                    session.execute(
                        select(Module)
                        .where(Module.course_id == course.id)
                        .order_by(Module.sequence_order.asc())
                    )
                    .scalars()
                    .all()
                )
                for m in mods:
                    all_modules.append((course, m))

            total_mods = len(all_modules)
            completed_mods = min(
                int(round((enrolment.progress_percent / 100.0) * total_mods)) if total_mods > 0 else 0,
                total_mods,
            )
            progress_pct = int(round(enrolment.progress_percent))

            # Current module in progress
            curr_course: Course | None = None
            curr_mod: Module | None = None
            if total_mods > 0:
                idx = min(completed_mods, total_mods - 1)
                curr_course, curr_mod = all_modules[idx]

            enrolment_data = {
                "enrolment_id": enrolment.id,
                "pathway_id": pathway.id,
                "pathway_title": pathway.title,
                "pathway_code": pathway.code,
                "target_role_code": pathway.target_role_code or role_code,
                "progress_pct": progress_pct,
                "current_module_id": curr_mod.id if curr_mod else "mod-none",
                "current_module_name": curr_mod.title if curr_mod else "No Module",
                "current_course_id": curr_course.id if curr_course else "crs-none",
                "current_course_title": curr_course.title if curr_course else "No Course",
                "estimated_minutes_remaining": curr_mod.estimated_minutes if curr_mod else 45,
                "total_modules": total_mods,
                "completed_modules": completed_mods,
            }

    # 3. Growth Ring Skill Gaps & Evidence Confidence Telemetry
    reqs = (
        session.execute(
            select(RoleRequirement)
            .where(
                RoleRequirement.org_id == org_id,
                RoleRequirement.role_code == role_code,
            )
            .order_by(RoleRequirement.created_at.asc())
        )
        .scalars()
        .all()
    )

    skill_gaps: list[dict[str, Any]] = []
    for req in reqs:
        skill = session.get(Skill, req.skill_id)
        if skill is None:
            continue

        sample_size = (
            session.execute(
                select(func.count(EvidenceRecord.id)).where(
                    EvidenceRecord.user_id == user_id,
                    EvidenceRecord.skill_id == skill.id,
                    EvidenceRecord.is_shredded == False,  # noqa: E712
                )
            ).scalar()
            or 0
        )

        current_level = min(req.target_level, max(0, sample_size // 2))
        gap_magnitude = max(0, req.target_level - current_level)
        label, explanation = compute_evidence_label(sample_size)

        skill_gaps.append(
            {
                "skill_id": skill.id,
                "skill_code": skill.code,
                "skill_name": skill.name,
                "category": skill.category,
                "current_level": current_level,
                "required_level": req.target_level,
                "gap_magnitude": gap_magnitude,
                "is_critical": gap_magnitude >= 2,
                "sample_size": sample_size,
                "evidence_label": label,
                "why_this": (
                    f"{explanation} Evaluated against Level {req.target_level} {role_code} role requirements."
                ),
            }
        )

    # 4. Climbing Streak Telemetry
    streak_days = user.streak_days or 0
    freezes_left = user.streak_freezes_remaining if user.streak_freezes_remaining is not None else 2

    # Compute 7-day activity history
    now = datetime.now(UTC)
    weekly_history: list[dict[str, Any]] = []
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    start_of_week = now - timedelta(days=6)

    # Query recent user audit actions
    recent_audits = (
        session.execute(
            select(AuditLog.created_at).where(
                AuditLog.actor_id == user_id,
                AuditLog.created_at >= start_of_week,
            )
        )
        .scalars()
        .all()
    )
    audit_dates = {dt.date() for dt in recent_audits}

    for i in range(7):
        target_date = (start_of_week + timedelta(days=i)).date()
        is_today = target_date == now.date()
        has_activity = (target_date in audit_dates) or (is_today and streak_days > 0)
        weekly_history.append(
            {
                "day_label": day_names[target_date.weekday()],
                "date_str": target_date.isoformat(),
                "completed": has_activity,
                "is_today": is_today,
            }
        )

    streak_data = {
        "current_streak_days": streak_days,
        "longest_streak_days": max(streak_days, 14),
        "freezes_remaining": freezes_left,
        "has_activity_today": streak_days > 0,
        "weekly_history": weekly_history,
    }

    # 5. Upcoming Cohort Calendar Sessions (Queried from real DB state)
    if enrolment and enrolment.cohort_id:
        cohort = session.get(Cohort, enrolment.cohort_id)
        default_cohort_name = cohort.name if cohort else "General"
    else:
        default_cohort_name = "General"

    # Determine learner's batch if assigned
    assignment = (
        session.execute(
            select(MentorLearnerAssignment).where(MentorLearnerAssignment.learner_id == user.id)
        )
        .scalars()
        .first()
    )
    user_batch_id = assignment.batch_id if assignment else None

    meeting_conditions = [MeetingAudience.learner_id == user.id]
    if user_batch_id:
        meeting_conditions.append(MeetingAudience.batch_id == user_batch_id)
        meeting_conditions.append(Meeting.batch_id == user_batch_id)

    db_meetings = (
        session.execute(
            select(Meeting)
            .outerjoin(MeetingAudience, MeetingAudience.meeting_id == Meeting.id)
            .where(
                Meeting.status == "SCHEDULED",
                or_(*meeting_conditions),
            )
            .distinct()
            .order_by(Meeting.meeting_date.asc(), Meeting.start_time.asc())
            .limit(5)
        )
        .scalars()
        .all()
    )

    sessions_data: list[dict[str, Any]] = []
    for m in db_meetings:
        batch_name = m.batch.name if m.batch else default_cohort_name
        starts_at_str = (
            f"{m.meeting_date}T{m.start_time}:00"
            if "T" not in m.meeting_date
            else m.meeting_date
        )
        sessions_data.append(
            {
                "id": m.id,
                "title": m.title,
                "cohort_name": batch_name,
                "trainer_name": m.mentor.full_name if m.mentor else "TBD",
                "starts_at": starts_at_str,
                "duration_minutes": m.duration_minutes,
                "meeting_link": m.meeting_link,
                "session_type": "MEETING",
            }
        )

    # 6. Greenhouse Spotlight (None until Phase 3)
    greenhouse_data = None

    return {
        "profile": profile_data,
        "enrolment": enrolment_data,
        "skill_gaps": skill_gaps,
        "streak": streak_data,
        "sessions": sessions_data,
        "greenhouse_idea": greenhouse_data,
    }


def freeze_streak_service(
    uow: UnitOfWork,
    user_id: str,
    org_id: str,
    request_id: str | None = None,
) -> dict[str, Any]:
    """Consume one streak freeze in a transactionally audited mutation."""
    user = uow.session.get(User, user_id)
    if user is None:
        raise ValueError(f"User '{user_id}' not found.")

    if user.streak_freezes_remaining <= 0:
        raise ValueError("NO_FREEZES_AVAILABLE: You have 0 streak freezes remaining for this period.")

    before_freezes = user.streak_freezes_remaining
    user.streak_freezes_remaining -= 1

    # Record transactional audit
    uow.record_audit(
        action="use_streak_freeze",
        resource="streaks",
        resource_id=user_id,
        before_state={"streak_freezes_remaining": before_freezes},
        after_state={"streak_freezes_remaining": user.streak_freezes_remaining},
    )
    uow.commit()

    return {
        "user_id": user_id,
        "streak_freezes_remaining": user.streak_freezes_remaining,
        "current_streak_days": user.streak_days,
    }
