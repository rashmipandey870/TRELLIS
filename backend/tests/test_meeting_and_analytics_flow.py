"""Automated tests verifying meeting scheduling form flow and graphical analytics endpoints."""

from datetime import UTC, datetime, timedelta
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.api.v1.admin import get_cohort_intelligence
from app.api.v1.learner import (
    download_meeting_ics,
    get_learner_ai_diagnostic,
    get_learner_dashboard,
    list_learner_meetings,
)
from app.api.v1.mentor import (
    MeetingCreateRequest,
    get_assessment_analysis,
    get_mentor_batches,
    list_mentor_meetings,
    schedule_meeting,
)
from app.models import (
    Answer,
    Assessment,
    AssessmentAttempt,
    AssessmentAudience,
    Batch,
    Meeting,
    MeetingAudience,
    MentorLearnerAssignment,
    Organisation,
    User,
)


@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:", echo=False)
    from app.models.base import Base
    Base.metadata.create_all(engine)
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def test_meeting_schedule_form_flow(test_db: Session):
    """Verify meeting schedule form works with ISO datetimes, platform links, and audience tracking."""
    # 1. Setup organization, mentor, batch, and learner
    org = Organisation(name="CSM Technologies", code="CSM-TEST")
    test_db.add(org)
    test_db.flush()

    mentor = User(
        org_id=org.id,
        email="mentor.lead@csmtech.internal",
        password_hash="dummy_hash_123",
        full_name="Lead Cloud Mentor",
        role="MENTOR",
        is_active=True,
    )
    learner = User(
        org_id=org.id,
        email="learner.test@csmtech.internal",
        password_hash="dummy_hash_123",
        full_name="Test Student",
        role="LEARNER",
        is_active=True,
    )
    test_db.add_all([mentor, learner])
    test_db.flush()

    batch = Batch(name="Batch Test", code="BATCH_TEST", org_id=org.id)
    test_db.add(batch)
    test_db.flush()

    assignment = MentorLearnerAssignment(
        mentor_id=mentor.id,
        learner_id=learner.id,
        batch_id=batch.id,
    )
    test_db.add(assignment)
    test_db.commit()

    # 2. Verify mentor can list their assigned batches dynamically
    mentor_batches = get_mentor_batches(db=test_db, mentor=mentor)
    assert len(mentor_batches) == 1
    assert mentor_batches[0]["name"] == "Batch Test"

    # 3. Test meeting schedule submission using datetime-local format (with 'T')
    tomorrow = datetime.now(UTC) + timedelta(days=1)
    payload_dict = {
        "title": "Architecture Review & Sandboxing Lab",
        "description": "Interactive code review session",
        "meeting_link": "https://teams.microsoft.com/l/meetup-join/csm-session-123",
        "start_time": f"{tomorrow.strftime('%Y-%m-%d')}T14:00",
        "end_time": f"{tomorrow.strftime('%Y-%m-%d')}T15:00",
        "batch_id": batch.id,
        "learner_ids": [learner.id],
    }

    req = MeetingCreateRequest(**payload_dict)
    assert req.meeting_date == tomorrow.strftime("%Y-%m-%d")
    assert req.start_time == "14:00"
    assert req.end_time == "15:00"

    result = schedule_meeting(payload=req, db=test_db, mentor=mentor, _uow=None)
    assert result["title"] == "Architecture Review & Sandboxing Lab"
    assert result["status"] == "SCHEDULED"

    # 4. Verify meeting appears in mentor meetings list with direct join link
    m_list = list_mentor_meetings(db=test_db, mentor=mentor)
    assert len(m_list) == 1
    assert m_list[0]["meeting_link"] == "https://teams.microsoft.com/l/meetup-join/csm-session-123"

    # 5. Verify learner sees meeting on their dashboard and meetings list
    l_dashboard = get_learner_dashboard(db=test_db, learner=learner)
    assert len(l_dashboard["upcoming_meetings"]) == 1
    assert l_dashboard["upcoming_meetings"][0]["meeting_link"] == "https://teams.microsoft.com/l/meetup-join/csm-session-123"

    l_meetings = list_learner_meetings(db=test_db, learner=learner)
    assert len(l_meetings) == 1
    assert l_meetings[0]["title"] == "Architecture Review & Sandboxing Lab"

    # 6. Verify iCalendar (.ics) download returns valid standard RFC 5545 calendar file
    ics_resp = download_meeting_ics(meeting_id=result["id"], db=test_db, learner=learner)
    assert ics_resp.status_code == 200
    assert "BEGIN:VCALENDAR" in ics_resp.body.decode()
    assert "https://teams.microsoft.com/l/meetup-join/csm-session-123" in ics_resp.body.decode()


def test_graphical_analytics_endpoints(test_db: Session):
    """Verify graphical SVG analysis reports return valid vectors for Learner and Admin."""
    org = Organisation(name="CSM Technologies", code="CSM-ANALYTICS")
    test_db.add(org)
    test_db.flush()

    admin = User(org_id=org.id, email="admin.test@csmtech.internal", password_hash="dummy_hash_123", full_name="Admin User", role="ADMIN", is_active=True)
    mentor = User(org_id=org.id, email="mentor.analytics@csmtech.internal", password_hash="dummy_hash_123", full_name="Analytics Mentor", role="MENTOR", is_active=True)
    learner = User(org_id=org.id, email="learner.analytics@csmtech.internal", password_hash="dummy_hash_123", full_name="Analytics Student", role="LEARNER", is_active=True)
    test_db.add_all([admin, mentor, learner])
    test_db.flush()

    # Create assessment attempts with scores
    assessment = Assessment(
        mentor_id=mentor.id,
        title="Python Algorithms & Architecture",
        field="Python",
        duration_minutes=60,
        passing_score=75,
        status="PUBLISHED",
    )
    test_db.add(assessment)
    test_db.flush()

    attempt = AssessmentAttempt(
        assessment_id=assessment.id,
        learner_id=learner.id,
        score=88.0,
        total_marks=100.0,
        status="SUBMITTED",
        submit_time=datetime.now(UTC),
    )
    test_db.add(attempt)
    test_db.commit()

    # 1. Learner AI Diagnostic
    l_diag = get_learner_ai_diagnostic(db=test_db, learner=learner)
    assert "charts" in l_diag
    assert "<svg" in l_diag["charts"]["bell_curve_svg"]
    assert "<svg" in l_diag["charts"]["competency_bar_svg"]

    # 2. Admin Cohort Intelligence
    admin_intel = get_cohort_intelligence(db=test_db, _admin=admin)
    assert admin_intel["total_submissions"] >= 1
    assert "<svg" in admin_intel["charts"]["cohort_bell_curve_svg"]
    assert "<svg" in admin_intel["charts"]["competency_bar_svg"]
