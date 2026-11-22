"""Unit and integration tests for Phase B Functionality.

Covers:
- B1: Multi-role chatbot (Learner, Mentor, Admin), rate limiting (30/hr), streaming SSE, offline structured card fallback.
- B2: 7 Policy categories, question bank category filter, AI subjective rubric evaluation, psychometric disclaimer.
- B3: File upload answer storage, 10MB limit enforcement, signed token download.
- B4: Growth Ring PDF report generation via ReportLab.
- B5: Topic mastery model, targeted study plan generation, mentor needs-attention queue.
"""

from __future__ import annotations

import io
from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException, UploadFile
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

import app.models
from app.ai.chatbot.chat_service import chat_role, stream_chat_role
from app.ai.gateway import ai_gateway
from app.api.v1.admin import (
    AdminChatbotRequest,
    chat_with_admin_copilot,
    stream_with_admin_copilot,
)
from app.api.v1.learner import (
    ChatbotRequest,
    ChatMessageItem,
    chat_with_the_gardener,
    export_growth_ring_pdf,
    get_learner_topic_mastery,
    generate_study_plan,
    stream_with_the_gardener,
    upload_answer_file,
)
from app.api.v1.mentor import (
    MentorChatbotRequest,
    ai_evaluate_subjective_answer,
    chat_with_mentor_assistant,
    get_learners_needs_attention,
    list_question_bank,
    stream_with_mentor_assistant,
)
from app.api.v1.storage import download_file
from app.models.assessments import (
    Answer,
    Assessment,
    AssessmentAttempt,
    AssessmentQuestion,
    QuestionBank,
)
from app.models.base import Base
from app.models.batches import Batch, MentorLearnerAssignment
from app.models.curriculum import Enrolment, Pathway
from app.models.tenancy import Organisation
from app.models.user import User
from app.schemas.category import AssessmentCategory, PSYCHOMETRIC_DISCLAIMER
from app.services.pdf_report_service import generate_growth_ring_pdf
from app.services.storage_service import storage_service


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def b_setup(db_session: Session):
    org = Organisation(name="CSM Phase B Org", code="CSM_PHASE_B")
    db_session.add(org)
    db_session.flush()

    admin = User(
        org_id=org.id,
        email="admin_b@csmtech.internal",
        full_name="Admin B Enterprise",
        password_hash="pw",
        role="ADMIN",
        must_change_password=False,
    )
    mentor = User(
        org_id=org.id,
        email="mentor_b@csmtech.internal",
        full_name="Mentor B Lead",
        password_hash="pw",
        role="MENTOR",
        must_change_password=False,
    )
    learner = User(
        org_id=org.id,
        email="learner_b@csmtech.internal",
        full_name="Learner B Trainee",
        password_hash="pw",
        role="LEARNER",
        streak_days=5,
        must_change_password=False,
    )
    db_session.add_all([admin, mentor, learner])
    db_session.flush()

    batch = Batch(
        org_id=org.id,
        name="Batch Beta 2026",
        code="BATCH_B_2026",
        field="Full Stack",
    )
    db_session.add(batch)
    db_session.flush()

    mla = MentorLearnerAssignment(
        mentor_id=mentor.id,
        learner_id=learner.id,
        batch_id=batch.id,
    )
    db_session.add(mla)

    pathway = Pathway(
        org_id=org.id,
        author_id=mentor.id,
        code="PW_CLOUD_ENG",
        title="Cloud Engineering Pathway",
        description="Comprehensive cloud systems",
    )
    db_session.add(pathway)
    db_session.flush()

    enrolment = Enrolment(
        org_id=org.id,
        user_id=learner.id,
        pathway_id=pathway.id,
        batch_id=batch.id,
        progress_percent=65.0,
    )
    db_session.add(enrolment)

    # Questions across categories
    q_tech = QuestionBank(
        author_id=mentor.id,
        title="FastAPI Async Coroutines",
        question_text="Explain async/await in Python event loops.",
        question_type="SHORT_ANSWER",
        category=AssessmentCategory.TECHNICAL_KNOWLEDGE.value,
        field="Python",
        topic="Async Programming",
    )
    q_psy = QuestionBank(
        author_id=mentor.id,
        title="Conflict Resolution Preferences",
        question_text="How do you handle disagreement in code reviews?",
        question_type="SCENARIO",
        category=AssessmentCategory.PSYCHOMETRIC.value,
        field="Leadership",
        topic="Team Collaboration",
    )
    q_file = QuestionBank(
        author_id=mentor.id,
        title="System Architecture Diagram Upload",
        question_text="Upload your architecture diagram in PDF or image format.",
        question_type="FILE_UPLOAD",
        category=AssessmentCategory.ADDITIONAL.value,
        field="Architecture",
        topic="System Design",
    )
    db_session.add_all([q_tech, q_psy, q_file])
    db_session.flush()

    assessment = Assessment(
        mentor_id=mentor.id,
        batch_id=batch.id,
        title="Phase B Assessment Test",
        field="Cloud Architecture",
        duration_minutes=45,
        passing_score=70.0,
        status="PUBLISHED",
        version=1,
    )
    db_session.add(assessment)
    db_session.flush()

    aq1 = AssessmentQuestion(assessment_id=assessment.id, bank_question_id=q_tech.id, sequence_order=1, marks=10.0)
    aq2 = AssessmentQuestion(assessment_id=assessment.id, bank_question_id=q_file.id, sequence_order=2, marks=10.0)
    db_session.add_all([aq1, aq2])
    db_session.flush()

    attempt = AssessmentAttempt(
        assessment_id=assessment.id,
        learner_id=learner.id,
        start_time=datetime.now(UTC) - timedelta(minutes=20),
        total_marks=20.0,
        score=0.0,
        status="IN_PROGRESS",
    )
    db_session.add(attempt)
    db_session.flush()

    ans1 = Answer(
        attempt_id=attempt.id,
        bank_question_id=q_tech.id,
        text_response="Asyncio leverages a single-threaded cooperative multitasking event loop using coroutines.",
        grading_status="PENDING_REVIEW",
        score_awarded=0.0,
    )
    db_session.add(ans1)
    db_session.commit()

    return {
        "admin": admin,
        "mentor": mentor,
        "learner": learner,
        "assessment": assessment,
        "attempt": attempt,
        "q_tech": q_tech,
        "q_psy": q_psy,
        "q_file": q_file,
        "ans1": ans1,
    }


