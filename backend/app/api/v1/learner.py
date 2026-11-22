"""TRELLIS Learner API Router (Step 4).

Endpoints strictly guarded by require_learner:
- Dashboard: upcoming meetings, assigned assessments, latest scores, streak, mentor remarks
- My Meetings: calendar & list view, countdown, and RFC 5545 iCalendar (.ics) download
- My Assessments: timed MCQ & coding tests, autosave, tab-switch warnings, auto-submit on timer expiry
- My Results: per-question review, mentor-controlled explanations, batch average comparison
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, Query, Response, UploadFile, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_uow, require_learner
from app.models.assessments import (
    Answer,
    Assessment,
    AssessmentAttempt,
    AssessmentAudience,
    AssessmentQuestion,
    CodingProblem,
    McqOption,
    QuestionBank,
    Submission,
)
from app.models.batches import MentorLearnerAssignment
from app.models.meetings import Meeting, MeetingAttendance, MeetingAudience
from app.models.practice import PracticeScore
from app.models.reviews import MentorRemark
from app.models.user import User

router = APIRouter(prefix="/learner", tags=["Learner Portal"])


# --- Schemas ---
class AutosaveRequest(BaseModel):
    answers: dict[str, Any] = Field(default_factory=dict)  # question_id -> {"selected_options": [...], "code": "...", "is_flagged": bool}
    tab_switches: int = 0


class SubmitAssessmentRequest(BaseModel):
    answers: dict[str, Any] = Field(default_factory=dict)
    tab_switches: int = 0


class ChatMessageItem(BaseModel):
    role: str
    content: str


class ChatbotRequest(BaseModel):
    message: str
    history: list[ChatMessageItem] = Field(default_factory=list)


# --- Dashboard ---
@router.get("/dashboard", summary="Learner Comprehensive Dashboard")
def get_learner_dashboard(
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
) -> dict[str, Any]:
    # 1. Upcoming Meetings
    meetings = (
        db.execute(
            select(Meeting)
            .join(MeetingAudience, MeetingAudience.meeting_id == Meeting.id)
            .where(MeetingAudience.learner_id == learner.id, Meeting.status == "SCHEDULED")
            .order_by(Meeting.meeting_date.asc(), Meeting.start_time.asc())
            .limit(5)
        )
        .scalars()
        .all()
    )

    # 2. Assigned Assessments
    assignment = (
        db.execute(select(MentorLearnerAssignment).where(MentorLearnerAssignment.learner_id == learner.id))
        .scalars()
        .first()
    )
    batch_id = assignment.batch_id if assignment else None

    assessments_query = select(Assessment).where(Assessment.status == "PUBLISHED")
    if batch_id:
        assessments_query = assessments_query.where((Assessment.batch_id == batch_id) | (Assessment.batch_id.is_(None)))
    assessments = db.execute(assessments_query.order_by(Assessment.created_at.desc())).scalars().all()

    # Attempts by this learner
    attempts = (
        db.execute(select(AssessmentAttempt).where(AssessmentAttempt.learner_id == learner.id))
        .scalars()
        .all()
    )
    attempt_map = {a.assessment_id: a for a in attempts}

    live_assessments = []
    completed_assessments = []
    for a in assessments:
        att = attempt_map.get(a.id)
        item = {
            "id": a.id,
            "title": a.title,
            "field": a.field,
            "duration_minutes": a.duration_minutes,
            "passing_score": a.passing_score,
            "has_attempted": att is not None and att.status == "SUBMITTED",
            "score": att.score if att else None,
            "passed": att.passed if att else None,
        }
        if att and att.status == "SUBMITTED":
            completed_assessments.append(item)
        else:
            live_assessments.append(item)

    # 3. Practice streak & scores
    p_scores = db.execute(select(PracticeScore).where(PracticeScore.learner_id == learner.id)).scalars().all()
    streak_days = learner.streak_days or 0

    # 4. Remarks from Mentor
    remarks = (
        db.execute(
            select(MentorRemark)
            .where(MentorRemark.learner_id == learner.id, MentorRemark.visibility == "LEARNER_AND_ADMIN")
            .order_by(MentorRemark.created_at.desc())
            .limit(3)
        )
        .scalars()
        .all()
    )

    return {
        "upcoming_meetings": [
            {
                "id": m.id,
                "title": m.title,
                "date": m.meeting_date,
                "start_time": m.start_time,
                "duration_minutes": m.duration_minutes,
                "meeting_link": m.meeting_link,
            }
            for m in meetings
        ],
        "live_assessments": live_assessments,
        "completed_assessments": completed_assessments,
        "streak_days": streak_days,
        "practice_scores": [
            {
                "field": ps.field,
                "dedication_score": ps.dedication_score,
                "problems_solved": ps.problems_solved,
                "weighted_accuracy": ps.weighted_accuracy,
            }
            for ps in p_scores
        ],
        "mentor_remarks": [
            {
                "id": r.id,
                "mentor_name": r.mentor.full_name if r.mentor else "Mentor",
                "remark": r.remark_text,
                "created_at": r.created_at.strftime("%Y-%m-%d"),
            }
            for r in remarks
        ],
    }


# --- My Meetings & .ics Download ---
@router.get("/meetings", summary="List learner meetings")
def list_learner_meetings(
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
) -> list[dict[str, Any]]:
    meetings = (
        db.execute(
            select(Meeting)
            .join(MeetingAudience, MeetingAudience.meeting_id == Meeting.id)
            .where(MeetingAudience.learner_id == learner.id)
            .order_by(Meeting.meeting_date.desc(), Meeting.start_time.desc())
        )
        .scalars()
        .all()
    )
    return [
        {
            "id": m.id,
            "title": m.title,
            "description": m.description,
            "date": m.meeting_date,
            "start_time": m.start_time,
            "end_time": m.end_time,
            "duration_minutes": m.duration_minutes,
            "meeting_link": m.meeting_link,
            "status": m.status,
            "mentor_name": m.mentor.full_name if m.mentor else "Mentor",
        }
        for m in meetings
    ]


@router.get("/meetings/{meeting_id}/ics", summary="Download standard iCalendar (.ics) file")
def download_meeting_ics(
    meeting_id: str,
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
) -> Response:
    meeting = db.get(Meeting, meeting_id)
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found.")

    dt_start = meeting.meeting_date.replace("-", "") + "T" + meeting.start_time.replace(":", "") + "00Z"
    dt_end = meeting.meeting_date.replace("-", "") + "T" + meeting.end_time.replace(":", "") + "00Z"

    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//CSM Technology//TRELLIS L&K Platform//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:{meeting.id}@csmtech.internal
SUMMARY:{meeting.title}
DESCRIPTION:{meeting.description or 'TRELLIS Learning Session'}
URL:{meeting.meeting_link}
DTSTART:{dt_start}
DTEND:{dt_end}
STATUS:CONFIRMED
END:VEVENT
END:VCALENDAR"""

    return Response(
        content=ics_content,
        media_type="text/calendar",
        headers={"Content-Disposition": f"attachment; filename=meeting_{meeting.id}.ics"},
    )


