"""TRELLIS Mentor API Router (Step 3).

Endpoints strictly guarded by require_mentor:
- Mentor Dashboard: assigned learners, upcoming meetings, live assessments, practice alerts
- Meeting Management: conflict-checked scheduling, editing, canceling, attendance marking
- Assessment Builder: multi-format tests (MCQ + Coding), versioning on publish/submit, question bank, result analysis with CSV export
- Learner Review: assigned learner review and qualitative feedback/remarks
- Talent Spotlight: act on AI practice alerts (Invite, Interview, Recommend Promotion, Dismiss)
"""

from __future__ import annotations

import csv
import io
import logging
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, HttpUrl, model_validator
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session, joinedload, load_only, selectinload

from app.api.deps import get_db, get_uow, require_mentor, require_role, verify_mentor_learner_access
from app.core.config import settings
from app.models.audit import AuditLog
from app.models.assessments import (
    Answer,
    Assessment,
    AssessmentAttempt,
    AssessmentAudience,
    AssessmentNote,
    AssessmentQuestion,
    CodingProblem,
    McqOption,
    QuestionBank,
    Submission,
    TestCase,
)
from app.models.batches import Batch, MentorLearnerAssignment
from app.models.meetings import Meeting, MeetingAttendance, MeetingAudience
from app.models.notifications import Notification
from app.models.practice import AlertAction, PracticeScore, TalentAlert
from app.models.reviews import MentorRemark
from app.models.user import User
from app.schemas.category import AssessmentCategory
from app.schemas.notes import AssessmentNoteCreate, AssessmentNoteUpdate
from app.services.email_service import dispatch_email_notification

router = APIRouter(prefix="/mentor", tags=["Mentor Portal"])


# --- Schemas ---
class MeetingCreateRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    description: str | None = None
    meeting_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD
    start_time: str = Field(..., pattern=r"^\d{2}:\d{2}$")  # HH:MM
    end_time: str = Field(..., pattern=r"^\d{2}:\d{2}$")  # HH:MM
    duration_minutes: int = 60
    meeting_link: str = Field(..., min_length=10)  # Teams / Meet / Zoom
    batch_id: str | None = None
    learner_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def normalize_datetimes(cls, data: Any) -> Any:
        if isinstance(data, dict):
            start = data.get("start_time", "")
            end = data.get("end_time", "")
            if "T" in str(start):
                parts = str(start).split("T")
                if not data.get("meeting_date"):
                    data["meeting_date"] = parts[0]
                data["start_time"] = parts[1][:5]
            if "T" in str(end):
                parts = str(end).split("T")
                data["end_time"] = parts[1][:5]
            if not data.get("meeting_date"):
                data["meeting_date"] = datetime.now(UTC).strftime("%Y-%m-%d")
        return data


class AttendanceItem(BaseModel):
    learner_id: str
    attended: bool
    remarks: str | None = None


class MarkAttendanceRequest(BaseModel):
    attendances: list[AttendanceItem]


class AssessmentCreateRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    field: str = "General"
    instructions: str | None = None
    duration_minutes: int = 60
    passing_score: float = 60.0
    start_window: datetime | None = None
    end_window: datetime | None = None
    batch_id: str | None = None
    learner_ids: list[str] = Field(default_factory=list)
    show_explanations: bool = True
    mask_hidden_cases: bool = True


def validate_mentor_targets(
    db: Session,
    mentor: User,
    batch_id: str | None,
    learner_ids: list[str] | None,
) -> None:
    """Validate that batch_id and learner_ids belong to the mentor's own assignments."""
    if (mentor.role or "").upper() == "ADMIN":
        return

    assigned_batches = set(
        db.execute(
            select(MentorLearnerAssignment.batch_id).where(
                MentorLearnerAssignment.mentor_id == mentor.id,
                MentorLearnerAssignment.batch_id.is_not(None),
            )
        ).scalars().all()
    )
    assigned_learners = set(
        db.execute(
            select(MentorLearnerAssignment.learner_id).where(
                MentorLearnerAssignment.mentor_id == mentor.id
            )
        ).scalars().all()
    )

    if batch_id and assigned_batches and batch_id not in assigned_batches:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied: Mentor is not assigned to batch '{batch_id}'.",
        )

    if learner_ids:
        for lid in learner_ids:
            if assigned_learners and lid not in assigned_learners:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied: Learner '{lid}' is not assigned to this mentor.",
                )


def validate_meeting_url(url: str, allowed_hosts: list[str]) -> None:
    """Validate that meeting link uses https and its host matches the configured allow-list."""
    if not url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Meeting link is required.",
        )
    parsed = urlparse(url)
    if (parsed.scheme or "").lower() != "https":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid meeting URL: Only https:// scheme is allowed (javascript:, data:, and http: are strictly rejected).",
        )
    hostname = (parsed.hostname or "").lower()
    if not hostname:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid meeting URL: Hostname is missing.",
        )

    def is_allowed(host: str, rule: str) -> bool:
        clean_rule = rule.lower().lstrip("*.")
        return host == clean_rule or host.endswith("." + clean_rule)

    if not any(is_allowed(hostname, rule) for rule in allowed_hosts):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Meeting host '{hostname}' is not in allowed domains: {allowed_hosts}.",
        )


def validate_meeting_schedule_and_conflicts(
    db: Session,
    mentor_id: str,
    meeting_date: str,
    start_time: str,
    end_time: str,
    batch_id: str | None,
    learner_ids: list[str],
    exclude_meeting_id: str | None = None,
) -> None:
    """Validate date not in the past, end_time > start_time, and overlapping conflicts for mentor and audience."""
    # 1. Date not in past
    try:
        m_date = datetime.strptime(meeting_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format. Expected YYYY-MM-DD.")

    now_utc = datetime.now(UTC)
    if m_date < now_utc.date():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Meeting date cannot be in the past.")

    # 2. end_time > start_time
    try:
        s_time = datetime.strptime(start_time, "%H:%M").time()
        e_time = datetime.strptime(end_time, "%H:%M").time()
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid time format. Expected HH:MM.")

    if e_time <= s_time:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Meeting end_time must be strictly after start_time.")

    # 3. Conflict detection for SAME mentor (overlapping time range)
    query_mentor = select(Meeting).where(
        Meeting.mentor_id == mentor_id,
        Meeting.meeting_date == meeting_date,
        Meeting.status == "SCHEDULED",
        Meeting.start_time < end_time,
        Meeting.end_time > start_time,
    )
    if exclude_meeting_id:
        query_mentor = query_mentor.where(Meeting.id != exclude_meeting_id)

    mentor_conflict = db.execute(query_mentor).scalars().first()
    if mentor_conflict:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Scheduling conflict: Mentor already has meeting '{mentor_conflict.title}' scheduled on {meeting_date} ({mentor_conflict.start_time} - {mentor_conflict.end_time}).",
        )

    # 4. Conflict detection for ANY learner in audience
    audience_learners = set(learner_ids or [])
    if batch_id:
        batch_lids = db.execute(
            select(MentorLearnerAssignment.learner_id).where(MentorLearnerAssignment.batch_id == batch_id)
        ).scalars().all()
        audience_learners.update(batch_lids)

    if audience_learners:
        overlapping_query = select(Meeting).where(
            Meeting.meeting_date == meeting_date,
            Meeting.status == "SCHEDULED",
            Meeting.start_time < end_time,
            Meeting.end_time > start_time,
        )
        if exclude_meeting_id:
            overlapping_query = overlapping_query.where(Meeting.id != exclude_meeting_id)

        overlapping_meetings = db.execute(overlapping_query).scalars().all()
        for om in overlapping_meetings:
            om_learners = set()
            om_aud = db.execute(select(MeetingAudience).where(MeetingAudience.meeting_id == om.id)).scalars().all()
            for aud in om_aud:
                if aud.learner_id:
                    om_learners.add(aud.learner_id)
                elif aud.batch_id:
                    om_b_lids = db.execute(
                        select(MentorLearnerAssignment.learner_id).where(MentorLearnerAssignment.batch_id == aud.batch_id)
                    ).scalars().all()
                    om_learners.update(om_b_lids)

            conflict_lids = audience_learners.intersection(om_learners)
            if conflict_lids:
                cl_name = sorted(conflict_lids)[0]
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Scheduling conflict: Learner '{cl_name}' is already scheduled in meeting '{om.title}' on {meeting_date} ({om.start_time} - {om.end_time}).",
                )


class McqQuestionCreateRequest(BaseModel):
    title: str
    question_text: str
    category: AssessmentCategory = Field(default=AssessmentCategory.TECHNICAL_KNOWLEDGE)
    field: str
    topic: str
    difficulty: str = "MEDIUM"
    tags: list[str] = Field(default_factory=list)
    explanation: str | None = None
    options: list[dict[str, Any]]  # [{"text": "...", "is_correct": bool, "explanation": "..."}]


class CodingProblemCreateRequest(BaseModel):
    title: str
    description: str
    category: AssessmentCategory = Field(default=AssessmentCategory.CODING)
    constraints: str | None = None
    field: str
    difficulty: str = "MEDIUM"
    marks: float = 10.0
    time_limit_ms: int = 3000
    memory_limit_mb: int = 256
    starter_code: dict[str, str] = Field(default_factory=dict)
    reference_solution: str | None = None
    test_cases: list[dict[str, Any]] = Field(default_factory=list)
    rubric: dict[str, Any] | None = None
    schema_ddl: str | None = None


class AnswerGradeItem(BaseModel):
    answer_id: str
    score_awarded: float
    feedback: str | None = None
    override_reason: str | None = None


class GradeAttemptRequest(BaseModel):
    grades: list[AnswerGradeItem]


class RemarkCreateRequest(BaseModel):
    remark_text: str = Field(..., min_length=2)
    assessment_id: str | None = None
    meeting_id: str | None = None
    visibility: str = "LEARNER_AND_ADMIN"


class AlertActionRequest(BaseModel):
    action: str = Field(..., pattern="^(INVITE_ASSESSMENT|SCHEDULE_INTERVIEW|RECOMMEND_PROMOTION|DISMISSED|DISMISS)$")
    notes: str | None = None
    assessment_id: str | None = None
    meeting_date: str | None = None
    start_time: str | None = None
    end_time: str | None = None
    meeting_link: str | None = None


class AttachQuestionRequest(BaseModel):
    question_id: str | None = None
    bank_question_id: str | None = None
    marks: float = 5.0
    order: int | None = None
    sequence_order: int | None = None


class QuestionReorderItem(BaseModel):
    question_id: str | None = None
    bank_question_id: str | None = None
    aq_id: str | None = None
    id: str | None = None
    marks: float = 5.0
    order: int = 1
    sequence_order: int | None = None