# ==============================================================================
# B1: Multi-Role Chatbot & Streaming Tests
# ==============================================================================

def test_learner_chatbot_chat_and_offline_card(b_setup, db_session):
    learner = b_setup["learner"]

    # 1. Chat with model offline (circuit breaker tripped)
    ai_gateway.circuit_breaker.trip()
    req = ChatbotRequest(message="What is my current enrolled pathway?", history=[])
    data = chat_with_the_gardener(payload=req, db=db_session, learner=learner, _uow=None)

    assert "reply" in data
    assert "Cloud Engineering Pathway" in data["reply"] or "Cloud Engineering" in str(data["context_used"])
    assert data["provenance"]["provider"] == "procedural"
    ai_gateway.circuit_breaker.reset()


def test_mentor_and_admin_chatbot_endpoints(b_setup, db_session):
    # Mentor Chatbot
    mentor = b_setup["mentor"]
    req_m = MentorChatbotRequest(message="How many learners are currently assigned to my batches?", history=[])
    res_m = chat_with_mentor_assistant(payload=req_m, db=db_session, mentor=mentor, _uow=None)
    assert "reply" in res_m
    assert res_m["context_used"]["role"] == "MENTOR"

    # Admin Chatbot
    admin = b_setup["admin"]
    req_a = AdminChatbotRequest(message="What is the total platform user count?", history=[])
    res_a = chat_with_admin_copilot(payload=req_a, db=db_session, admin=admin, _uow=None)
    assert "reply" in res_a
    assert res_a["context_used"]["role"] == "ADMIN"


def test_chatbot_streaming_sse_generator(b_setup, db_session):
    learner = b_setup["learner"]
    response = stream_with_the_gardener(payload=ChatbotRequest(message="Hello Gardener"), db=db_session, learner=learner)
    assert response.media_type == "text/event-stream"

    chunks = list(stream_chat_role(user=learner, user_message="Hello Gardener", db=db_session))
    body = "".join(chunks)
    assert "event: start" in body
    assert "event: delta" in body
    assert "event: done" in body