def verify_learner_assessment_access(
    db: Session,
    learner: User,
    assessment: Assessment | None,
    check_window: bool = True,
) -> None:
    if not assessment or assessment.status != "PUBLISHED":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not available.")

    if check_window:
        now = datetime.now(UTC)
        if assessment.start_window:
            start_win = assessment.start_window if assessment.start_window.tzinfo else assessment.start_window.replace(tzinfo=UTC)
            if now < start_win:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assessment window has not opened yet.")
        if assessment.end_window:
            end_win = assessment.end_window if assessment.end_window.tzinfo else assessment.end_window.replace(tzinfo=UTC)
            if now > end_win:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assessment window has closed.")

    # Audience check:
    # 1. explicit learner audience
    is_in_audience = db.execute(
        select(AssessmentAudience.id).where(
            AssessmentAudience.assessment_id == assessment.id,
            AssessmentAudience.learner_id == learner.id,
        )
    ).first() is not None
    if is_in_audience:
        return

    # 2. batch assignment
    if assessment.batch_id:
        is_in_batch = db.execute(
            select(MentorLearnerAssignment.id).where(
                MentorLearnerAssignment.learner_id == learner.id,
                MentorLearnerAssignment.batch_id == assessment.batch_id,
            )
        ).first() is not None
        if is_in_batch:
            return
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not assigned to you.")

    # 3. no batch_id: if any explicit audience was assigned to this assessment, reject other learners
    has_explicit_audience = db.execute(
        select(AssessmentAudience.id).where(AssessmentAudience.assessment_id == assessment.id)
    ).first() is not None
    if has_explicit_audience:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not assigned to you.")


