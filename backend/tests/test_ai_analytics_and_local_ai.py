"""TRELLIS AI Diagnostic, Local AI & Visual Psychometrics Tests.

Validates:
1. Local AI & Ollama Integration:
   - JSON cleaning and schema parsing for local LLMs (zero API keys).
   - Graceful zero-downtime fallback to procedural multi-discipline generator when offline.
2. Educational Data Science via NumPy, Pandas & SciPy:
   - Cohort Gaussian normal distribution curve (SciPy stats.norm.pdf).
   - Psychometric percentile ranking (SciPy stats.percentileofscore).
   - Multi-track competency vector aggregation (Pandas DataFrame).
   - Linear regression performance trajectory (NumPy polyfit).
3. Vector SVG Visual Charts:
   - Cohort Bell Curve SVG generation with passing threshold and student marker.
   - Competency horizontal bar SVG chart.
   - Velocity trendline SVG chart.
4. AI Diagnostics Endpoints:
   - GET /learner/analytics/ai-diagnostic (learner self-review).
   - GET /mentor/learners/{learner_id}/ai-diagnostic (mentor review with 403 checks).
   - GET /mentor/assessments/{assessment_id}/ai-insights (item difficulty index & curve).
   - GET /admin/analytics/cohort-intelligence (department overview).
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api.v1.admin import get_cohort_intelligence, get_learner_detail
from app.api.v1.learner import get_learner_ai_diagnostic
from app.api.v1.mentor import get_assessment_ai_insights, get_learner_ai_diagnostic_for_mentor
from app.models import (
    Answer,
    Assessment,
    AssessmentAttempt,
    AssessmentQuestion,
    Base,
    Batch,
    MentorLearnerAssignment,
    Organisation,
    PracticeAttempt,
    PracticeQuestion,
    PracticeSession,
    QuestionBank,
    User,
)
from app.services.ai_analytics_engine import (
    analyze_assessment_ai_insights,
    analyze_learner_performance,
    generate_cohort_bell_curve_svg,
    generate_competency_bar_svg,
    generate_velocity_trendline_svg,
)
from app.services.ai_question_generator import (
    _clean_json_text,
    _call_llm_json,
    generate_ai_practice_problem,
)


@pytest.fixture
def ai_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        org = Organisation(name="CSM Technology", code="CSM_AI")
        session.add(org)
        session.flush()

        mentor = User(
            id="mentor_ai",
            org_id=org.id,
            email="mentor.ai@csm.tech",
            password_hash="pw",
            full_name="Dr. Alan Turing",
            role="MENTOR",
            is_active=True,
        )
        learner1 = User(
            id="learner_ai_1",
            org_id=org.id,
            email="learner.ai1@csm.tech",
            password_hash="pw",
            full_name="Ada Lovelace",
            role="LEARNER",
            is_active=True,
        )
        learner_outsider = User(
            id="learner_ai_outsider",
            org_id=org.id,
            email="outsider@csm.tech",
            password_hash="pw",
            full_name="Outsider User",
            role="LEARNER",
            is_active=True,
        )
        admin = User(
            id="admin_ai",
            org_id=org.id,
            email="admin.ai@csm.tech",
            password_hash="pw",
            full_name="Admin Director",
            role="ADMIN",
            is_active=True,
        )
        batch = Batch(
            id="batch_ai",
            org_id=org.id,
            name="AI Alpha Cohort",
            code="BATCH_AI_ALPHA",
            field="Python",
        )
        session.add_all([mentor, learner1, learner_outsider, admin, batch])
        session.flush()

        # Mentor assignment: mentor_ai -> learner1 in batch_ai
        assign = MentorLearnerAssignment(mentor_id=mentor.id, batch_id=batch.id, learner_id=learner1.id)
        session.add(assign)

        # Create Assessment with questions
        assessment = Assessment(
            id="assess_ai_1",
            mentor_id=mentor.id,
            batch_id=batch.id,
            title="Advanced Python Concurrency",
            field="Python",
            duration_minutes=60,
            passing_score=75.0,
            status="PUBLISHED",
            version=1,
        )
        session.add(assessment)
        session.flush()

        qb1 = QuestionBank(
            author_id=mentor.id,
            title="Asyncio Task Groups",
            question_text="What happens when a child task fails in asyncio.TaskGroup?",
            question_type="MCQ",
            field="Python",
            topic="Concurrency",
            difficulty="HARD",
        )
        session.add(qb1)
        session.flush()

        aq1 = AssessmentQuestion(
            assessment_id=assessment.id,
            bank_question_id=qb1.id,
            sequence_order=1,
            marks=10.0,
        )
        session.add(aq1)
        session.flush()

        # Add Completed Attempts for Learner 1
        att1 = AssessmentAttempt(
            assessment_id=assessment.id,
            learner_id=learner1.id,
            status="SUBMITTED",
            score=90.0,
            total_marks=100.0,
            passed=True,
            start_time=datetime(2026, 11, 20, 10, 0, tzinfo=UTC),
            submit_time=datetime(2026, 11, 20, 10, 35, tzinfo=UTC),
        )
        att2 = AssessmentAttempt(
            assessment_id=assessment.id,
            learner_id=learner1.id,
            status="SUBMITTED",
            score=84.0,
            total_marks=100.0,
            passed=True,
            start_time=datetime(2026, 11, 20, 12, 0, tzinfo=UTC),
            submit_time=datetime(2026, 11, 20, 12, 40, tzinfo=UTC),
        )
        session.add_all([att1, att2])
        session.flush()

        ans1 = Answer(
            attempt_id=att1.id,
            bank_question_id=qb1.id,
            score_awarded=10.0,
        )
        session.add(ans1)

        # Add Practice Session & Attempt
        ps1 = PracticeSession(
            id="ps_ai_1",
            learner_id=learner1.id,
            field="Python",
        )
        session.add(ps1)
        session.flush()

        pq1 = PracticeQuestion(
            session_id=ps1.id,
            title="FastAPI Lifespan Context",
            field="Python",
            difficulty="MEDIUM",
            mode="MCQ",
            question_data_json={"question": "Lifespan event handler signature"},
        )
        session.add(pq1)
        session.flush()

        pr1 = PracticeAttempt(
            learner_id=learner1.id,
            question_id=pq1.id,
            is_correct=True,
            answer_json={"selected_answer": "Option A"},
        )
        session.add(pr1)
        session.commit()

    with Session(engine) as session:
        yield session


def test_clean_json_text_and_schema_parsing():
    """Verify robust JSON markdown extraction for raw LLM outputs."""
    raw_markdown = "```json\n{\n  \"title\": \"Binary Tree Inversion\",\n  \"difficulty\": \"EASY\"\n}\n```"
    cleaned = _clean_json_text(raw_markdown)
    assert json.loads(cleaned) == {"title": "Binary Tree Inversion", "difficulty": "EASY"}

    prose_json = "Here is your requested question:\n{\"title\": \"SQL Join\", \"options\": [\"A\", \"B\", \"C\", \"D\"]}\nHope this helps!"
    cleaned2 = _clean_json_text(prose_json)
    assert json.loads(cleaned2)["title"] == "SQL Join"


def test_local_ollama_fallback_resilience():
    """Verify that when local Ollama is offline, generator automatically falls back to procedural engine."""
    with patch("urllib.request.urlopen", side_effect=Exception("Connection refused to localhost:11434")):
        res = _call_llm_json("generate question", timeout=1)
        assert res is None  # Handled gracefully without crash

    # Practice generation succeeds using deterministic generator
    problem = generate_ai_practice_problem(field="Python", difficulty="MEDIUM", mode="MCQ")
    assert problem["title"] is not None
    assert problem["mode"] == "MCQ"
    assert len(problem["options"]) == 4


def test_psychometrics_vector_svg_generators():
    """Verify SVG chart synthesis using SciPy and NumPy."""
    cohort_scores = [50.0, 60.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0]

    # 1. Cohort Bell Curve SVG
    curve_svg = generate_cohort_bell_curve_svg(learner_score=88.0, cohort_scores=cohort_scores, passing_score=75.0)
    assert "<svg" in curve_svg
    assert "</svg>" in curve_svg
    assert "viewBox" in curve_svg
    assert "Score: 88.0%" in curve_svg
    assert "PASS (75%)" in curve_svg

    # 2. Competency Bar SVG
    field_accs = {"Python": 92.5, "SQL": 88.0, "Java": 70.0, "DSA": 65.0}
    comp_svg = generate_competency_bar_svg(field_accs)
    assert "<svg" in comp_svg
    assert "Python" in comp_svg
    assert "92.5%" in comp_svg

    # 3. Velocity Trendline SVG
    trend_svg = generate_velocity_trendline_svg(scores=[70.0, 74.0, 80.0, 88.0, 92.0])
    assert "<svg" in trend_svg
    assert "polyline" in trend_svg


def test_analyze_learner_performance_dataframe(ai_db: Session):
    """Verify Pandas DataFrame aggregation and SciPy percentile evaluation."""
    diagnostic = analyze_learner_performance("learner_ai_1", ai_db)

    assert diagnostic["learner_id"] == "learner_ai_1"
    assert diagnostic["average_score"] > 80.0
    assert 0.0 <= diagnostic["percentile_rank"] <= 100.0
    assert "Python" in diagnostic["field_accuracies"]
    assert diagnostic["velocity_index"] > 0
    assert diagnostic["ai_narrative"] is not None
    assert "<svg" in diagnostic["charts"]["bell_curve_svg"]
    assert "<svg" in diagnostic["charts"]["competency_bar_svg"]
    assert "<svg" in diagnostic["charts"]["velocity_trendline_svg"]


def test_analyze_assessment_ai_insights(ai_db: Session):
    """Verify assessment item-level difficulty index and psychometrics."""
    insights = analyze_assessment_ai_insights("assess_ai_1", ai_db)

    assert insights["assessment_id"] == "assess_ai_1"
    assert insights["mean_score"] > 80.0
    assert len(insights["question_diagnostics"]) >= 1
    assert "accuracy_rate" in insights["question_diagnostics"][0]
    assert "<svg" in insights["charts"]["distribution_curve_svg"]


def test_api_analytics_endpoints_and_access_control(ai_db: Session):
    """Verify API routes for learner, mentor, and admin."""
    learner1 = ai_db.get(User, "learner_ai_1")
    mentor = ai_db.get(User, "mentor_ai")
    admin = ai_db.get(User, "admin_ai")

    # 1. Learner gets their own AI diagnostic
    res_l = get_learner_ai_diagnostic(db=ai_db, learner=learner1)
    assert res_l["learner_name"] == "Ada Lovelace"
    assert "charts" in res_l

    # 2. Mentor gets assigned learner's diagnostic (200)
    res_m = get_learner_ai_diagnostic_for_mentor(learner_id="learner_ai_1", db=ai_db, mentor=mentor)
    assert res_m["learner_id"] == "learner_ai_1"

    # 3. Mentor accessing unassigned learner returns 403 Forbidden
    with pytest.raises(HTTPException) as exc_403:
        get_learner_ai_diagnostic_for_mentor(learner_id="learner_ai_outsider", db=ai_db, mentor=mentor)
    assert exc_403.value.status_code == status.HTTP_403_FORBIDDEN

    # 4. Mentor gets assessment AI insights
    res_a = get_assessment_ai_insights(assessment_id="assess_ai_1", db=ai_db, mentor=mentor)
    assert res_a["assessment_id"] == "assess_ai_1"

    # 5. Admin gets cohort intelligence
    res_admin = get_cohort_intelligence(db=ai_db, _admin=admin)
    assert "total_submissions" in res_admin
    assert "<svg" in res_admin["charts"]["cohort_bell_curve_svg"]