class ReorderQuestionsRequest(BaseModel):
    questions: list[QuestionReorderItem] = Field(default_factory=list)


class UnifiedQuestionCreateRequest(BaseModel):
    title: str
    question_text: str | None = None
    description: str | None = None
    type: str = "MCQ"
    question_type: str | None = None
    category: AssessmentCategory = Field(default=AssessmentCategory.TECHNICAL_KNOWLEDGE)
    field: str = "Python"
    topic: str = "General"
    difficulty: str = "MEDIUM"
    marks: float = 10.0
    tags: list[str] = Field(default_factory=list)
    explanation: str | None = None
    options: list[dict[str, Any]] = Field(default_factory=list)
    constraints: str | None = None
    starter_code: dict[str, str] = Field(default_factory=dict)
    reference_solution: str | None = None
    test_cases: list[dict[str, Any]] = Field(default_factory=list)
    time_limit_ms: int = 3000
    memory_limit_mb: int = 256
    rubric: dict[str, Any] | None = None
    schema_ddl: str | None = None


class AnswerGradeItem(BaseModel):
    answer_id: str
    score_awarded: float
    feedback: str | None = None
    override_reason: str | None = None


class GradeAttemptRequest(BaseModel):
    grades: list[AnswerGradeItem]


# --- Mentor Dashboard ---
@router.get("/dashboard", summary="Mentor Overview Dashboard")
def get_mentor_dashboard(
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
) -> dict[str, Any]:
    from app.core.cache import fast_cache
    cache_key = f"mentor:dashboard:{mentor.id}"
    cached = fast_cache.get(cache_key)
    if cached is not None:
        return cached

    # Query assigned learners count via SQL aggregation
    assigned_learners_count = (
        db.execute(
            select(func.count(MentorLearnerAssignment.learner_id.distinct()))
            .where(MentorLearnerAssignment.mentor_id == mentor.id)
        ).scalar()
        or 0
    )

    # Upcoming meetings
    upcoming_meetings = (
        db.execute(
            select(Meeting)
            .where(Meeting.mentor_id == mentor.id, Meeting.status == "SCHEDULED")
            .order_by(Meeting.meeting_date.asc(), Meeting.start_time.asc())
            .limit(5)
        )
        .scalars()
        .all()
    )

    # Assessments created by this mentor
    assessments = (
        db.execute(
            select(Assessment)
            .where(Assessment.mentor_id == mentor.id)
            .order_by(Assessment.created_at.desc())
            .limit(5)
        )
        .scalars()
        .all()
    )

    # Practice alerts
    pending_alerts_rows = (
        db.execute(
            select(
                TalentAlert.id,
                TalentAlert.field,
                TalentAlert.evidence_json,
                User.full_name.label("learner_name"),
            )
            .outerjoin(User, User.id == TalentAlert.learner_id)
            .where(TalentAlert.mentor_id == mentor.id, TalentAlert.status == "PENDING")
            .order_by(TalentAlert.created_at.desc())
        )
        .all()
    )

    result = {
        "assigned_learners_count": assigned_learners_count,
        "upcoming_meetings": [
            {
                "id": m.id,
                "title": m.title,
                "date": m.meeting_date,
                "start_time": m.start_time,
                "duration_minutes": m.duration_minutes,
                "meeting_link": m.meeting_link,
            }
            for m in upcoming_meetings
        ],
        "assessments": [
            {
                "id": a.id,
                "title": a.title,
                "field": a.field,
                "status": a.status,
                "version": a.version,
            }
            for a in assessments
        ],
        "talent_alerts_count": len(pending_alerts_rows),
        "talent_alerts": [
            {
                "id": r.id,
                "learner_name": r.learner_name or "Learner",
                "field": r.field,
                "evidence": r.evidence_json,
            }
            for r in pending_alerts_rows
        ],
    }
    fast_cache.set(cache_key, result, ttl_seconds=20.0)
    return result


# --- Meeting Scheduling & Attendance ---
@router.get("/meetings", summary="List meetings created by mentor")
def list_mentor_meetings(
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
) -> list[dict[str, Any]]:
    meetings = (
        db.execute(select(Meeting).where(Meeting.mentor_id == mentor.id).order_by(Meeting.meeting_date.desc()))
        .scalars()
        .all()
    )
    return [
        {
            "id": m.id,
            "title": m.title,
            "description": m.description,
            "meeting_date": m.meeting_date,
            "start_time": m.start_time,
            "end_time": m.end_time,
            "duration_minutes": m.duration_minutes,
            "meeting_link": m.meeting_link,
            "status": m.status,
            "batch_name": m.batch.name if m.batch else "Direct Learners",
        }
        for m in meetings
    ]