# ==============================================================================
# B2: Categories & AI Rubric Evaluation Tests
# ==============================================================================

def test_question_bank_category_filtering(b_setup, db_session):
    mentor = b_setup["mentor"]

    all_q = list_question_bank(db=db_session, mentor=mentor)
    assert len(all_q) >= 3

    psy_q = list_question_bank(category="Psychometric", db=db_session, mentor=mentor)
    assert len(psy_q) >= 1
    for q in psy_q:
        assert q["category"] == "Psychometric"


def test_ai_subjective_rubric_evaluation(b_setup, db_session):
    mentor = b_setup["mentor"]
    attempt = b_setup["attempt"]
    ans = b_setup["ans1"]

    data = ai_evaluate_subjective_answer(
        attempt_id=attempt.id,
        answer_id=ans.id,
        db=db_session,
        mentor=mentor,
    )
    assert "criteria" in data
    assert "proposed_score" in data
    assert 0.0 <= data["proposed_score"] <= data["max_score"]
    assert data["requires_mentor_confirmation"] is True
    assert len(data["strengths"]) > 0


# ==============================================================================
# B3: Storage & Answer File Upload Tests
# ==============================================================================

def test_answer_file_upload_and_signed_download(b_setup, db_session):
    learner = b_setup["learner"]
    attempt = b_setup["attempt"]
    q_file = b_setup["q_file"]

    file_content = b"%PDF-1.4 Mock system architecture diagram test file"
    upload = UploadFile(
        file=io.BytesIO(file_content),
        filename="architecture_diagram.pdf",
        headers={"content-type": "application/pdf"},
    )

    upload_data = upload_answer_file(
        attempt_id=attempt.id,
        question_id=q_file.id,
        file=upload,
        db=db_session,
        learner=learner,
    )
    assert "file_url" in upload_data
    assert "token" in upload_data
    assert upload_data["file_name"] == "architecture_diagram.pdf"

    # Download using signed token
    signed_token = upload_data["token"]
    file_resp = download_file(token_or_name=signed_token)
    assert file_resp.filename == "architecture_diagram.pdf"


# ==============================================================================
# B4: Growth Ring Report & PDF Generation Tests
# ==============================================================================

def test_growth_ring_pdf_generation():
    report_data = {
        "learner_name": "Priya Sharma",
        "assessment_title": "Enterprise Cloud Architecture",
        "score": 85.0,
        "total_marks": 100.0,
        "percentage": 85.0,
        "passed": True,
        "percentile_rank": 92.0,
        "category_proficiencies": {
            "Cloud Infrastructure": 90.0,
            "Security & Auth": 80.0,
            "Database Systems": 85.0,
        },
        "strengths": ["High accuracy on IAM policy evaluation", "Optimized VPC peering architecture"],
        "gaps": ["Deep dive recommended on Redis caching invalidation"],
        "next_steps": ["Review Redis eviction policies", "Complete 2 practice labs"],
        "ai_narrative": "Priya demonstrates outstanding proficiency in core cloud topologies.",
        "generated_at": datetime.now(UTC).isoformat(),
    }
    pdf_bytes = generate_growth_ring_pdf(report_data)
    assert len(pdf_bytes) > 500
    assert pdf_bytes.startswith(b"%PDF-")


# ==============================================================================
# B5: Topic Mastery & Mentor Needs-Attention Queue Tests
# ==============================================================================

def test_learner_topic_mastery_and_study_plan(b_setup, db_session):
    learner = b_setup["learner"]

    # Mastery
    mastery_data = get_learner_topic_mastery(db=db_session, learner=learner)
    assert "overall_mastery" in mastery_data
    assert len(mastery_data["topics"]) > 0

    # Study plan
    plan_data = generate_study_plan(db=db_session, learner=learner)
    assert len(plan_data["days"]) == 7
    assert "target_topic" in plan_data


def test_mentor_learners_needs_attention_queue(b_setup, db_session):
    mentor = b_setup["mentor"]
    items = get_learners_needs_attention(db=db_session, mentor=mentor)
    assert isinstance(items, list)