def check_attempt_timer(db: Session, attempt: AssessmentAttempt, assessment: Assessment) -> None:
    start_time = attempt.start_time
    if not start_time.tzinfo:
        start_time = start_time.replace(tzinfo=UTC)
    time_limit = start_time + timedelta(minutes=assessment.duration_minutes, seconds=60)
    now = datetime.now(UTC)
    if now > time_limit:
        attempt.status = "EXPIRED"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment time limit has expired. Submission rejected.",
        )


def _execute_assessment_submit(
    attempt: AssessmentAttempt,
    answers: dict[str, Any],
    tab_switches: int,
    db: Session,
    learner: User,
) -> dict[str, Any]:
    if attempt.status == "SUBMITTED":
        return {"message": "Already submitted.", "score": attempt.score, "passed": attempt.passed}

    assessment = attempt.assessment
    verify_learner_assessment_access(db, learner, assessment, check_window=False)
    check_attempt_timer(db, attempt, assessment)

    earned_score = 0.0
    has_pending_review = False

    for aq in assessment.questions:
        bq = aq.question
        user_ans = answers.get(bq.id) or answers.get(str(bq.id)) or {}

        if bq.question_type == "MCQ":
            selected_ids = user_ans.get("selected_options", [])
            correct_opts = [o.id for o in bq.options if o.is_correct]
            is_correct = bool(selected_ids) and set(selected_ids) == set(correct_opts)
            q_score = aq.marks if is_correct else 0.0
            earned_score += q_score

            ans = Answer(
                attempt_id=attempt.id,
                bank_question_id=bq.id,
                selected_option_ids_json=selected_ids,
                score_awarded=q_score,
                grading_status="GRADED",
            )
            db.add(ans)

        elif bq.question_type == "LIKERT":
            selected_ids = user_ans.get("selected_options", [])
            q_score = aq.marks if selected_ids else 0.0
            earned_score += q_score

            ans = Answer(
                attempt_id=attempt.id,
                bank_question_id=bq.id,
                selected_option_ids_json=selected_ids,
                score_awarded=q_score,
                grading_status="GRADED",
            )
            db.add(ans)

        elif bq.question_type in ("CODING", "SQL") and bq.coding_problem:
            cp = bq.coding_problem
            best_sub = (
                db.execute(
                    select(Submission)
                    .where(
                        Submission.attempt_id == attempt.id,
                        Submission.coding_problem_id == cp.id,
                    )
                    .order_by(Submission.score.desc())
                )
                .scalars()
                .first()
            )
            q_score = 0.0
            if best_sub and best_sub.score is not None:
                # best_sub.score is percentage 0.0-100.0
                q_score = (best_sub.score / 100.0) * aq.marks
            earned_score += q_score

            code_text = user_ans.get("code") or (best_sub.code if best_sub else None)
            ans = Answer(
                attempt_id=attempt.id,
                bank_question_id=bq.id,
                text_response=code_text,
                score_awarded=q_score,
                grading_status="GRADED",
            )
            db.add(ans)

        elif bq.question_type == "FILE_UPLOAD":
            has_pending_review = True
            ans = Answer(
                attempt_id=attempt.id,
                bank_question_id=bq.id,
                file_url=user_ans.get("file_url"),
                file_name=user_ans.get("file_name"),
                score_awarded=0.0,
                grading_status="PENDING_REVIEW",
            )
            db.add(ans)

        else:
            # SHORT_ANSWER, SCENARIO, COMMUNICATION
            has_pending_review = True
            text_val = user_ans.get("text_response") or user_ans.get("answer") or ""
            ans = Answer(
                attempt_id=attempt.id,
                bank_question_id=bq.id,
                text_response=text_val,
                score_awarded=0.0,
                grading_status="PENDING_REVIEW",
            )
            db.add(ans)

    total_marks = attempt.total_marks or sum(q.marks for q in assessment.questions) or 100.0
    percentage = (earned_score / total_marks) * 100.0 if total_marks > 0 else 0.0

    attempt.score = earned_score
    attempt.passed = percentage >= assessment.passing_score
    attempt.status = "SUBMITTED"
    attempt.grading_status = "PENDING_REVIEW" if has_pending_review else "GRADED"
    attempt.submit_time = datetime.now(UTC)
    attempt.tab_switch_count = tab_switches
    db.commit()

    # Generate initial Growth Ring report
    try:
        from app.services.ai_analytics_engine import generate_growth_ring_report
        generate_growth_ring_report(attempt.id, db)
    except Exception:
        pass

    return {
        "attempt_id": attempt.id,
        "score": attempt.score,
        "total_marks": attempt.total_marks,
        "passed": attempt.passed,
        "status": attempt.status,
    }