@router.post("/meetings", status_code=status.HTTP_201_CREATED, summary="Schedule meeting with conflict detection")
def schedule_meeting(
    payload: MeetingCreateRequest,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    validate_mentor_targets(db, mentor, payload.batch_id, payload.learner_ids)
    validate_meeting_url(payload.meeting_link, settings.MEETING_ALLOWLIST_HOSTS)
    validate_meeting_schedule_and_conflicts(
        db=db,
        mentor_id=mentor.id,
        meeting_date=payload.meeting_date,
        start_time=payload.start_time,
        end_time=payload.end_time,
        batch_id=payload.batch_id,
        learner_ids=payload.learner_ids,
    )

    meeting = Meeting(
        title=payload.title,
        description=payload.description,
        meeting_date=payload.meeting_date,
        start_time=payload.start_time,
        end_time=payload.end_time,
        duration_minutes=payload.duration_minutes,
        meeting_link=payload.meeting_link,
        mentor_id=mentor.id,
        batch_id=payload.batch_id,
        status="SCHEDULED",
    )
    db.add(meeting)
    db.flush()

    # Create audience entries & notifications
    recipients = set(payload.learner_ids)
    if payload.batch_id:
        batch_learners = (
            db.execute(
                select(MentorLearnerAssignment.learner_id).where(
                    MentorLearnerAssignment.batch_id == payload.batch_id
                )
            )
            .scalars()
            .all()
        )
        recipients.update(batch_learners)
        db.add(MeetingAudience(meeting_id=meeting.id, batch_id=payload.batch_id))

    for lid in recipients:
        db.add(MeetingAudience(meeting_id=meeting.id, learner_id=lid))
        notif = Notification(
            recipient_id=lid,
            sender_id=mentor.id,
            title=f"New Meeting: {meeting.title}",
            message=f"Your mentor {mentor.full_name} scheduled '{meeting.title}' for {meeting.meeting_date} at {meeting.start_time}.",
            notification_type="MEETING",
            link="/learner/meetings",
        )
        db.add(notif)
        u = db.get(User, lid)
        if u and u.email:
            try:
                dispatch_email_notification(
                    to_email=u.email,
                    subject=f"TRELLIS Meeting: {meeting.title}",
                    html_content=f"<p>Hello {u.full_name},</p><p>Your mentor {mentor.full_name} scheduled <strong>{meeting.title}</strong> for {meeting.meeting_date} at {meeting.start_time}.</p><p><a href='{meeting.meeting_link}'>Join Meeting</a></p>",
                    text_content=f"Hello {u.full_name},\nYour mentor {mentor.full_name} scheduled '{meeting.title}' for {meeting.meeting_date} at {meeting.start_time}.\nLink: {meeting.meeting_link}",
                )
            except Exception:
                pass

    db.commit()
    return {"id": meeting.id, "title": meeting.title, "status": meeting.status}


@router.put("/meetings/{meeting_id}", summary="Edit or reschedule meeting")
def edit_meeting(
    meeting_id: str,
    payload: MeetingCreateRequest,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    meeting = db.get(Meeting, meeting_id)
    if not meeting or meeting.mentor_id != mentor.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found.")

    validate_mentor_targets(db, mentor, payload.batch_id, payload.learner_ids)
    validate_meeting_url(payload.meeting_link, settings.MEETING_ALLOWLIST_HOSTS)
    validate_meeting_schedule_and_conflicts(
        db=db,
        mentor_id=mentor.id,
        meeting_date=payload.meeting_date,
        start_time=payload.start_time,
        end_time=payload.end_time,
        batch_id=payload.batch_id,
        learner_ids=payload.learner_ids,
        exclude_meeting_id=meeting.id,
    )

    meeting.title = payload.title
    meeting.description = payload.description
    meeting.meeting_date = payload.meeting_date
    meeting.start_time = payload.start_time
    meeting.end_time = payload.end_time
    meeting.duration_minutes = payload.duration_minutes
    meeting.meeting_link = payload.meeting_link

    # Notify audience of update
    audiences = db.execute(select(MeetingAudience).where(MeetingAudience.meeting_id == meeting.id)).scalars().all()
    for aud in audiences:
        if aud.learner_id:
            notif = Notification(
                recipient_id=aud.learner_id,
                sender_id=mentor.id,
                title=f"Meeting Updated: {meeting.title}",
                message=f"Meeting '{meeting.title}' was rescheduled to {meeting.meeting_date} at {meeting.start_time}.",
                notification_type="MEETING",
                link="/learner/meetings",
            )
            db.add(notif)

    db.commit()
    return {"message": "Meeting rescheduled successfully.", "id": meeting.id}


@router.delete("/meetings/{meeting_id}", summary="Cancel meeting")
def cancel_meeting(
    meeting_id: str,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    meeting = db.get(Meeting, meeting_id)
    if not meeting or meeting.mentor_id != mentor.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found.")

    meeting.status = "CANCELLED"

    audiences = db.execute(select(MeetingAudience).where(MeetingAudience.meeting_id == meeting.id)).scalars().all()
    for aud in audiences:
        if aud.learner_id:
            notif = Notification(
                recipient_id=aud.learner_id,
                sender_id=mentor.id,
                title=f"Meeting Cancelled: {meeting.title}",
                message=f"Meeting '{meeting.title}' scheduled for {meeting.meeting_date} has been cancelled.",
                notification_type="MEETING",
                link="/learner/meetings",
            )
            db.add(notif)
            u = db.get(User, aud.learner_id)
            if u and u.email:
                try:
                    dispatch_email_notification(
                        to_email=u.email,
                        subject=f"TRELLIS Meeting Cancelled: {meeting.title}",
                        html_content=f"<p>Hello {u.full_name},</p><p>Meeting <strong>{meeting.title}</strong> scheduled for {meeting.meeting_date} has been cancelled by {mentor.full_name}.</p>",
                        text_content=f"Hello {u.full_name},\nMeeting '{meeting.title}' scheduled for {meeting.meeting_date} has been cancelled.",
                    )
                except Exception:
                    pass

    db.commit()
    return {"message": "Meeting cancelled."}


@router.post("/meetings/{meeting_id}/attendance", summary="Mark attendance for a meeting")
def mark_attendance(
    meeting_id: str,
    payload: MarkAttendanceRequest,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    meeting = db.get(Meeting, meeting_id)
    if not meeting or meeting.mentor_id != mentor.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found.")

    # Determine all valid learner IDs in the meeting audience
    valid_learners = set()
    audiences = db.execute(select(MeetingAudience).where(MeetingAudience.meeting_id == meeting.id)).scalars().all()
    for aud in audiences:
        if aud.learner_id:
            valid_learners.add(aud.learner_id)
        elif aud.batch_id:
            batch_lids = db.execute(
                select(MentorLearnerAssignment.learner_id).where(MentorLearnerAssignment.batch_id == aud.batch_id)
            ).scalars().all()
            valid_learners.update(batch_lids)

    # Validate that every attendance entry belongs to the audience
    for item in payload.attendances:
        if item.learner_id not in valid_learners:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Attendance error: Learner '{item.learner_id}' is not in the audience for meeting '{meeting.title}'.",
            )

        att = (
            db.execute(
                select(MeetingAttendance).where(
                    MeetingAttendance.meeting_id == meeting.id,
                    MeetingAttendance.learner_id == item.learner_id,
                )
            )
            .scalars()
            .first()
        )
        if not att:
            att = MeetingAttendance(
                meeting_id=meeting.id,
                learner_id=item.learner_id,
                attended=item.attended,
                remarks=item.remarks,
            )
            db.add(att)
        else:
            att.attended = item.attended
            att.remarks = item.remarks

    db.commit()
    return {"message": "Attendance recorded."}


# --- Assessment Builder & Question Bank ---
@router.get("/assessments", summary="List mentor's assessments")
def list_mentor_assessments(
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
) -> list[dict[str, Any]]:
    assessments = (
        db.execute(
            select(Assessment)
            .options(
                joinedload(Assessment.batch),
                selectinload(Assessment.attempts),
                selectinload(Assessment.notes),
                selectinload(Assessment.audience_learners),
                selectinload(Assessment.questions).joinedload(AssessmentQuestion.question),
            )
            .where(Assessment.mentor_id == mentor.id)
            .order_by(Assessment.created_at.desc())
        )
        .scalars()
        .all()
    )
    return [
        {
            "id": a.id,
            "title": a.title,
            "field": a.field,
            "instructions": a.instructions,
            "duration_minutes": a.duration_minutes,
            "passing_score": a.passing_score,
            "status": a.status,
            "is_published": a.status == "PUBLISHED",
            "version": a.version,
            "notes_count": len(a.notes),
            "questions_count": len(a.questions),
            "total_marks": sum(float(q.marks) for q in a.questions),
            "submissions_count": sum(1 for att in a.attempts if att.status == "SUBMITTED"),
            "batch_id": a.batch_id,
            "batch_name": a.batch.name if a.batch else "All Assigned",
            "start_window": a.start_window.isoformat() if a.start_window else None,
            "end_window": a.end_window.isoformat() if a.end_window else None,
            "audience_learners": [aud.learner_id for aud in a.audience_learners],
            "questions": [
                {
                    "id": q.id,
                    "bank_question_id": q.bank_question_id,
                    "title": q.question.title if q.question else "",
                    "type": q.question.question_type if q.question else "MCQ",
                    "marks": q.marks,
                    "order": q.sequence_order,
                }
                for q in sorted(a.questions, key=lambda x: x.sequence_order)
            ],
        }
        for a in assessments
    ]


@router.post("/assessments", status_code=status.HTTP_201_CREATED, summary="Create an assessment draft")
def create_assessment(
    payload: AssessmentCreateRequest,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    validate_mentor_targets(db, mentor, payload.batch_id, payload.learner_ids)

    assessment = Assessment(
        mentor_id=mentor.id,
        batch_id=payload.batch_id,
        title=payload.title,
        field=payload.field,
        instructions=payload.instructions,
        duration_minutes=payload.duration_minutes,
        passing_score=payload.passing_score,
        start_window=payload.start_window,
        end_window=payload.end_window,
        show_explanations=payload.show_explanations,
        mask_hidden_cases=payload.mask_hidden_cases,
        status="DRAFT",
        version=1,
    )
    db.add(assessment)
    db.flush()

    for lid in payload.learner_ids:
        db.add(AssessmentAudience(assessment_id=assessment.id, learner_id=lid))

    db.commit()
    db.refresh(assessment)
    return {"id": assessment.id, "title": assessment.title, "status": assessment.status, "version": assessment.version}


@router.put("/assessments/{assessment_id}", summary="Edit assessment (versions if published with submissions)")
def update_assessment(
    assessment_id: str,
    payload: AssessmentCreateRequest,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    assessment = db.get(Assessment, assessment_id)
    if not assessment or assessment.mentor_id != mentor.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found.")

    validate_mentor_targets(db, mentor, payload.batch_id, payload.learner_ids)

    # Check if assessment is published and has submissions
    submissions_count = (
        db.execute(
            select(func.count(AssessmentAttempt.id)).where(
                AssessmentAttempt.assessment_id == assessment.id
            )
        ).scalar()
        or 0
    )

    if assessment.status == "PUBLISHED" and submissions_count > 0:
        # Invariant: A published assessment with submissions cannot be edited in place. Version it!
        new_version = Assessment(
            mentor_id=mentor.id,
            batch_id=payload.batch_id,
            title=payload.title,
            field=payload.field,
            instructions=payload.instructions,
            duration_minutes=payload.duration_minutes,
            passing_score=payload.passing_score,
            start_window=payload.start_window,
            end_window=payload.end_window,
            show_explanations=payload.show_explanations,
            mask_hidden_cases=payload.mask_hidden_cases,
            status="DRAFT",
            version=assessment.version + 1,
        )
        db.add(new_version)
        db.flush()
        for q in assessment.questions:
            db.add(
                AssessmentQuestion(
                    assessment_id=new_version.id,
                    bank_question_id=q.bank_question_id,
                    sequence_order=q.sequence_order,
                    marks=q.marks,
                )
            )
        for lid in payload.learner_ids:
            db.add(AssessmentAudience(assessment_id=new_version.id, learner_id=lid))
        db.commit()
        db.refresh(new_version)
        return {
            "message": f"Assessment has active submissions. Created version {new_version.version} instead.",
            "id": new_version.id,
            "version": new_version.version,
        }

    assessment.title = payload.title
    assessment.field = payload.field
    assessment.instructions = payload.instructions
    assessment.duration_minutes = payload.duration_minutes
    assessment.passing_score = payload.passing_score
    assessment.start_window = payload.start_window
    assessment.end_window = payload.end_window
    assessment.show_explanations = payload.show_explanations
    assessment.mask_hidden_cases = payload.mask_hidden_cases
    assessment.batch_id = payload.batch_id

    # Sync audience
    db.execute(
        delete(AssessmentAudience).where(AssessmentAudience.assessment_id == assessment.id)
    )
    for lid in payload.learner_ids:
        db.add(AssessmentAudience(assessment_id=assessment.id, learner_id=lid))

    db.commit()
    return {"message": "Assessment updated.", "id": assessment.id, "version": assessment.version}


@router.post("/assessments/{assessment_id}/publish", summary="Publish an assessment")
def publish_assessment(
    assessment_id: str,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    assessment = db.get(Assessment, assessment_id)
    if not assessment or assessment.mentor_id != mentor.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found.")

    # Idempotency check: Publishing an already published assessment must be a no-op (no duplicate notifications)
    if assessment.status == "PUBLISHED":
        return {
            "id": assessment.id,
            "status": assessment.status,
            "message": "Assessment is already published.",
        }

    if len(assessment.questions) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot publish assessment without questions.")

    assessment.status = "PUBLISHED"

    recipients = set()
    # Notify learners in batch
    if assessment.batch_id:
        batch_learners = (
            db.execute(
                select(MentorLearnerAssignment.learner_id).where(
                    MentorLearnerAssignment.batch_id == assessment.batch_id
                )
            )
            .scalars()
            .all()
        )
        recipients.update(batch_learners)

    # Notify explicit audience
    audience_learners = (
        db.execute(
            select(AssessmentAudience.learner_id).where(
                AssessmentAudience.assessment_id == assessment.id
            )
        )
        .scalars()
        .all()
    )
    recipients.update(audience_learners)

    for lid in recipients:
        notif = Notification(
            recipient_id=lid,
            sender_id=mentor.id,
            title=f"New Assessment Available: {assessment.title}",
            message=f"Mentor {mentor.full_name} published assessment '{assessment.title}'. Duration: {assessment.duration_minutes} mins.",
            notification_type="ASSESSMENT",
            link="/learner/assessments",
        )
        db.add(notif)
        u = db.get(User, lid)
        if u and u.email:
            try:
                dispatch_email_notification(
                    to_email=u.email,
                    subject=f"New Assessment Available: {assessment.title}",
                    html_content=f"<p>Hello {u.full_name},</p><p>Mentor {mentor.full_name} published assessment <strong>{assessment.title}</strong>.</p><p>Duration: {assessment.duration_minutes} minutes.</p>",
                    text_content=f"Hello {u.full_name},\nMentor {mentor.full_name} published assessment '{assessment.title}'. Duration: {assessment.duration_minutes} mins.",
                )
            except Exception:
                pass

    db.commit()
    return {"id": assessment.id, "status": assessment.status}


@router.get("/assessments/{assessment_id}/questions", summary="Get questions attached to an assessment")
def get_assessment_questions(
    assessment_id: str,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
) -> list[dict[str, Any]]:
    assessment = db.get(Assessment, assessment_id)
    if not assessment or assessment.mentor_id != mentor.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found.")

    return [
        {
            "id": aq.id,
            "aq_id": aq.id,
            "assessment_id": aq.assessment_id,
            "bank_question_id": aq.bank_question_id,
            "sequence_order": aq.sequence_order,
            "order": aq.sequence_order,
            "marks": aq.marks,
            "title": aq.question.title if aq.question else "",
            "type": aq.question.question_type if aq.question else "MCQ",
            "question_type": aq.question.question_type if aq.question else "MCQ",
            "field": aq.question.field if aq.question else "",
            "difficulty": aq.question.difficulty if aq.question else "MEDIUM",
            "content": aq.question.question_text if aq.question else "",
            "options": [
                {
                    "id": opt.id,
                    "option_text": opt.option_text,
                    "is_correct": opt.is_correct,
                    "explanation": opt.explanation,
                }
                for opt in (getattr(aq.question, "options", None) or [])
            ],
            "coding_problem": (
                {
                    "constraints": aq.question.coding_problem.constraints,
                    "time_limit_ms": aq.question.coding_problem.time_limit_ms,
                    "memory_limit_mb": aq.question.coding_problem.memory_limit_mb,
                    "starter_code": aq.question.coding_problem.starter_code_json,
                }
                if aq.question and aq.question.coding_problem
                else None
            ),
        }
        for aq in sorted(assessment.questions, key=lambda x: x.sequence_order)
    ]


@router.post("/assessments/{assessment_id}/questions", status_code=status.HTTP_201_CREATED, summary="Attach question to assessment")
def attach_question_to_assessment(
    assessment_id: str,
    payload: AttachQuestionRequest,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    assessment = db.get(Assessment, assessment_id)
    if not assessment or assessment.mentor_id != mentor.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found.")

    qid = payload.question_id or payload.bank_question_id
    if not qid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="question_id is required.")

    bank_q = db.get(QuestionBank, qid)
    if not bank_q:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found in question bank.")

    if bank_q.author_id and bank_q.author_id != mentor.id and bank_q.author and bank_q.author.org_id != mentor.org_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied: Cannot use question from another organization.")

    submissions_count = (
        db.execute(
            select(func.count(AssessmentAttempt.id)).where(AssessmentAttempt.assessment_id == assessment.id)
        ).scalar()
        or 0
    )

    if assessment.status == "PUBLISHED" and submissions_count > 0:
        new_version = Assessment(
            mentor_id=mentor.id,
            batch_id=assessment.batch_id,
            title=assessment.title,
            field=assessment.field,
            instructions=assessment.instructions,
            duration_minutes=assessment.duration_minutes,
            passing_score=assessment.passing_score,
            start_window=assessment.start_window,
            end_window=assessment.end_window,
            show_explanations=assessment.show_explanations,
            mask_hidden_cases=assessment.mask_hidden_cases,
            status="DRAFT",
            version=assessment.version + 1,
        )
        db.add(new_version)
        db.flush()

        for q in assessment.questions:
            db.add(
                AssessmentQuestion(
                    assessment_id=new_version.id,
                    bank_question_id=q.bank_question_id,
                    sequence_order=q.sequence_order,
                    marks=q.marks,
                )
            )
        for aud in assessment.audience_learners:
            db.add(AssessmentAudience(assessment_id=new_version.id, learner_id=aud.learner_id))

        new_order = len(assessment.questions) + 1
        new_aq = AssessmentQuestion(
            assessment_id=new_version.id,
            bank_question_id=bank_q.id,
            sequence_order=payload.order or payload.sequence_order or new_order,
            marks=payload.marks,
        )
        db.add(new_aq)
        db.commit()
        db.refresh(new_version)
        return {
            "message": f"Assessment has active submissions. Created version {new_version.version} instead.",
            "versioned": True,
            "assessment_id": new_version.id,
            "new_assessment_id": new_version.id,
            "id": new_aq.id,
            "version": new_version.version,
        }

    order = payload.order or payload.sequence_order or (len(assessment.questions) + 1)
    existing = next((q for q in assessment.questions if q.bank_question_id == bank_q.id), None)
    if existing:
        existing.marks = payload.marks
        existing.sequence_order = order
        db.commit()
        db.refresh(existing)
        return {
            "id": existing.id,
            "assessment_id": assessment.id,
            "bank_question_id": bank_q.id,
            "marks": existing.marks,
            "sequence_order": existing.sequence_order,
            "title": bank_q.title,
        }

    aq = AssessmentQuestion(
        assessment_id=assessment.id,
        bank_question_id=bank_q.id,
        sequence_order=order,
        marks=payload.marks,
    )
    db.add(aq)
    db.commit()
    db.refresh(aq)
    return {
        "id": aq.id,
        "assessment_id": assessment.id,
        "bank_question_id": bank_q.id,
        "marks": aq.marks,
        "sequence_order": aq.sequence_order,
        "title": bank_q.title,
    }


@router.put("/assessments/{assessment_id}/questions", summary="Reorder or replace assessment questions")
def update_assessment_questions(
    assessment_id: str,
    payload: ReorderQuestionsRequest,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    assessment = db.get(Assessment, assessment_id)
    if not assessment or assessment.mentor_id != mentor.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found.")

    submissions_count = (
        db.execute(
            select(func.count(AssessmentAttempt.id)).where(AssessmentAttempt.assessment_id == assessment.id)
        ).scalar()
        or 0
    )

    target_assessment = assessment
    versioned = False
    if assessment.status == "PUBLISHED" and submissions_count > 0:
        versioned = True
        target_assessment = Assessment(
            mentor_id=mentor.id,
            batch_id=assessment.batch_id,
            title=assessment.title,
            field=assessment.field,
            instructions=assessment.instructions,
            duration_minutes=assessment.duration_minutes,
            passing_score=assessment.passing_score,
            start_window=assessment.start_window,
            end_window=assessment.end_window,
            show_explanations=assessment.show_explanations,
            mask_hidden_cases=assessment.mask_hidden_cases,
            status="DRAFT",
            version=assessment.version + 1,
        )
        db.add(target_assessment)
        db.flush()
        for aud in assessment.audience_learners:
            db.add(AssessmentAudience(assessment_id=target_assessment.id, learner_id=aud.learner_id))

    existing_by_bank = {q.bank_question_id: q for q in target_assessment.questions}
    existing_by_id = {q.id: q for q in target_assessment.questions}
    kept_ids = set()
    added = []

    for idx, item in enumerate(payload.questions, start=1):
        bank_qid = (
            item.bank_question_id
            or item.question_id
            or (existing_by_id.get(item.id or item.aq_id).bank_question_id if (item.id or item.aq_id) in existing_by_id else None)
            or (item.id if item.id in existing_by_bank else None)
        )
        if not bank_qid:
            continue
        bank_q = db.get(QuestionBank, bank_qid)
        if not bank_q:
            continue

        seq = item.order or item.sequence_order or idx
        match_aq = existing_by_id.get(item.id) or existing_by_id.get(item.aq_id) or existing_by_bank.get(bank_q.id)

        if match_aq and not versioned:
            match_aq.sequence_order = seq
            match_aq.marks = item.marks
            kept_ids.add(match_aq.id)
            added.append(match_aq)
        else:
            new_aq = AssessmentQuestion(
                assessment_id=target_assessment.id,
                bank_question_id=bank_q.id,
                sequence_order=seq,
                marks=item.marks,
            )
            db.add(new_aq)
            added.append(new_aq)

    if not versioned:
        for q in list(target_assessment.questions):
            if q.id not in kept_ids:
                db.delete(q)

    db.commit()
    return {
        "status": "updated",
        "message": "Questions updated.",
        "versioned": versioned,
        "assessment_id": target_assessment.id,
        "new_assessment_id": target_assessment.id if versioned else None,
        "version": target_assessment.version,
        "questions_count": len(added),
    }


@router.delete("/assessments/{assessment_id}/questions/{aq_id}", summary="Remove question from assessment")
def remove_question_from_assessment(
    assessment_id: str,
    aq_id: str,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    assessment = db.get(Assessment, assessment_id)
    if not assessment or assessment.mentor_id != mentor.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found.")

    submissions_count = (
        db.execute(
            select(func.count(AssessmentAttempt.id)).where(AssessmentAttempt.assessment_id == assessment.id)
        ).scalar()
        or 0
    )

    if assessment.status == "PUBLISHED" and submissions_count > 0:
        new_version = Assessment(
            mentor_id=mentor.id,
            batch_id=assessment.batch_id,
            title=assessment.title,
            field=assessment.field,
            instructions=assessment.instructions,
            duration_minutes=assessment.duration_minutes,
            passing_score=assessment.passing_score,
            start_window=assessment.start_window,
            end_window=assessment.end_window,
            show_explanations=assessment.show_explanations,
            mask_hidden_cases=assessment.mask_hidden_cases,
            status="DRAFT",
            version=assessment.version + 1,
        )
        db.add(new_version)
        db.flush()
        for q in assessment.questions:
            if q.id != aq_id and q.bank_question_id != aq_id:
                db.add(
                    AssessmentQuestion(
                        assessment_id=new_version.id,
                        bank_question_id=q.bank_question_id,
                        sequence_order=q.sequence_order,
                        marks=q.marks,
                    )
                )
        for aud in assessment.audience_learners:
            db.add(AssessmentAudience(assessment_id=new_version.id, learner_id=aud.learner_id))

        db.commit()
        return {
            "message": f"Assessment has active submissions. Created version {new_version.version} with question removed.",
            "versioned": True,
            "assessment_id": new_version.id,
            "version": new_version.version,
        }

    aq = db.execute(
        select(AssessmentQuestion).where(
            AssessmentQuestion.assessment_id == assessment.id,
            (AssessmentQuestion.id == aq_id) | (AssessmentQuestion.bank_question_id == aq_id),
        )
    ).scalar_one_or_none()

    if not aq:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question is not attached to this assessment.")

    db.delete(aq)
    db.commit()
    return {"status": "deleted", "message": "Question detached from assessment.", "id": aq.id}


@router.get("/assessments/{assessment_id}/notes", summary="List mentor study notes for an assessment")
def list_assessment_notes(
    assessment_id: str,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
) -> list[dict[str, Any]]:
    assessment = db.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found.")

    notes = (
        db.execute(
            select(AssessmentNote)
            .options(joinedload(AssessmentNote.author))
            .where(AssessmentNote.assessment_id == assessment_id)
            .order_by(AssessmentNote.created_at.desc())
        )
        .scalars()
        .all()
    )
    return [
        {
            "id": n.id,
            "assessment_id": n.assessment_id,
            "assessment_title": assessment.title,
            "author_id": n.author_id,
            "author_name": n.author.full_name if n.author else mentor.full_name,
            "title": n.title,
            "module_name": n.module_name,
            "summary": n.summary,
            "content": n.content,
            "key_takeaways": n.key_takeaways or [],
            "recommended_reading": n.recommended_reading or [],
            "estimated_read_time_minutes": n.estimated_read_time_minutes,
            "is_published": n.is_published,
            "created_at": n.created_at.isoformat() if n.created_at else None,
            "updated_at": n.updated_at.isoformat() if n.updated_at else None,
        }
        for n in notes
    ]


@router.post("/assessments/{assessment_id}/notes", status_code=status.HTTP_201_CREATED, summary="Create study note for an assessment module")
def create_assessment_note(
    assessment_id: str,
    payload: AssessmentNoteCreate,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    assessment = db.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found.")

    note = AssessmentNote(
        assessment_id=assessment.id,
        author_id=mentor.id,
        title=payload.title,
        module_name=payload.module_name or assessment.title,
        summary=payload.summary,
        content=payload.content,
        key_takeaways=payload.key_takeaways or [],
        recommended_reading=payload.recommended_reading or [],
        estimated_read_time_minutes=payload.estimated_read_time_minutes,
        is_published=payload.is_published,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return {
        "id": note.id,
        "assessment_id": note.assessment_id,
        "assessment_title": assessment.title,
        "author_id": note.author_id,
        "author_name": mentor.full_name,
        "title": note.title,
        "module_name": note.module_name,
        "summary": note.summary,
        "content": note.content,
        "key_takeaways": note.key_takeaways,
        "recommended_reading": note.recommended_reading,
        "estimated_read_time_minutes": note.estimated_read_time_minutes,
        "is_published": note.is_published,
        "created_at": note.created_at.isoformat(),
        "updated_at": note.updated_at.isoformat(),
    }


@router.put("/notes/{note_id}", summary="Update a study note")
def update_assessment_note(
    note_id: str,
    payload: AssessmentNoteUpdate,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    note = db.get(AssessmentNote, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Study note not found.")

    if payload.title is not None:
        note.title = payload.title
    if payload.module_name is not None:
        note.module_name = payload.module_name
    if payload.summary is not None:
        note.summary = payload.summary
    if payload.content is not None:
        note.content = payload.content
    if payload.key_takeaways is not None:
        note.key_takeaways = payload.key_takeaways
    if payload.recommended_reading is not None:
        note.recommended_reading = payload.recommended_reading
    if payload.estimated_read_time_minutes is not None:
        note.estimated_read_time_minutes = payload.estimated_read_time_minutes
    if payload.is_published is not None:
        note.is_published = payload.is_published

    db.commit()
    db.refresh(note)
    return {
        "id": note.id,
        "assessment_id": note.assessment_id,
        "author_id": note.author_id,
        "title": note.title,
        "module_name": note.module_name,
        "summary": note.summary,
        "content": note.content,
        "key_takeaways": note.key_takeaways,
        "recommended_reading": note.recommended_reading,
        "estimated_read_time_minutes": note.estimated_read_time_minutes,
        "is_published": note.is_published,
        "updated_at": note.updated_at.isoformat(),
    }


@router.delete("/notes/{note_id}", summary="Delete a study note")
def delete_assessment_note(
    note_id: str,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    note = db.get(AssessmentNote, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Study note not found.")
    db.delete(note)
    db.commit()
    return {"status": "deleted", "message": "Study note removed successfully.", "id": note_id}


@router.post("/questions", status_code=status.HTTP_201_CREATED, summary="Create Question in Question Bank (Unified route)")
def create_question_unified(
    payload: UnifiedQuestionCreateRequest,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    q_type = (payload.type or payload.question_type or "MCQ").upper()
    if q_type == "CODING" or (q_type == "SQL" and (payload.test_cases or payload.starter_code)):
        prob_payload = CodingProblemCreateRequest(
            title=payload.title,
            description=payload.description or payload.question_text or payload.title,
            category=payload.category,
            constraints=payload.constraints,
            field=payload.field,
            difficulty=payload.difficulty.upper(),
            marks=payload.marks,
            time_limit_ms=payload.time_limit_ms,
            memory_limit_mb=payload.memory_limit_mb,
            starter_code=payload.starter_code or ({"sql": "-- Write your SQL query here\n"} if q_type == "SQL" else {}),
            reference_solution=payload.reference_solution,
            test_cases=payload.test_cases,
        )
        res = add_coding_to_bank(prob_payload, db=db, mentor=mentor, _uow=_uow)
        if q_type == "SQL":
            bq = db.get(QuestionBank, res["id"])
            if bq:
                bq.question_type = "SQL"
                if bq.coding_problem:
                    bq.coding_problem.problem_type = "SQL"
                    bq.coding_problem.schema_ddl = payload.schema_ddl
                db.commit()
            res["type"] = "SQL"
        return res
    elif q_type in ("SHORT_ANSWER", "FILE_UPLOAD", "SCENARIO", "COMMUNICATION", "SQL"):
        cat_val = payload.category.value if isinstance(payload.category, AssessmentCategory) else str(payload.category)
        bank_q = QuestionBank(
            author_id=mentor.id,
            title=payload.title,
            question_text=payload.question_text or payload.description or payload.title,
            question_type=q_type,
            category=cat_val,
            field=payload.field,
            topic=payload.topic,
            difficulty=payload.difficulty.upper(),
            tags_json=payload.tags,
            explanation=payload.explanation,
            rubric_json=payload.rubric or {},
            is_active=True,
        )
        db.add(bank_q)
        db.commit()
        db.refresh(bank_q)
        return {
            "id": bank_q.id,
            "title": bank_q.title,
            "type": bank_q.question_type,
            "field": bank_q.field,
            "difficulty": bank_q.difficulty,
            "tags": bank_q.tags_json or [],
            "content": bank_q.question_text,
            "message": f"{q_type} question added to Question Bank.",
        }
    else:
        opts = payload.options
        if not opts:
            opts = [
                {"text": "Option A", "is_correct": True, "explanation": "Correct answer"},
                {"text": "Option B", "is_correct": False, "explanation": ""},
                {"text": "Option C", "is_correct": False, "explanation": ""},
                {"text": "Option D", "is_correct": False, "explanation": ""},
            ]
        mcq_payload = McqQuestionCreateRequest(
            title=payload.title,
            question_text=payload.question_text or payload.description or payload.title,
            category=payload.category,
            field=payload.field,
            topic=payload.topic,
            difficulty=payload.difficulty.upper(),
            tags=payload.tags,
            explanation=payload.explanation,
            options=opts,
        )
        return add_mcq_to_bank(mcq_payload, db=db, mentor=mentor, _uow=_uow)


@router.get("/questions", summary="List question bank items")
@router.get("/question-bank", summary="List question bank items alias")
def list_question_bank(
    field: str | None = None,
    difficulty: str | None = None,
    category: str | None = None,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
) -> list[dict[str, Any]]:
    query = select(QuestionBank)
    if field:
        query = query.where(QuestionBank.field == field)
    if difficulty:
        query = query.where(QuestionBank.difficulty == difficulty.upper())
    if category:
        query = query.where(QuestionBank.category == category)

    items = db.execute(query).scalars().all()
    return [
        {
            "id": q.id,
            "title": q.title,
            "type": q.question_type,
            "field": q.field,
            "category": getattr(q, "category", "Technical Knowledge"),
            "difficulty": q.difficulty,
            "tags": q.tags_json or [],
            "content": q.question_text,
        }
        for q in items
    ]


@router.post("/question-bank/mcq", status_code=status.HTTP_201_CREATED, summary="Add MCQ to Question Bank")
def add_mcq_to_bank(
    payload: McqQuestionCreateRequest,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    cat_val = payload.category.value if isinstance(payload.category, AssessmentCategory) else str(payload.category)
    q = QuestionBank(
        author_id=mentor.id,
        title=payload.title,
        question_text=payload.question_text,
        question_type="MCQ",
        category=cat_val,
        field=payload.field,
        topic=payload.topic,
        difficulty=payload.difficulty.upper(),
        tags_json=payload.tags,
        explanation=payload.explanation,
    )
    db.add(q)
    db.flush()

    for idx, opt in enumerate(payload.options, start=1):
        o = McqOption(
            question_id=q.id,
            option_text=opt["text"],
            is_correct=bool(opt.get("is_correct", False)),
            explanation=opt.get("explanation"),
            sequence_order=idx,
        )
        db.add(o)

    db.commit()
    return {"id": q.id, "title": q.title, "type": "MCQ"}


@router.post("/question-bank/coding", status_code=status.HTTP_201_CREATED, summary="Add Coding Problem to Question Bank")
def add_coding_to_bank(
    payload: CodingProblemCreateRequest,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    cat_val = payload.category.value if isinstance(payload.category, AssessmentCategory) else str(payload.category)
    q = QuestionBank(
        author_id=mentor.id,
        title=payload.title,
        question_text=payload.description,
        question_type="CODING",
        category=cat_val,
        field=payload.field,
        topic="Algorithms",
        difficulty=payload.difficulty.upper(),
    )
    db.add(q)
    db.flush()

    prob = CodingProblem(
        bank_id=q.id,
        title=payload.title,
        description=payload.description,
        constraints=payload.constraints,
        field=payload.field,
        difficulty=payload.difficulty.upper(),
        marks=payload.marks,
        time_limit_ms=payload.time_limit_ms,
        memory_limit_mb=payload.memory_limit_mb,
        starter_code_json=payload.starter_code,
        reference_solution=payload.reference_solution,
    )
    db.add(prob)
    db.flush()

    for tc in payload.test_cases:
        t = TestCase(
            problem_id=prob.id,
            input_data=tc.get("input_data") or tc.get("input") or "",
            expected_output=tc.get("expected_output") or tc.get("output") or "",
            is_hidden=bool(tc.get("is_hidden", False)),
            weight=float(tc.get("weight", 1.0)),
        )
        db.add(t)

    db.commit()
    return {"id": q.id, "coding_problem_id": prob.id, "title": prob.title, "type": "CODING"}


@router.get("/assessments/{assessment_id}/analysis", summary="Result analysis with score distribution and CSV export")
@router.get("/assessments/{assessment_id}/results", summary="Assessment results analysis alias")
def get_assessment_analysis(
    assessment_id: str,
    export: bool = False,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
) -> Any:
    assessment = db.get(Assessment, assessment_id)
    if not assessment or assessment.mentor_id != mentor.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found.")

    attempts = (
        db.execute(
            select(AssessmentAttempt)
            .options(joinedload(AssessmentAttempt.learner))
            .where(AssessmentAttempt.assessment_id == assessment.id, AssessmentAttempt.status == "SUBMITTED")
        )
        .scalars()
        .all()
    )

    if export:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Learner Name", "Email", "Score", "Total Marks", "Passed", "Submitted At"])
        for a in attempts:
            writer.writerow([
                a.learner.full_name if a.learner else "",
                a.learner.email if a.learner else "",
                a.score,
                a.total_marks,
                "YES" if a.passed else "NO",
                a.submit_time.isoformat() if a.submit_time else "",
            ])
        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=assessment_{assessment_id}_results.csv"},
        )

    scores = [a.score for a in attempts]
    avg_score = sum(scores) / len(scores) if scores else 0.0
    pass_rate = (sum(1 for a in attempts if a.passed) / len(attempts) * 100.0) if attempts else 0.0

    from app.services.analytics_service import analyze_assessment_comprehensive

    comp_analysis = analyze_assessment_comprehensive(assessment_id, db)

    return {
        "assessment_title": assessment.title,
        "n": comp_analysis.get("n", len(attempts)),
        "computed_at": comp_analysis.get("computed_at"),
        "definition": comp_analysis.get("definition"),
        "total_attempts": len(attempts),
        "average_score": round(avg_score, 1),
        "pass_rate": round(pass_rate, 1),
        "funnel": comp_analysis.get("funnel"),
        "item_analysis": comp_analysis.get("item_analysis"),
        "score_distribution": {
            "0-50": sum(1 for s in scores if s < 50),
            "50-70": sum(1 for s in scores if 50 <= s < 70),
            "70-90": sum(1 for s in scores if 70 <= s < 90),
            "90-100": sum(1 for s in scores if s >= 90),
        },
        "learners": [
            {
                "id": a.learner_id,
                "attempt_id": a.id,
                "name": a.learner.full_name if a.learner else "Learner",
                "email": a.learner.email if a.learner else "",
                "score": a.score,
                "passed": a.passed,
                "grading_status": getattr(a, "grading_status", "GRADED"),
                "report_status": getattr(a, "report_status", "NONE"),
                "submit_time": a.submit_time.isoformat() if a.submit_time else None,
            }
            for a in attempts
        ],
    }


@router.get("/assessments/{assessment_id}/results/export", summary="Direct CSV export of assessment results")
def export_assessment_results_csv(
    assessment_id: str,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
) -> Response:
    return get_assessment_analysis(assessment_id=assessment_id, export=True, db=db, mentor=mentor)


@router.get("/assessments/{assessment_id}/ai-insights", summary="Get AI assessment difficulty and cohort insights")
def get_assessment_ai_insights(
    assessment_id: str,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
) -> dict[str, Any]:
    assessment = db.get(Assessment, assessment_id)
    if not assessment or assessment.mentor_id != mentor.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found.")
    from app.services.ai_analytics_engine import analyze_assessment_ai_insights
    return analyze_assessment_ai_insights(assessment_id, db)


@router.get("/assessments/{assessment_id}/submissions", summary="List attempts and grading statuses for an assessment")
def list_assessment_submissions(
    assessment_id: str,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
) -> list[dict[str, Any]]:
    assessment = db.get(Assessment, assessment_id)
    if not assessment or assessment.mentor_id != mentor.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found.")

    attempts = (
        db.execute(
            select(AssessmentAttempt)
            .where(AssessmentAttempt.assessment_id == assessment.id, AssessmentAttempt.status == "SUBMITTED")
            .order_by(AssessmentAttempt.submit_time.desc())
        )
        .scalars()
        .all()
    )

    return [
        {
            "id": a.id,
            "learner_id": a.learner_id,
            "learner_name": a.learner.full_name if a.learner else "Learner",
            "learner_email": a.learner.email if a.learner else "",
            "score": float(a.score),
            "total_marks": float(a.total_marks),
            "passed": bool(a.passed),
            "status": a.status,
            "grading_status": getattr(a, "grading_status", "GRADED"),
            "report_status": getattr(a, "report_status", "NONE"),
            "submit_time": a.submit_time.isoformat() if a.submit_time else None,
            "has_report": bool(a.report_json),
        }
        for a in attempts
    ]


@router.get("/assessments/attempts/{attempt_id}/answers", summary="Get answers for manual grading")
def get_attempt_answers_for_grading(
    attempt_id: str,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
) -> dict[str, Any]:
    attempt = db.get(AssessmentAttempt, attempt_id)
    if not attempt or attempt.assessment.mentor_id != mentor.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found.")

    answers_data = []
    for ans in attempt.answers:
        bq = ans.question
        aq = next((q for q in attempt.assessment.questions if q.bank_question_id == bq.id), None)
        answers_data.append({
            "answer_id": ans.id,
            "question_id": bq.id,
            "question_title": bq.title,
            "question_text": bq.question_text,
            "question_type": bq.question_type,
            "marks": aq.marks if aq else 10.0,
            "score_awarded": float(ans.score_awarded),
            "grading_status": getattr(ans, "grading_status", "GRADED"),
            "text_response": ans.text_response,
            "file_url": ans.file_url,
            "file_name": ans.file_name,
            "mentor_feedback": ans.mentor_feedback,
            "rubric": getattr(bq, "rubric_json", {}) or {},
        })

    return {
        "attempt_id": attempt.id,
        "assessment_id": attempt.assessment_id,
        "assessment_title": attempt.assessment.title,
        "learner_name": attempt.learner.full_name if attempt.learner else "Learner",
        "score": float(attempt.score),
        "total_marks": float(attempt.total_marks),
        "passed": bool(attempt.passed),
        "grading_status": getattr(attempt, "grading_status", "GRADED"),
        "report_status": getattr(attempt, "report_status", "NONE"),
        "answers": answers_data,
    }


@router.post("/assessments/attempts/{attempt_id}/grade", summary="Grade subjective answers manually")
def grade_attempt_answers(
    attempt_id: str,
    payload: GradeAttemptRequest,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    attempt = db.get(AssessmentAttempt, attempt_id)
    if not attempt or attempt.assessment.mentor_id != mentor.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found.")

    grade_map = {g.answer_id: g for g in payload.grades}
    q_marks_map = {q.bank_question_id: float(q.marks) for q in attempt.assessment.questions}

    for ans in attempt.answers:
        if ans.id in grade_map:
            item = grade_map[ans.id]
            qid = getattr(ans, "bank_question_id", getattr(ans, "question_id", None))
            max_marks = q_marks_map.get(qid, float(getattr(getattr(ans, "question", None), "marks", 10.0)))
            
            # 0.2 Bounds validation: 0 <= score_awarded <= question marks
            if item.score_awarded < 0 or item.score_awarded > max_marks:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Score awarded ({item.score_awarded}) for answer '{ans.id}' must be between 0 and maximum question marks ({max_marks}).",
                )

            # 0.2 Audit logging for overrides of auto-graded scores
            was_auto_graded = getattr(ans, "grading_status", None) == "GRADED" and ans.score_awarded is not None
            if was_auto_graded and float(ans.score_awarded) != float(item.score_awarded):
                reason = (item.override_reason or item.feedback or "").strip()
                if not reason:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Overriding auto-graded score for answer '{ans.id}' requires an override reason.",
                    )
                audit = AuditLog(
                    org_id=mentor.org_id,
                    actor_id=mentor.id,
                    action="GRADE_OVERRIDE",
                    resource="assessment_answers",
                    resource_id=ans.id,
                    reason=reason,
                    before_state_json={
                        "attempt_id": attempt.id,
                        "question_id": qid,
                        "old_score": float(ans.score_awarded),
                        "grading_status": ans.grading_status,
                    },
                    after_state_json={
                        "attempt_id": attempt.id,
                        "question_id": qid,
                        "new_score": float(item.score_awarded),
                        "grading_status": "GRADED",
                        "override_reason": reason,
                    },
                )
                db.add(audit)

            ans.score_awarded = float(item.score_awarded)
            ans.mentor_feedback = item.feedback
            ans.grading_status = "GRADED"

    total_earned = sum(float(a.score_awarded) for a in attempt.answers)
    attempt.score = total_earned
    total_marks = attempt.total_marks or sum(q.marks for q in attempt.assessment.questions) or 100.0
    percentage = (total_earned / total_marks) * 100.0 if total_marks > 0 else 0.0
    attempt.passed = percentage >= attempt.assessment.passing_score

    all_graded = all(getattr(a, "grading_status", "GRADED") == "GRADED" for a in attempt.answers)
    attempt.grading_status = "GRADED" if all_graded else "PENDING_REVIEW"
    db.commit()

    try:
        from app.services.ai_analytics_engine import generate_growth_ring_report
        generate_growth_ring_report(attempt.id, db)
    except Exception as e:
        logger.warning(f"Could not re-generate growth ring report: {e}")

    return {
        "status": "success",
        "attempt_id": attempt.id,
        "score": float(attempt.score),
        "passed": bool(attempt.passed),
        "grading_status": attempt.grading_status,
        "message": "Attempt graded successfully.",
    }


@router.post("/assessments/attempts/{attempt_id}/answers/{answer_id}/ai-evaluate", summary="AI Subjective Rubric Evaluation")
def ai_evaluate_subjective_answer(
    attempt_id: str,
    answer_id: str,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    """Provide AI-driven rubric evaluation for open-ended or subjective trainee answers."""
    attempt = db.get(AssessmentAttempt, attempt_id)
    if not attempt or attempt.assessment.mentor_id != mentor.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment attempt not found.")

    ans = db.get(Answer, answer_id)
    if not ans or ans.attempt_id != attempt.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found in this attempt.")

    bq = ans.question
    aq = next((q for q in attempt.assessment.questions if q.bank_question_id == bq.id), None)
    max_marks = float(aq.marks) if aq else 10.0

    student_response = (ans.text_response or ans.file_name or "").strip()
    from app.services.rubric_evaluator import evaluate_subjective_response
    evaluation = evaluate_subjective_response(
        question_title=bq.title,
        question_text=bq.question_text,
        student_response=student_response,
        max_marks=max_marks,
        rubric_criteria=getattr(bq, "rubric_json", None),
    )
    return evaluation


@router.get("/assessments/attempts/{attempt_id}/report/pdf", summary="Export Growth Ring Report as PDF (Mentor)")
def export_growth_ring_pdf_mentor(
    attempt_id: str,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
) -> Response:
    """Generate and return official CSM Growth Ring evaluation PDF for mentor review."""
    attempt = db.get(AssessmentAttempt, attempt_id)
    if not attempt or attempt.assessment.mentor_id != mentor.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment attempt not found.")

    if not attempt.report_json:
        from app.services.ai_analytics_engine import generate_growth_ring_report
        generate_growth_ring_report(attempt.id, db)
        db.refresh(attempt)

    from app.services.pdf_report_service import generate_growth_ring_pdf
    pdf_bytes = generate_growth_ring_pdf(attempt.report_json)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="growth_ring_report_{attempt.id[:8]}.pdf"'},
    )


@router.post("/assessments/attempts/{attempt_id}/approve-report", summary="Approve AI Growth Ring report for learner")
def approve_assessment_report(
    attempt_id: str,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    attempt = db.get(AssessmentAttempt, attempt_id)
    if not attempt or attempt.assessment.mentor_id != mentor.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found.")

    attempt.report_status = "APPROVED"
    attempt.report_approved_at = datetime.now(UTC)
    db.commit()
    return {"status": "APPROVED", "attempt_id": attempt.id, "message": "Growth Ring report approved and released to learner."}


@router.post("/assessments/attempts/{attempt_id}/reject-report", summary="Reject/Request revision on AI report")
def reject_assessment_report(
    attempt_id: str,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    attempt = db.get(AssessmentAttempt, attempt_id)
    if not attempt or attempt.assessment.mentor_id != mentor.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found.")

    attempt.report_status = "REJECTED"
    db.commit()
    return {"status": "REJECTED", "attempt_id": attempt.id, "message": "Growth Ring report held for revision."}


@router.get("/learners/{learner_id}/ai-diagnostic", summary="Get mentor/admin AI diagnostic review for a learner")
def get_learner_ai_diagnostic_for_mentor(
    learner_id: str,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_role("MENTOR", "ADMIN")),
) -> dict[str, Any]:
    if (mentor.role or "").upper() != "ADMIN":
        if not verify_mentor_learner_access(mentor, learner_id, db):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Learner is not assigned to you.")
    from app.services.ai_analytics_engine import analyze_learner_performance
    return analyze_learner_performance(learner_id, db)


@router.get("/batches", summary="List batches assigned to this mentor")
def get_mentor_batches(
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
) -> list[dict[str, Any]]:
    assignments = db.execute(
        select(MentorLearnerAssignment).where(
            MentorLearnerAssignment.mentor_id == mentor.id,
            MentorLearnerAssignment.batch_id.isnot(None),
        )
    ).scalars().all()
    batch_ids = list({a.batch_id for a in assignments if a.batch_id})
    if not batch_ids:
        return []
    batches = db.execute(select(Batch).where(Batch.id.in_(batch_ids))).scalars().all()
    return [{"id": b.id, "name": b.name, "field": b.field} for b in batches]


@router.get("/learners", summary="List learners assigned to this mentor")
def get_assigned_learners(
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
) -> list[dict[str, Any]]:
    from app.core.cache import fast_cache
    cache_key = f"mentor:learners:{mentor.id}"
    cached = fast_cache.get(cache_key)
    if cached is not None:
        return cached
    # Get all batches this mentor is assigned to
    batches = db.execute(
        select(Batch).join(MentorLearnerAssignment, MentorLearnerAssignment.batch_id == Batch.id).where(
            MentorLearnerAssignment.mentor_id == mentor.id
        )
    ).scalars().all()
    batch_ids = [b.id for b in batches]

    assignments = db.execute(
        select(MentorLearnerAssignment).where(MentorLearnerAssignment.mentor_id == mentor.id)
    ).scalars().all()
    learner_ids = list({a.learner_id for a in assignments if a.learner_id})

    if not learner_ids and batch_ids:
        # Check if learners are in the batches
        batch_assignments = db.execute(
            select(MentorLearnerAssignment).where(MentorLearnerAssignment.batch_id.in_(batch_ids))
        ).scalars().all()
        learner_ids = list({a.learner_id for a in batch_assignments if a.learner_id})

    if not learner_ids:
        return []

    learners = db.execute(select(User).where(User.id.in_(learner_ids))).scalars().all()
    if not learners:
        return []

    # Eager load assignments with batch for all learners in one query
    learner_assignments = db.execute(
        select(MentorLearnerAssignment)
        .options(joinedload(MentorLearnerAssignment.batch))
        .where(MentorLearnerAssignment.learner_id.in_(learner_ids))
    ).scalars().all()
    batch_map = {
        la.learner_id: (la.batch.name if la.batch else "Direct Assignment")
        for la in learner_assignments
        if la.learner_id
    }

    # Grouped average score in one query
    score_rows = db.execute(
        select(AssessmentAttempt.learner_id, func.avg(AssessmentAttempt.score))
        .where(AssessmentAttempt.learner_id.in_(learner_ids), AssessmentAttempt.status == "SUBMITTED")
        .group_by(AssessmentAttempt.learner_id)
    ).all()
    score_map = {row[0]: round(float(row[1]), 1) for row in score_rows}

    # Remarks in one query
    remarks = db.execute(
        select(MentorRemark)
        .where(MentorRemark.learner_id.in_(learner_ids))
        .order_by(MentorRemark.created_at.desc())
    ).scalars().all()
    remark_map: dict[str, str] = {}
    for r in remarks:
        if r.learner_id not in remark_map:
            remark_map[r.learner_id] = r.remark_text

    result = [
        {
            "id": l.id,
            "name": l.full_name,
            "full_name": l.full_name,
            "email": l.email,
            "streak_days": l.streak_days or 0,
            "batch_name": batch_map.get(l.id, "Direct Assignment"),
            "avg_score": score_map.get(l.id, 0.0),
            "latest_remark": remark_map.get(l.id, ""),
        }
        for l in learners
    ]
    fast_cache.set(cache_key, result, ttl_seconds=30.0)
    return result


# --- Learner Review & Remarks ---
@router.post("/learners/{learner_id}/remarks", summary="Add qualitative remarks visible to learner")
def add_learner_remark(
    learner_id: str,
    payload: RemarkCreateRequest,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    if not verify_mentor_learner_access(mentor, learner_id, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Learner is not assigned to you.")

    remark = MentorRemark(
        mentor_id=mentor.id,
        learner_id=learner_id,
        assessment_id=payload.assessment_id,
        meeting_id=payload.meeting_id,
        remark_text=payload.remark_text,
        visibility=payload.visibility,
    )
    db.add(remark)

    notif = Notification(
        recipient_id=learner_id,
        sender_id=mentor.id,
        title="New Feedback from Your Mentor",
        message=f"Mentor {mentor.full_name} shared feedback: '{payload.remark_text[:80]}...'",
        notification_type="SYSTEM",
        link="/learner/dashboard",
    )
    db.add(notif)
    db.commit()
    return {"message": "Feedback submitted.", "id": remark.id}


def serialize_talent_alert(a: TalentAlert) -> dict[str, Any]:
    ev = a.evidence_json or {}
    return {
        "id": a.id,
        "learner_id": a.learner_id,
        "learner_name": a.learner.full_name if a.learner else "Learner",
        "mentor_id": a.mentor_id,
        "mentor_name": a.mentor.full_name if a.mentor else "Mentor",
        "field": a.field,
        "active_days": ev.get("active_days_30d") or ev.get("active_days") or 0,
        "accuracy": round(float(ev.get("weighted_accuracy") or ev.get("accuracy") or 0.0), 1),
        "problems_count": ev.get("problems_attempted") or ev.get("problems_count") or 0,
        "dedication_score": round(float(ev.get("dedication_score") or ev.get("score") or 0.0), 0),
        "acceptance_rate": round(float(ev.get("acceptance_rate") or 0.0), 1),
        "evidence": ev,
        "status": a.status,
        "action_taken": a.action_taken,
        "action_notes": a.action_notes,
        "action_time": a.action_time.isoformat() if a.action_time else None,
        "created_at": a.created_at.isoformat() if a.created_at else None,
        "message": f"{a.learner.full_name if a.learner else 'Learner'} achieved high dedication thresholds in {a.field} track.",
    }


@router.get("/spotlight", summary="List talent spotlight alerts for mentor")
def get_talent_spotlight_alerts(
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
) -> list[dict[str, Any]]:
    alerts = (
        db.execute(
            select(TalentAlert)
            .where(TalentAlert.mentor_id == mentor.id)
            .order_by(TalentAlert.created_at.desc())
        )
        .scalars()
        .all()
    )
    return [serialize_talent_alert(a) for a in alerts]


# --- Talent Spotlight Actions ---
@router.post("/talent-alerts/{alert_id}/action", summary="Act on Talent Spotlight alert")
@router.post("/spotlight/{alert_id}/action", summary="Act on Talent Spotlight alert alias")
def act_on_talent_alert(
    alert_id: str,
    payload: AlertActionRequest,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    alert = db.get(TalentAlert, alert_id)
    if not alert or alert.mentor_id != mentor.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found.")

    # Invariant: Block repeat actions on a closed alert with 409 Conflict
    if alert.status != "PENDING":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Repeat actions blocked: Alert is already closed with status '{alert.status}'.",
        )

    action_norm = "DISMISSED" if payload.action in {"DISMISS", "DISMISSED"} else payload.action
    alert.status = action_norm
    alert.action_taken = action_norm
    alert.action_notes = payload.notes
    alert.action_time = datetime.now(UTC)

    # 1. INVITE_ASSESSMENT must create a real assessment_audience row for a chosen assessment
    if payload.action == "INVITE_ASSESSMENT":
        target_assessment = None
        if payload.assessment_id:
            target_assessment = db.get(Assessment, payload.assessment_id)
            if not target_assessment:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target assessment not found.")
        else:
            # Query mentor's latest published assessment or any published assessment in the track
            target_assessment = (
                db.execute(
                    select(Assessment)
                    .where(Assessment.mentor_id == mentor.id, Assessment.status == "PUBLISHED")
                    .order_by(Assessment.created_at.desc())
                )
                .scalars()
                .first()
            )
            if not target_assessment:
                target_assessment = (
                    db.execute(
                        select(Assessment)
                        .where(Assessment.status == "PUBLISHED")
                        .order_by(Assessment.created_at.desc())
                    )
                    .scalars()
                    .first()
                )

        if target_assessment:
            existing_aud = db.execute(
                select(AssessmentAudience).where(
                    AssessmentAudience.assessment_id == target_assessment.id,
                    AssessmentAudience.learner_id == alert.learner_id,
                )
            ).first()
            if not existing_aud:
                db.add(AssessmentAudience(assessment_id=target_assessment.id, learner_id=alert.learner_id))

        notif = Notification(
            recipient_id=alert.learner_id,
            sender_id=mentor.id,
            title="Special Assessment Invitation",
            message=f"Based on your outstanding practice dedication in {alert.field}, you have been invited to assessment '{target_assessment.title if target_assessment else 'Assessment'}'.",
            notification_type="ASSESSMENT",
            link="/learner/assessments",
        )
        db.add(notif)

    # 2. SCHEDULE_INTERVIEW must create a real Meeting for that learner
    elif payload.action == "SCHEDULE_INTERVIEW":
        m_date = payload.meeting_date or datetime.now(UTC).date().isoformat()
        s_time = payload.start_time or "14:00"
        e_time = payload.end_time or "15:00"
        m_link = payload.meeting_link or "https://meet.google.com/talent-interview"
        validate_meeting_url(m_link, settings.MEETING_ALLOWLIST_HOSTS)

        interview_meeting = Meeting(
            title=f"Talent Interview: {alert.learner.full_name if alert.learner else 'Learner'}",
            description=f"Special talent interview for {alert.field}. Notes: {payload.notes or 'None'}",
            meeting_date=m_date,
            start_time=s_time,
            end_time=e_time,
            duration_minutes=60,
            meeting_link=m_link,
            mentor_id=mentor.id,
            status="SCHEDULED",
        )
        db.add(interview_meeting)
        db.flush()
        db.add(MeetingAudience(meeting_id=interview_meeting.id, learner_id=alert.learner_id))

        notif = Notification(
            recipient_id=alert.learner_id,
            sender_id=mentor.id,
            title="Interview Scheduled: Talent Spotlight",
            message=f"Your mentor scheduled a talent review interview on {m_date} at {s_time}.",
            notification_type="MEETING",
            link="/learner/meetings",
        )
        db.add(notif)

    # 3. RECOMMEND_PROMOTION must persist a record visible to admin
    elif payload.action == "RECOMMEND_PROMOTION":
        audit = AuditLog(
            org_id=mentor.org_id,
            actor_id=mentor.id,
            action="RECOMMEND_PROMOTION",
            resource="talent_alerts",
            resource_id=alert.id,
            reason=payload.notes,
            after_state_json={
                "alert_id": alert.id,
                "learner_id": alert.learner_id,
                "field": alert.field,
                "status": "RECOMMENDED_PROMOTION",
                "notes": payload.notes,
            },
        )
        db.add(audit)

        notif = Notification(
            recipient_id=alert.learner_id,
            sender_id=mentor.id,
            title="Promotion Recommendation",
            message=f"Your mentor recommended you for competency milestone advancement in {alert.field}!",
            notification_type="SYSTEM",
            link="/learner/profile",
        )
        db.add(notif)

    # Record discrete audit action log
    action_log = AlertAction(
        alert_id=alert.id,
        mentor_id=mentor.id,
        action_taken=payload.action,
        notes=payload.notes,
    )
    db.add(action_log)

    db.commit()
    return {"message": "Action recorded successfully.", "status": alert.status}


# --- Needs Attention Queue & Role Chatbot (Phase B) ---
class ChatMessageItem(BaseModel):
    role: str
    content: str


class MentorChatbotRequest(BaseModel):
    message: str
    history: list[ChatMessageItem] = Field(default_factory=list)


@router.get("/learners/needs-attention", summary="Get priority queue of trainees requiring mentor intervention")
def get_learners_needs_attention(
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
) -> list[dict[str, Any]]:
    """Identify trainees with failing assessment attempts, pending grading, or broken streaks."""
    # Find assigned learners
    learner_query = select(MentorLearnerAssignment.learner_id).where(
        MentorLearnerAssignment.mentor_id == mentor.id
    )
    assigned_learner_ids = list(set(db.execute(learner_query).scalars().all()))

    if not assigned_learner_ids:
        return []

    attention_items = []
    learners = db.execute(select(User).where(User.id.in_(assigned_learner_ids))).scalars().all()

    for l in learners:
        # Check for unreviewed subjective answers
        pending_att = db.execute(
            select(AssessmentAttempt)
            .where(
                AssessmentAttempt.learner_id == l.id,
                AssessmentAttempt.status == "SUBMITTED",
                AssessmentAttempt.grading_status == "PENDING_REVIEW",
            )
        ).scalars().first()

        if pending_att:
            attention_items.append({
                "learner_id": l.id,
                "learner_name": l.full_name,
                "learner_email": l.email,
                "urgency": "HIGH",
                "reason": f"Pending subjective grading on '{pending_att.assessment.title if pending_att.assessment else 'Assessment'}'",
                "attempt_id": pending_att.id,
                "action_type": "GRADE_SUBMISSION",
            })
            continue

        # Check for recent failed assessment
        latest_att = db.execute(
            select(AssessmentAttempt)
            .where(AssessmentAttempt.learner_id == l.id, AssessmentAttempt.status == "SUBMITTED")
            .order_by(AssessmentAttempt.submit_time.desc())
        ).scalars().first()

        if latest_att and not latest_att.passed:
            score_pct = (float(latest_att.score) / float(latest_att.total_marks or 100.0)) * 100.0
            attention_items.append({
                "learner_id": l.id,
                "learner_name": l.full_name,
                "learner_email": l.email,
                "urgency": "HIGH",
                "reason": f"Failed '{latest_att.assessment.title if latest_att.assessment else 'Assessment'}' with {score_pct:.1f}%",
                "attempt_id": latest_att.id,
                "action_type": "SCHEDULE_1ON1",
            })
            continue

        # Check for inactive streak
        if l.streak_days == 0:
            attention_items.append({
                "learner_id": l.id,
                "learner_name": l.full_name,
                "learner_email": l.email,
                "urgency": "MEDIUM",
                "reason": "Learning streak lapsed to 0 days (no practice activity)",
                "attempt_id": None,
                "action_type": "SEND_NUDGE",
            })

    return attention_items


@router.post("/chatbot/chat", summary="Chat with TRELLIS Mentor Assistant")
def chat_with_mentor_assistant(
    payload: MentorChatbotRequest,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    from app.ai.chatbot.chat_service import chat_role
    history_dicts = [{"role": m.role, "content": m.content} for m in payload.history]
    result = chat_role(
        user=mentor,
        user_message=payload.message,
        db=db,
        history=history_dicts,
    )
    if "error" in result and result["error"] == "RATE_LIMIT_EXCEEDED":
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=result["message"])
    return result


@router.post("/chatbot/stream", summary="Stream chat with TRELLIS Mentor Assistant (POST)")
def stream_with_mentor_assistant(
    payload: MentorChatbotRequest,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
) -> StreamingResponse:
    from app.ai.chatbot.chat_service import stream_chat_role
    return StreamingResponse(
        stream_chat_role(user=mentor, user_message=payload.message, db=db),
        media_type="text/event-stream",
    )


# --- Assessment Presets & CSV Import/Export Studio (Phase 3.5) ---

class QuestionImportRequest(BaseModel):
    csv_content: str
    dry_run: bool = True


@router.get("/assessments/templates", summary="Get role and learning path assessment templates/presets (Phase 3.5)")
def get_assessment_templates(
    mentor: User = Depends(require_mentor),
) -> list[dict[str, Any]]:
    return [
        {
            "id": "FULLSTACK_ENTRY",
            "name": "Junior Full-Stack Engineering Entry",
            "field": "Web & Full Stack",
            "target_experience": "0-2 Years",
            "duration_minutes": 60,
            "passing_score": 60.0,
            "proctoring_flags": {"strict_tab_monitoring": True, "fullscreen_required": False},
            "category_split": {"Technical Knowledge": 40, "Coding": 40, "Quantitative Aptitude": 20},
            "instructions": "Baseline engineering evaluation covering JavaScript/TypeScript, REST architecture, and core algorithms.",
        },
        {
            "id": "CLOUD_DEVOPS_MID",
            "name": "Mid-Level Cloud Platform & DevOps",
            "field": "Cloud & DevOps",
            "target_experience": "2-4 Years",
            "duration_minutes": 75,
            "passing_score": 65.0,
            "proctoring_flags": {"strict_tab_monitoring": True, "fullscreen_required": True},
            "category_split": {"Technical Knowledge": 50, "Coding": 30, "Situational Judgement": 20},
            "instructions": "Production infrastructure readiness sprint focusing on Docker, Kubernetes, CI/CD, and system diagnostics.",
        },
        {
            "id": "DATA_AI_SPECIALIST",
            "name": "Senior Data Engineering & AI Sprint",
            "field": "Data & AI",
            "target_experience": "3-6 Years",
            "duration_minutes": 90,
            "passing_score": 70.0,
            "proctoring_flags": {"strict_tab_monitoring": True, "fullscreen_required": True},
            "category_split": {"Technical Knowledge": 40, "Coding": 40, "Logical Reasoning": 20},
            "instructions": "Advanced data pipeline architecture, SQL query tuning, Spark optimizations, and LLM evaluation benchmarks.",
        },
        {
            "id": "SYSTEMS_KERNEL",
            "name": "Core Systems & Embedded C/C++",
            "field": "Core Systems",
            "target_experience": "2-5 Years",
            "duration_minutes": 90,
            "passing_score": 70.0,
            "proctoring_flags": {"strict_tab_monitoring": True, "fullscreen_required": True},
            "category_split": {"Technical Knowledge": 40, "Coding": 50, "Quantitative Aptitude": 10},
            "instructions": "Memory management, POSIX threading, low-level pointer arithmetic, and system call profiling.",
        },
        {
            "id": "WORKPLACE_READINESS",
            "name": "Workplace Communication & Readiness",
            "field": "Engineering Architecture",
            "target_experience": "All Cohorts",
            "duration_minutes": 45,
            "passing_score": 60.0,
            "proctoring_flags": {"strict_tab_monitoring": False, "fullscreen_required": False},
            "category_split": {"English & Communication": 50, "Psychometric": 50},
            "instructions": "Evaluates professional clarity, workplace collaboration, stakeholder communication, and situational composure.",
        },
    ]


@router.post("/questions/import", summary="Import questions via CSV with dry-run support (Phase 3.5)")
def import_questions_csv(
    payload: QuestionImportRequest,
    db: Session = Depends(get_db),
    mentor: User = Depends(require_mentor),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    reader = csv.DictReader(io.StringIO(payload.csv_content.strip()))
    valid_rows = []
    errors = []
    valid_categories = {c.value for c in AssessmentCategory}

    for idx, row in enumerate(reader, 1):
        title = (row.get("title") or "").strip()
        text = (row.get("question_text") or "").strip()
        category = (row.get("category") or "").strip()
        field = (row.get("field") or "General").strip()
        topic = (row.get("topic") or "General").strip()
        difficulty = (row.get("difficulty") or "MEDIUM").strip().upper()
        correct_answer = (row.get("correct_answer") or "").strip()
        raw_options = (row.get("options") or "").strip()

        if not title or not text:
            errors.append(f"Row {idx}: 'title' and 'question_text' are required.")
            continue
        if category not in valid_categories:
            errors.append(f"Row {idx}: Invalid category '{category}'. Must be one of: {sorted(list(valid_categories))}")
            continue

        options = [opt.strip() for opt in raw_options.split("|") if opt.strip()] if raw_options else []
        valid_rows.append({
            "title": title,
            "question_text": text,
            "category": category,
            "field": field,
            "topic": topic,
            "difficulty": difficulty,
            "correct_answer": correct_answer,
            "options": options,
        })

    if not payload.dry_run and valid_rows:
        for item in valid_rows:
            q = QuestionBank(
                author_id=mentor.id,
                title=item["title"],
                question_text=item["question_text"],
                question_type="MCQ" if item["options"] else "SHORT_ANSWER",
                category=item["category"],
                field=item["field"],
                topic=item["topic"],
                difficulty=item["difficulty"],
                is_active=True,
            )
            db.add(q)
            db.flush()
            for seq, opt_text in enumerate(item["options"], 1):
                db.add(McqOption(
                    question_id=q.id,
                    option_text=opt_text,
                    is_correct=(opt_text == item["correct_answer"]),
                    sequence_order=seq,
                ))

    return {
        "dry_run": payload.dry_run,
        "total_parsed": len(valid_rows) + len(errors),
        "valid_count": len(valid_rows),
        "error_count": len(errors),
        "errors": errors,
        "preview": valid_rows[:5],
    }
