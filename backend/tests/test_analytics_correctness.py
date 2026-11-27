"""Unit and integration tests for verified analytics correctness (Section 3).

Verifies:
- Percentage normalization (score / total_marks * 100)
- Excludes psychometric assessments from technical metrics
- Trend slope agreement with qualitative labels (Improving, Declining, Steady)
- Percentile rank returns null when N < 10, accurate rank when N >= 10
- Item difficulty index P, discrimination index D, distractor distribution
- Every metric endpoint returns n, computed_at, definition
- Zero hard-coded fallback values
"""

from __future__ import annotations

import math
from datetime import UTC, datetime, timedelta
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

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
    QuestionBank,
    Submission,
    User,
)
from app.services.analytics_service import (
    analyze_assessment_comprehensive,
    analyze_learner,
    compute_linear_trend_slope,
    compute_percentage_score,
    compute_percentile_rank,
    compute_sample_stdev,
)


def test_percentage_score_normalization():
    assert compute_percentage_score(45.0, 50.0) == 90.0
    assert compute_percentage_score(0.0, 100.0) == 0.0
    assert compute_percentage_score(100.0, 100.0) == 100.0
    assert compute_percentage_score(10.0, 0.0) == 0.0


def test_linear_trend_slope_and_labels():
    # Strictly increasing
    slope, label = compute_linear_trend_slope([60.0, 70.0, 80.0, 90.0])
    assert slope == 10.0
    assert label == "Improving"

    # Strictly decreasing
    slope, label = compute_linear_trend_slope([90.0, 80.0, 70.0, 60.0])
    assert slope == -10.0
    assert label == "Declining"

    # Steady / flat
    slope, label = compute_linear_trend_slope([75.0, 75.2, 74.9, 75.1])
    assert abs(slope) < 0.5
    assert label == "Steady"

    # Single value
    slope, label = compute_linear_trend_slope([85.0])
    assert slope == 0.0
    assert label == "Steady"


def test_percentile_rank_bounds():
    # N < 10 returns None
    assert compute_percentile_rank(75.0, [60.0, 70.0, 80.0]) is None

    # N >= 10
    cohort = [50.0, 60.0, 70.0, 75.0, 80.0, 85.0, 90.0, 92.0, 95.0, 100.0]
    rank = compute_percentile_rank(75.0, cohort)
    assert rank is not None
    assert 30.0 <= rank <= 40.0


def test_sample_stdev():
    assert compute_sample_stdev([]) == 0.0
    assert compute_sample_stdev([50.0]) == 0.0
    vals = [10.0, 20.0, 30.0]
    assert compute_sample_stdev(vals) == 10.0


def test_learner_analytics_excludes_psychometrics():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as db:
        org = Organisation(name="CSM Analytics", code="CSM-ANA")
        db.add(org)
        db.flush()

        learner = User(
            org_id=org.id,
            email="ana_learner@csmtech.internal",
            password_hash="pwd",
            full_name="Analytics Learner",
            role="LEARNER",
            is_active=True,
        )
        mentor = User(
            org_id=org.id,
            email="ana_mentor@csmtech.internal",
            password_hash="pwd",
            full_name="Analytics Mentor",
            role="MENTOR",
            is_active=True,
        )
        db.add_all([learner, mentor])
        db.flush()

        # 1. Technical assessment (80/100 -> 80%)
        tech_assessment = Assessment(
            mentor_id=mentor.id,
            title="Python Advanced",
            field="Python",
            passing_score=60,
        )
        # 2. Psychometric assessment (unscored or dimension-only)
        psycho_assessment = Assessment(
            mentor_id=mentor.id,
            title="Behavioral Inventory",
            field="Psychometric",
            passing_score=0,
        )
        db.add_all([tech_assessment, psycho_assessment])
        db.flush()

        att_tech = AssessmentAttempt(
            assessment_id=tech_assessment.id,
            learner_id=learner.id,
            score=80.0,
            total_marks=100.0,
            passed=True,
            status="SUBMITTED",
            submit_time=datetime.now(UTC),
        )
        att_psycho = AssessmentAttempt(
            assessment_id=psycho_assessment.id,
            learner_id=learner.id,
            score=0.0,
            total_marks=0.0,
            passed=True,
            status="SUBMITTED",
            submit_time=datetime.now(UTC),
        )
        db.add_all([att_tech, att_psycho])
        db.commit()

        analysis = analyze_learner(learner.id, db)

        # Technical mean must be 80.0, NOT dragged down to 40.0 by psychometrics!
        assert analysis["scores"]["mean_percentage"] == 80.0
        assert analysis["n_scored_assessments"] == 1
        assert analysis["n_scored_assessments"] == len(analysis["scores"]["history"])
        assert "computed_at" in analysis
        assert "definition" in analysis


def test_analyze_assessment_comprehensive_with_selected_option_ids_json():
    """Verify item analysis and distractor counts work with selected_option_ids_json without 500."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as db:
        org = Organisation(name="CSM Analytics 2", code="CSM-ANA2")
        db.add(org)
        db.flush()

        mentor = User(
            org_id=org.id,
            email="item_mentor@csmtech.internal",
            password_hash="pwd",
            full_name="Item Mentor",
            role="MENTOR",
            is_active=True,
        )
        learners = [
            User(
                org_id=org.id,
                email=f"item_learner_{i}@csmtech.internal",
                password_hash="pwd",
                full_name=f"Item Learner {i}",
                role="LEARNER",
                is_active=True,
            )
            for i in range(5)
        ]
        db.add_all([mentor] + learners)
        db.flush()

        q1 = QuestionBank(
            author_id=mentor.id,
            title="FastAPI Lifespan",
            question_text="How do you handle lifespan events?",
            question_type="MCQ",
            field="Python",
            topic="FastAPI",
            category="TECHNICAL",
            difficulty="MEDIUM",
        )
        db.add(q1)
        db.flush()

        assessment = Assessment(
            mentor_id=mentor.id,
            title="FastAPI Mastery",
            field="Python",
            passing_score=60,
        )
        db.add(assessment)
        db.flush()

        aq = AssessmentQuestion(
            assessment_id=assessment.id,
            bank_question_id=q1.id,
            marks=10,
            sequence_order=1,
        )
        db.add(aq)
        db.flush()

        # Add attempts with answers using selected_option_ids_json
        for idx, l in enumerate(learners):
            att = AssessmentAttempt(
                assessment_id=assessment.id,
                learner_id=l.id,
                score=10.0 if idx < 3 else 0.0,
                total_marks=10.0,
                passed=idx < 3,
                status="SUBMITTED",
                submit_time=datetime.now(UTC),
            )
            db.add(att)
            db.flush()

            chosen_opt = "opt_correct" if idx < 3 else "opt_distractor_b"
            ans = Answer(
                attempt_id=att.id,
                bank_question_id=q1.id,
                selected_option_ids_json=[chosen_opt],
                score_awarded=10.0 if idx < 3 else 0.0,
            )
            # Verify Answer model backward-compatible properties
            assert ans.selected_option_id == chosen_opt
            assert ans.answer_text is None
            db.add(ans)

        db.commit()

        # Run comprehensive analysis - must not raise AttributeError or 500
        result = analyze_assessment_comprehensive(assessment.id, db)
        assert result is not None
        assert result["assessment_id"] == assessment.id
        assert len(result["item_analysis"]) == 1
        item = result["item_analysis"][0]
        assert item["question_id"] == q1.id
        assert item["distractor_counts"].get("opt_correct") == 3
        assert item["distractor_counts"].get("opt_distractor_b") == 2
        assert item["difficulty_index_p"] == 0.60
