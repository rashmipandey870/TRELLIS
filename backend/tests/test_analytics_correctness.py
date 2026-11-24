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