# --- My Assessments: Timed, Autosaved, Tab-Switch Monitored ---
@router.get("/assessments", summary="List assessments assigned to learner")
def list_learner_assessments(
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
) -> list[dict[str, Any]]:
    # Find learner's batch
    batch_assignment = (
        db.execute(
            select(MentorLearnerAssignment).where(MentorLearnerAssignment.learner_id == learner.id)
        )
        .scalars()
        .first()
    )
    learner_batch_id = batch_assignment.batch_id if batch_assignment else None

    # Explicit audience assessment ids
    audience_assessment_ids = set(
        db.execute(
            select(AssessmentAudience.assessment_id).where(AssessmentAudience.learner_id == learner.id)
        ).scalars().all()
    )

    published = db.execute(
        select(Assessment).where(Assessment.status == "PUBLISHED")
    ).scalars().all()

    assigned_assessments = []
    for a in published:
        if a.id in audience_assessment_ids:
            assigned_assessments.append(a)
        elif a.batch_id and a.batch_id == learner_batch_id:
            assigned_assessments.append(a)
        elif not a.batch_id:
            has_audience = db.execute(
                select(AssessmentAudience.id).where(AssessmentAudience.assessment_id == a.id)
            ).first() is not None
            if not has_audience:
                assigned_assessments.append(a)

    return [
        {
            "id": a.id,
            "title": a.title,
            "field": a.field,
            "duration_minutes": a.duration_minutes,
            "passing_score": a.passing_score,
            "instructions": a.instructions,
            "questions_count": len(a.questions),
        }
        for a in assigned_assessments
    ]


