"""TRELLIS Phase 3 Mentor/Meeting Validation Tests.

Validates:
1. Meeting link URL parsing: requires https scheme and allow-listed host (teams.microsoft.com, meet.google.com, zoom.us, *.csm.tech); rejects javascript:, data:, http:, and unapproved hosts.
2. Schedule validation: end_time > start_time, date not in the past.
3. Conflict detection: detects overlapping time ranges for the same mentor AND for any learner in the audience.
4. Attendance marking: strictly restricted to learners in the meeting audience; rejects others with 400.
5. Talent alert actions:
   - INVITE_ASSESSMENT creates a real assessment_audience row.
   - SCHEDULE_INTERVIEW creates a real Meeting and MeetingAudience row.
   - RECOMMEND_PROMOTION creates an immutable AuditLog record.
   - Repeat actions on a closed alert are blocked.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from fastapi import HTTPException, status
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api.v1.mentor import (
    AlertActionRequest,
    AttendanceItem,
    MarkAttendanceRequest,
    MeetingCreateRequest,
    act_on_talent_alert,
    mark_attendance,
    schedule_meeting,
)
from app.core.config import settings
from app.models import (
    Assessment,
    AssessmentAudience,
    AuditLog,
    Base,
    Batch,
    Meeting,
    MeetingAttendance,
    MeetingAudience,
    MentorLearnerAssignment,
    Organisation,
    TalentAlert,
    User,
)


@pytest.fixture
def p3_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        org = Organisation(name="CSM Technology", code="CSM_P3")
        session.add(org)
        session.flush()

        mentor1 = User(
            id="mentor_p3_1",
            org_id=org.id,
            email="mentor.p3@csm.tech",
            password_hash="hashed_pw",
            full_name="Mentor P3",
            role="MENTOR",
            is_active=True,
        )
        learner1 = User(
            id="learner_p3_1",
            org_id=org.id,
            email="learner1.p3@csm.tech",
            password_hash="hashed_pw",
            full_name="Learner One P3",
            role="LEARNER",
            is_active=True,
        )
        learner2 = User(
            id="learner_p3_2",
            org_id=org.id,
            email="learner2.p3@csm.tech",
            password_hash="hashed_pw",
            full_name="Learner Two P3",
            role="LEARNER",
            is_active=True,
        )
        learner_outsider = User(
            id="learner_p3_outsider",
            org_id=org.id,
            email="outsider.p3@csm.tech",
            password_hash="hashed_pw",
            full_name="Learner Outsider P3",
            role="LEARNER",
            is_active=True,
        )
        session.add_all([mentor1, learner1, learner2, learner_outsider])

        batch1 = Batch(id="batch_p3_1", name="Batch P3", code="BATCH_P3", org_id=org.id)
        session.add(batch1)

        # Mentor assigned to batch1 and learner1 & learner2
        session.add_all([
            MentorLearnerAssignment(mentor_id=mentor1.id, learner_id=learner1.id, batch_id=batch1.id),
            MentorLearnerAssignment(mentor_id=mentor1.id, learner_id=learner2.id, batch_id=batch1.id),
        ])
        session.commit()
        yield session


def test_meeting_url_validation_allows_valid_hosts(p3_db: Session):
    mentor1 = p3_db.get(User, "mentor_p3_1")
    tomorrow = (datetime.now(UTC) + timedelta(days=1)).date().isoformat()

    valid_urls = [
        "https://teams.microsoft.com/l/meetup-join/19%3ameeting",
        "https://meet.google.com/abc-defg-hij",
        "https://zoom.us/j/123456789",
        "https://portal.csm.tech/conferences/room1",
        "https://csm.tech/meeting",
    ]

    for idx, url in enumerate(valid_urls):
        res = schedule_meeting(
            payload=MeetingCreateRequest(
                title=f"Valid Meeting {idx}",
                meeting_date=tomorrow,
                start_time=f"0{idx}:00" if idx < 10 else f"{idx}:00",
                end_time=f"0{idx}:30" if idx < 10 else f"{idx}:30",
                duration_minutes=30,
                meeting_link=url,
                learner_ids=["learner_p3_1"],
            ),
            db=p3_db,
            mentor=mentor1,
            _uow=None,
        )
        assert res["title"] == f"Valid Meeting {idx}"


def test_meeting_url_validation_rejects_unsafe_protocols_and_domains(p3_db: Session):
    mentor1 = p3_db.get(User, "mentor_p3_1")
    tomorrow = (datetime.now(UTC) + timedelta(days=1)).date().isoformat()

    invalid_urls = [
        "javascript:alert(1)",
        "data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==",
        "http://meet.google.com/insecure",
        "https://evil-phishing-site.com/login",
        "https://zoom.fake.org/meeting",
    ]

    for url in invalid_urls:
        with pytest.raises(HTTPException) as exc_info:
            schedule_meeting(
                payload=MeetingCreateRequest(
                    title="Suspicious Meeting",
                    meeting_date=tomorrow,
                    start_time="10:00",
                    end_time="11:00",
                    duration_minutes=60,
                    meeting_link=url,
                    learner_ids=["learner_p3_1"],
                ),
                db=p3_db,
                mentor=mentor1,
                _uow=None,
            )
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST


def test_schedule_validates_date_not_in_past_and_time_ordering(p3_db: Session):
    mentor1 = p3_db.get(User, "mentor_p3_1")
    yesterday = (datetime.now(UTC) - timedelta(days=1)).date().isoformat()
    tomorrow = (datetime.now(UTC) + timedelta(days=1)).date().isoformat()

    # Past date
    with pytest.raises(HTTPException) as exc_info1:
        schedule_meeting(
            payload=MeetingCreateRequest(
                title="Past Meeting",
                meeting_date=yesterday,
                start_time="10:00",
                end_time="11:00",
                duration_minutes=60,
                meeting_link="https://meet.google.com/test",
                learner_ids=["learner_p3_1"],
            ),
            db=p3_db,
            mentor=mentor1,
            _uow=None,
        )
    assert exc_info1.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "past" in exc_info1.value.detail.lower()

    # end_time <= start_time
    with pytest.raises(HTTPException) as exc_info2:
        schedule_meeting(
            payload=MeetingCreateRequest(
                title="Backward Time Meeting",
                meeting_date=tomorrow,
                start_time="11:00",
                end_time="10:00",
                duration_minutes=60,
                meeting_link="https://meet.google.com/test",
                learner_ids=["learner_p3_1"],
            ),
            db=p3_db,
            mentor=mentor1,
            _uow=None,
        )
    assert exc_info2.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "after" in exc_info2.value.detail.lower()


def test_meeting_conflict_detection_mentor_and_learner(p3_db: Session):
    mentor1 = p3_db.get(User, "mentor_p3_1")
    tomorrow = (datetime.now(UTC) + timedelta(days=1)).date().isoformat()

    # Schedule base meeting: 10:00 - 11:30 with learner1
    schedule_meeting(
        payload=MeetingCreateRequest(
            title="Base Meeting",
            meeting_date=tomorrow,
            start_time="10:00",
            end_time="11:30",
            duration_minutes=90,
            meeting_link="https://meet.google.com/base-meeting",
            learner_ids=["learner_p3_1"],
        ),
        db=p3_db,
        mentor=mentor1,
        _uow=None,
    )

    # 1. Overlapping meeting for SAME mentor (11:00 - 12:00) with learner2
    with pytest.raises(HTTPException) as exc_mentor_conflict:
        schedule_meeting(
            payload=MeetingCreateRequest(
                title="Conflicting Mentor Meeting",
                meeting_date=tomorrow,
                start_time="11:00",
                end_time="12:00",
                duration_minutes=60,
                meeting_link="https://meet.google.com/conflict1",
                learner_ids=["learner_p3_2"],
            ),
            db=p3_db,
            mentor=mentor1,
            _uow=None,
        )
    assert exc_mentor_conflict.value.status_code == status.HTTP_409_CONFLICT
    assert "conflict" in exc_mentor_conflict.value.detail.lower()

    # Create a second mentor assigned to learner1
    mentor2 = User(
        id="mentor_p3_2",
        org_id=mentor1.org_id,
        email="mentor2.p3@csm.tech",
        password_hash="hashed_pw",
        full_name="Mentor Two P3",
        role="MENTOR",
        is_active=True,
    )
    p3_db.add(mentor2)
    p3_db.add(MentorLearnerAssignment(mentor_id=mentor2.id, learner_id="learner_p3_1"))
    p3_db.commit()

    # 2. Mentor2 tries to schedule with learner1 during overlapping time (10:30 - 11:00)
    with pytest.raises(HTTPException) as exc_learner_conflict:
        schedule_meeting(
            payload=MeetingCreateRequest(
                title="Mentor2 Meeting with Learner1",
                meeting_date=tomorrow,
                start_time="10:30",
                end_time="11:00",
                duration_minutes=30,
                meeting_link="https://meet.google.com/mentor2-meeting",
                learner_ids=["learner_p3_1"],
            ),
            db=p3_db,
            mentor=mentor2,
            _uow=None,
        )
    assert exc_learner_conflict.value.status_code == status.HTTP_409_CONFLICT
    assert "learner" in exc_learner_conflict.value.detail.lower()


def test_mark_attendance_rejects_non_audience_learner(p3_db: Session):
    mentor1 = p3_db.get(User, "mentor_p3_1")
    tomorrow = (datetime.now(UTC) + timedelta(days=1)).date().isoformat()

    meeting = Meeting(
        title="Audience Specific Meeting",
        meeting_date=tomorrow,
        start_time="14:00",
        end_time="15:00",
        duration_minutes=60,
        meeting_link="https://meet.google.com/attendance-test",
        mentor_id=mentor1.id,
        status="SCHEDULED",
    )
    p3_db.add(meeting)
    p3_db.flush()
    p3_db.add(MeetingAudience(meeting_id=meeting.id, learner_id="learner_p3_1"))
    p3_db.commit()

    # Marking attendance for learner1 succeeds
    res = mark_attendance(
        meeting_id=meeting.id,
        payload=MarkAttendanceRequest(
            attendances=[AttendanceItem(learner_id="learner_p3_1", attended=True, remarks="Active")]
        ),
        db=p3_db,
        mentor=mentor1,
        _uow=None,
    )
    assert res["message"] == "Attendance recorded."

    # Marking attendance for learner_outsider (not in audience) is rejected with 400
    with pytest.raises(HTTPException) as exc_info:
        mark_attendance(
            meeting_id=meeting.id,
            payload=MarkAttendanceRequest(
                attendances=[AttendanceItem(learner_id="learner_p3_outsider", attended=True)]
            ),
            db=p3_db,
            mentor=mentor1,
            _uow=None,
        )
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "not in the audience" in exc_info.value.detail.lower()


def test_talent_alert_actions_persistence_and_closed_lock(p3_db: Session):
    mentor1 = p3_db.get(User, "mentor_p3_1")
    learner1 = p3_db.get(User, "learner_p3_1")

    # Create published assessment for invite testing
    assessment = Assessment(
        mentor_id=mentor1.id,
        title="Elite Spotlight Assessment",
        field="Python",
        duration_minutes=45,
        passing_score=80.0,
        status="PUBLISHED",
        version=1,
    )
    p3_db.add(assessment)
    p3_db.flush()

    alert1 = TalentAlert(
        mentor_id=mentor1.id,
        learner_id=learner1.id,
        field="Python",
        evidence_json={"accuracy": 98.0, "streak": 15},
        status="PENDING",
    )
    alert2 = TalentAlert(
        mentor_id=mentor1.id,
        learner_id=learner1.id,
        field="Python",
        evidence_json={"accuracy": 95.0, "streak": 12},
        status="PENDING",
    )
    alert3 = TalentAlert(
        mentor_id=mentor1.id,
        learner_id=learner1.id,
        field="Python",
        evidence_json={"accuracy": 99.0, "streak": 20},
        status="PENDING",
    )
    p3_db.add_all([alert1, alert2, alert3])
    p3_db.commit()

    # 1. INVITE_ASSESSMENT: Must create a real AssessmentAudience row
    act_on_talent_alert(
        alert_id=alert1.id,
        payload=AlertActionRequest(
            action="INVITE_ASSESSMENT",
            assessment_id=assessment.id,
            notes="Invited to elite test.",
        ),
        db=p3_db,
        mentor=mentor1,
        _uow=None,
    )
    aud = p3_db.execute(
        select(AssessmentAudience).where(
            AssessmentAudience.assessment_id == assessment.id,
            AssessmentAudience.learner_id == learner1.id,
        )
    ).first()
    assert aud is not None
    p3_db.refresh(alert1)
    assert alert1.status == "INVITE_ASSESSMENT"

    # Repeat action on closed alert1 must be blocked!
    with pytest.raises(HTTPException) as exc_blocked:
        act_on_talent_alert(
            alert_id=alert1.id,
            payload=AlertActionRequest(action="DISMISSED"),
            db=p3_db,
            mentor=mentor1,
            _uow=None,
        )
    assert exc_blocked.value.status_code in (status.HTTP_409_CONFLICT, status.HTTP_400_BAD_REQUEST)
    assert "already closed" in exc_blocked.value.detail.lower()

    # 2. SCHEDULE_INTERVIEW: Must create a real Meeting and MeetingAudience row
    tomorrow = (datetime.now(UTC) + timedelta(days=1)).date().isoformat()
    act_on_talent_alert(
        alert_id=alert2.id,
        payload=AlertActionRequest(
            action="SCHEDULE_INTERVIEW",
            meeting_date=tomorrow,
            start_time="15:00",
            end_time="16:00",
            meeting_link="https://meet.google.com/talent-interview-room",
            notes="Technical milestone review interview.",
        ),
        db=p3_db,
        mentor=mentor1,
        _uow=None,
    )
    created_meeting = p3_db.execute(
        select(Meeting).where(Meeting.meeting_link == "https://meet.google.com/talent-interview-room")
    ).scalars().first()
    assert created_meeting is not None
    m_aud = p3_db.execute(
        select(MeetingAudience).where(
            MeetingAudience.meeting_id == created_meeting.id,
            MeetingAudience.learner_id == learner1.id,
        )
    ).first()
    assert m_aud is not None

    # 3. RECOMMEND_PROMOTION: Must persist a record visible to admin in AuditLog
    act_on_talent_alert(
        alert_id=alert3.id,
        payload=AlertActionRequest(
            action="RECOMMEND_PROMOTION",
            notes="Recommendation for Senior Trainee promotion based on consistent 99% accuracy.",
        ),
        db=p3_db,
        mentor=mentor1,
        _uow=None,
    )
    audit_rec = p3_db.execute(
        select(AuditLog).where(
            AuditLog.action == "RECOMMEND_PROMOTION",
            AuditLog.resource_id == alert3.id,
        )
    ).scalars().first()
    assert audit_rec is not None
    assert audit_rec.actor_id == mentor1.id
    assert audit_rec.after_state_json["learner_id"] == learner1.id