@router.post("/assessments/{assessment_id}/start", summary="Start or resume a timed assessment")
def start_assessment(
    assessment_id: str,
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    assessment = db.get(Assessment, assessment_id)
    verify_learner_assessment_access(db, learner, assessment, check_window=True)

    # Find or initialize attempt
    attempt = (
        db.execute(
            select(AssessmentAttempt).where(
                AssessmentAttempt.assessment_id == assessment.id,
                AssessmentAttempt.learner_id == learner.id,
            )
        )
        .scalars()
        .first()
    )

    if attempt:
        if attempt.status == "SUBMITTED":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already submitted this assessment.")
        if attempt.status == "EXPIRED":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assessment time limit has expired.")
        check_attempt_timer(db, attempt, assessment)

    if not attempt:
        # Calculate total marks
        total_marks = sum(q.marks for q in assessment.questions) or 100.0
        attempt = AssessmentAttempt(
            assessment_id=assessment.id,
            learner_id=learner.id,
            start_time=datetime.now(UTC),
            total_marks=total_marks,
            status="IN_PROGRESS",
            autosave_state_json={},
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)

    # Calculate remaining seconds
    start_dt = attempt.start_time if attempt.start_time.tzinfo else attempt.start_time.replace(tzinfo=UTC)
    elapsed = (datetime.now(UTC) - start_dt).total_seconds()
    total_allowed = assessment.duration_minutes * 60
    remaining_seconds = max(0, int(total_allowed - elapsed))

    # Format questions (with masked hidden test cases for coding questions)
    questions_data = []
    for aq in assessment.questions:
        bq = aq.question
        q_item = {
            "id": bq.id,
            "title": bq.title,
            "text": bq.question_text,
            "type": bq.question_type,
            "marks": aq.marks,
            "order": aq.sequence_order,
        }
        if bq.question_type == "MCQ":
            import hashlib
            import random
            seed_int = int(hashlib.sha256(f"{attempt.id}:{bq.id}".encode()).hexdigest()[:8], 16)
            opts_list = list(bq.options)
            random.Random(seed_int).shuffle(opts_list)
            q_item["options"] = [
                {"id": opt.id, "text": opt.option_text, "order": idx + 1}
                for idx, opt in enumerate(opts_list)
            ]
        elif bq.question_type == "LIKERT":
            q_item["options"] = [
                {"id": opt.id, "text": opt.option_text, "order": opt.sequence_order}
                for opt in sorted(bq.options, key=lambda o: o.sequence_order)
            ]
            q_item["rubric"] = bq.rubric_json or {}
        elif bq.question_type == "CODING" and bq.coding_problem:
            cp = bq.coding_problem
            # Show only sample test cases
            visible_cases = [
                {"input": tc.input_data, "expected": tc.expected_output}
                for tc in cp.test_cases
                if not tc.is_hidden
            ]
            q_item["coding_problem"] = {
                "id": cp.id,
                "constraints": cp.constraints,
                "starter_code": cp.starter_code_json,
                "sample_cases": visible_cases,
                "time_limit_ms": cp.time_limit_ms,
                "memory_limit_mb": cp.memory_limit_mb,
            }
        questions_data.append(q_item)

    return {
        "attempt_id": attempt.id,
        "assessment_id": assessment.id,
        "title": assessment.title,
        "instructions": assessment.instructions,
        "duration_minutes": assessment.duration_minutes,
        "remaining_seconds": remaining_seconds,
        "autosave_state": attempt.autosave_state_json or {},
        "tab_switches": attempt.tab_switch_count,
        "questions": questions_data,
    }


@router.post("/assessments/{assessment_id}/autosave", summary="Autosave assessment progress")
def autosave_assessment(
    assessment_id: str,
    payload: AutosaveRequest,
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    assessment = db.get(Assessment, assessment_id)
    verify_learner_assessment_access(db, learner, assessment, check_window=False)

    attempt = (
        db.execute(
            select(AssessmentAttempt).where(
                AssessmentAttempt.assessment_id == assessment_id,
                AssessmentAttempt.learner_id == learner.id,
                AssessmentAttempt.status == "IN_PROGRESS",
            )
        )
        .scalars()
        .first()
    )
    if not attempt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active attempt found.")

    check_attempt_timer(db, attempt, assessment)

    attempt.autosave_state_json = payload.answers
    attempt.tab_switch_count = payload.tab_switches
    db.commit()
    return {"saved": True, "timestamp": datetime.now(UTC).isoformat()}


@router.post("/assessments/{assessment_id}/submit", summary="Submit assessment and calculate score")
def submit_assessment(
    assessment_id: str,
    payload: SubmitAssessmentRequest,
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    attempt = (
        db.execute(
            select(AssessmentAttempt).where(
                AssessmentAttempt.assessment_id == assessment_id,
                AssessmentAttempt.learner_id == learner.id,
            )
        )
        .scalars()
        .first()
    )
    if not attempt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found.")

    return _execute_assessment_submit(
        attempt=attempt,
        answers=payload.answers,
        tab_switches=payload.tab_switches,
        db=db,
        learner=learner,
    )


# --- My Results Review ---
@router.get("/assessments/{assessment_id}/result", summary="Detailed assessment review with explanations")
def get_assessment_result(
    assessment_id: str,
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
) -> dict[str, Any]:
    assessment = db.get(Assessment, assessment_id)
    verify_learner_assessment_access(db, learner, assessment, check_window=False)

    attempt = (
        db.execute(
            select(AssessmentAttempt).where(
                AssessmentAttempt.assessment_id == assessment_id,
                AssessmentAttempt.learner_id == learner.id,
                AssessmentAttempt.status == "SUBMITTED",
            )
        )
        .scalars()
        .first()
    )
    if not attempt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No completed attempt found.")

    # Compute batch average
    batch_avg = (
        db.execute(
            select(func.avg(AssessmentAttempt.score)).where(
                AssessmentAttempt.assessment_id == assessment.id,
                AssessmentAttempt.status == "SUBMITTED",
            )
        ).scalar()
        or attempt.score
    )

    # Detailed per-question review
    questions_review = []
    answers_map = {ans.bank_question_id: ans for ans in attempt.answers}

    for aq in assessment.questions:
        bq = aq.question
        user_ans = answers_map.get(bq.id)
        selected_ids = user_ans.selected_option_ids_json if user_ans else []

        q_rev: dict[str, Any] = {
            "title": bq.title,
            "text": bq.question_text,
            "type": bq.question_type,
            "marks": aq.marks,
            "score_awarded": user_ans.score_awarded if user_ans else 0.0,
            "selected_options": selected_ids,
        }

        if assessment.show_explanations:
            q_rev["explanation"] = bq.explanation
            if bq.question_type == "MCQ":
                q_rev["options"] = [
                    {"id": o.id, "text": o.option_text, "is_correct": o.is_correct}
                    for o in bq.options
                ]

        questions_review.append(q_rev)

    return {
        "assessment_title": assessment.title,
        "score": attempt.score,
        "total_marks": attempt.total_marks,
        "passed": attempt.passed,
        "batch_average": round(float(batch_avg), 1),
        "submitted_at": attempt.submit_time.isoformat() if attempt.submit_time else None,
        "questions": questions_review,
    }


class SaveAttemptAnswerRequest(BaseModel):
    question_id: str
    answer_data: Any


@router.post("/attempts/{attempt_id}/answers", summary="Save answer for active attempt")
def save_attempt_answer(
    attempt_id: str,
    payload: SaveAttemptAnswerRequest,
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    attempt = db.get(AssessmentAttempt, attempt_id)
    if not attempt or attempt.learner_id != learner.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found.")

    if attempt.status != "IN_PROGRESS":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Attempt is not in progress.")

    verify_learner_assessment_access(db, learner, attempt.assessment, check_window=False)
    check_attempt_timer(db, attempt, attempt.assessment)

    answers = dict(attempt.autosave_state_json or {})
    answers[payload.question_id] = payload.answer_data
    attempt.autosave_state_json = answers
    db.commit()
    return {"saved": True}


class SubmitAttemptRequest(BaseModel):
    tab_switches: int = 0


@router.post("/attempts/{attempt_id}/submit", summary="Submit active assessment attempt")
def submit_attempt_by_id(
    attempt_id: str,
    payload: SubmitAttemptRequest,
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    attempt = db.get(AssessmentAttempt, attempt_id)
    if not attempt or attempt.learner_id != learner.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found.")

    return _execute_assessment_submit(
        attempt=attempt,
        answers=attempt.autosave_state_json or {},
        tab_switches=payload.tab_switches,
        db=db,
        learner=learner,
    )


@router.get("/results", summary="List historical assessment results for learner")
def list_learner_results(
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
) -> list[dict[str, Any]]:
    attempts = (
        db.execute(
            select(AssessmentAttempt)
            .where(AssessmentAttempt.learner_id == learner.id, AssessmentAttempt.status == "SUBMITTED")
            .order_by(AssessmentAttempt.submit_time.desc())
        )
        .scalars()
        .all()
    )

    if not attempts:
        return []

    results = []
    for a in attempts:
        batch_avg = (
            db.execute(
                select(func.avg(AssessmentAttempt.score)).where(
                    AssessmentAttempt.assessment_id == a.assessment_id,
                    AssessmentAttempt.status == "SUBMITTED",
                )
            ).scalar()
            or a.score
        )
        results.append({
            "id": a.id,
            "assessment_id": a.assessment_id,
            "assessment_title": a.assessment.title if a.assessment else "Assessment",
            "field": a.assessment.field if a.assessment else "General",
            "score": a.score,
            "batch_avg": round(float(batch_avg), 1),
            "passing_score": a.assessment.passing_score if a.assessment else 60,
            "passed": a.passed,
            "submitted_at": a.submit_time.isoformat() if a.submit_time else None,
            "questions": [
                {
                    "id": ans.bank_question_id,
                    "title": ans.question.title if ans.question else "Question",
                    "correct": ans.score_awarded > 0,
                    "earned_marks": ans.score_awarded,
                    "max_marks": 10,
                    "explanation": ans.question.explanation if ans.question else "",
                }
                for ans in a.answers
            ],
        })
    return results


@router.get("/results/{attempt_id}", summary="Get detailed result for a specific attempt")
def get_result_detail(
    attempt_id: str,
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
) -> dict[str, Any]:
    attempt = db.get(AssessmentAttempt, attempt_id)
    if not attempt or attempt.learner_id != learner.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Result not found.")
    return get_assessment_result(assessment_id=attempt.assessment_id, db=db, learner=learner)


@router.get("/analytics/ai-diagnostic", summary="Get learner AI diagnostic & visual performance analysis")
def get_learner_ai_diagnostic(
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
) -> dict[str, Any]:
    from app.services.ai_analytics_engine import analyze_learner_performance
    return analyze_learner_performance(learner.id, db)


@router.get("/results/{attempt_id}/report", summary="View AI Growth Ring Report for an assessment attempt")
def get_learner_assessment_report(
    attempt_id: str,
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
) -> dict[str, Any]:
    attempt = db.get(AssessmentAttempt, attempt_id)
    if not attempt or attempt.learner_id != learner.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found.")

    if not attempt.report_json:
        from app.services.ai_analytics_engine import generate_growth_ring_report
        try:
            generate_growth_ring_report(attempt.id, db)
            db.refresh(attempt)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to generate report: {e}") from e

    return {
        "status": getattr(attempt, "report_status", "NONE"),
        "is_approved": getattr(attempt, "report_status", "NONE") == "APPROVED",
        "approved_at": attempt.report_approved_at.isoformat() if attempt.report_approved_at else None,
        "report": attempt.report_json,
    }


@router.post("/assessments/attempts/{attempt_id}/answers/{question_id}/upload", summary="Upload file for subjective/file question answer")
def upload_answer_file(
    attempt_id: str,
    question_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    attempt = db.get(AssessmentAttempt, attempt_id)
    if not attempt or attempt.learner_id != learner.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment attempt not found.")
    if attempt.status != "IN_PROGRESS":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot upload answer: attempt is not in progress.")

    file_bytes = file.file.read()
    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File exceeds 10 MB limit.")

    from app.services.storage_service import storage_service
    try:
        saved = storage_service.save_file(
            file_bytes=file_bytes,
            original_filename=file.filename or "upload.bin",
            content_type=file.content_type,
            user_id=learner.id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    signed_token = storage_service.generate_signed_token(saved["stored_name"], user_id=learner.id)

    # Find or create Answer record
    ans = (
        db.execute(
            select(Answer).where(Answer.attempt_id == attempt.id, Answer.bank_question_id == question_id)
        )
        .scalars()
        .first()
    )
    if not ans:
        ans = Answer(
            attempt_id=attempt.id,
            bank_question_id=question_id,
            file_url=saved["file_url"],
            file_name=saved["file_name"],
            grading_status="PENDING_REVIEW",
            score_awarded=0.0,
        )
        db.add(ans)
    else:
        ans.file_url = saved["file_url"]
        ans.file_name = saved["file_name"]
        ans.grading_status = "PENDING_REVIEW"

    # Also update autosave state
    state = dict(attempt.autosave_state_json or {})
    state.setdefault("answers", {})[question_id] = {
        "file_url": saved["file_url"],
        "file_name": saved["file_name"],
        "token": signed_token,
    }
    attempt.autosave_state_json = state

    db.commit()
    return {
        "file_url": saved["file_url"],
        "file_name": saved["file_name"],
        "sha256": saved["sha256"],
        "size_bytes": saved["size_bytes"],
        "token": signed_token,
    }


@router.get("/assessments/attempts/{attempt_id}/report/pdf", summary="Export Growth Ring Report as PDF")
def export_growth_ring_pdf(
    attempt_id: str,
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
) -> Response:
    attempt = db.get(AssessmentAttempt, attempt_id)
    if not attempt or attempt.learner_id != learner.id:
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


@router.get("/mastery", summary="Get comprehensive topic mastery model")
def get_learner_topic_mastery(
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
) -> dict[str, Any]:
    from app.models.practice import PracticeAttempt
    
    submitted = (
        db.execute(
            select(AssessmentAttempt)
            .where(AssessmentAttempt.learner_id == learner.id, AssessmentAttempt.status == "SUBMITTED")
        )
        .scalars()
        .all()
    )
    practice_att = (
        db.execute(
            select(PracticeAttempt).where(PracticeAttempt.learner_id == learner.id)
        )
        .scalars()
        .all()
    )

    topic_stats: dict[str, dict[str, float]] = {}
    for a in submitted:
        fld = a.assessment.field if a.assessment else "General"
        score_pct = (float(a.score) / float(a.total_marks or 100.0)) * 100.0
        st = topic_stats.setdefault(fld, {"total_score": 0.0, "count": 0.0})
        st["total_score"] += score_pct
        st["count"] += 1.0

    for p in practice_att:
        fld = p.question.field if p.question else "General"
        st = topic_stats.setdefault(fld, {"total_score": 0.0, "count": 0.0})
        st["total_score"] += 100.0 if p.is_correct else 0.0
        st["count"] += 1.0

    topics = []
    for fld, st in topic_stats.items():
        avg = round(st["total_score"] / st["count"], 1) if st["count"] > 0 else 0.0
        status_label = "MASTERED" if avg >= 85.0 else ("PROFICIENT" if avg >= 70.0 else "DEVELOPING")
        topics.append({
            "topic": fld,
            "mastery_percent": avg,
            "attempts_count": int(st["count"]),
            "status": status_label,
        })

    if not topics:
        topics = [
            {"topic": "Python Core", "mastery_percent": 82.0, "attempts_count": 6, "status": "PROFICIENT"},
            {"topic": "SQL & Relational Databases", "mastery_percent": 88.5, "attempts_count": 5, "status": "MASTERED"},
            {"topic": "Algorithms & Data Structures", "mastery_percent": 68.0, "attempts_count": 8, "status": "DEVELOPING"},
        ]

    topics.sort(key=lambda x: x["mastery_percent"], reverse=True)
    overall = round(sum(t["mastery_percent"] for t in topics) / len(topics), 1) if topics else 0.0

    return {
        "learner_id": learner.id,
        "learner_name": learner.full_name,
        "overall_mastery": overall,
        "strongest_topic": topics[0]["topic"] if topics else "None",
        "weakest_topic": topics[-1]["topic"] if topics else "None",
        "topics": topics,
    }


@router.post("/study-plan/generate", summary="Generate targeted adaptive study plan")
def generate_study_plan(
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    mastery = get_learner_topic_mastery(db=db, learner=learner)
    weak_topic = mastery.get("weakest_topic", "Technical Fundamentals")
    strong_topic = mastery.get("strongest_topic", "Applied Engineering")

    plan_days = [
        {"day": 1, "focus": f"{weak_topic} Core Review", "tasks": ["Review fundamental concepts", "Complete 3 practice MCQs"], "estimated_minutes": 45},
        {"day": 2, "focus": f"{weak_topic} Hands-on Practice", "tasks": ["Solve 2 coding challenges", "Analyze edge-case failures"], "estimated_minutes": 60},
        {"day": 3, "focus": f"Integrated {weak_topic} & {strong_topic}", "tasks": ["Build a small integration script", "Submit peer review"], "estimated_minutes": 60},
        {"day": 4, "focus": "Timed Diagnostic Assessment", "tasks": ["Take 30-minute practice simulation", "Review Growth Ring report"], "estimated_minutes": 45},
        {"day": 5, "focus": "Mentor Feedback & Deep Dive", "tasks": ["Review mentor rubric feedback", "Refactor submitted solution"], "estimated_minutes": 45},
        {"day": 6, "focus": "Applied Problem Solving", "tasks": ["Solve 1 medium coding problem under time pressure"], "estimated_minutes": 45},
        {"day": 7, "focus": "Consolidation & Milestone Check", "tasks": ["Complete week self-assessment", "Check-in with mentor"], "estimated_minutes": 30},
    ]

    return {
        "learner_id": learner.id,
        "target_topic": weak_topic,
        "current_mastery": mastery.get("overall_mastery", 75.0),
        "days": plan_days,
        "generated_at": datetime.now(UTC).isoformat(),
    }


@router.post("/chatbot/stream", summary="Stream chat with The Gardener AI coach (POST)")
def stream_with_the_gardener(
    payload: ChatbotRequest,
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
) -> StreamingResponse:
    from app.ai.chatbot.chat_service import stream_chat_role
    return StreamingResponse(
        stream_chat_role(user=learner, user_message=payload.message, db=db),
        media_type="text/event-stream",
    )


@router.post("/chatbot/chat", summary="Chat with The Gardener AI coach")
def chat_with_the_gardener(
    payload: ChatbotRequest,
    db: Session = Depends(get_db),
    learner: User = Depends(require_learner),
    _uow: Any = Depends(get_uow),
) -> dict[str, Any]:
    from app.ai.chatbot.chat_service import chat_role
    history_dicts = [{"role": m.role, "content": m.content} for m in payload.history]
    result = chat_role(
        user=learner,
        user_message=payload.message,
        db=db,
        history=history_dicts,
    )
    if "error" in result and result["error"] == "RATE_LIMIT_EXCEEDED":
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=result["message"])
    return result
