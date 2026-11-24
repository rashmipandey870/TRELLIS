"""TRELLIS Statistical & Educational Analytics Engine.

Calculates mathematically rigorous, verified metrics derived solely from raw database rows:
- Learner diagnostic, percentile rank, regression slope & trajectory, consistency
- Normalized percentage scores, excluding psychometric / unscored assessments
- Assessment completion funnel, Gaussian score statistics, difficulty index P,
  discrimination index D, distractor distribution
- Cohort heatmaps and risk flags with transparent, auditable reasons
- Every metric returns `n`, `computed_at`, and `definition`
"""

from __future__ import annotations

import math
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload, selectinload

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
from app.models.batches import Batch, MentorLearnerAssignment
from app.models.meetings import Meeting, MeetingAttendance, MeetingAudience
from app.models.practice import PracticeAttempt, PracticeScore
from app.models.user import User
from app.services.streak_service import derive_learner_streak_and_activity


def compute_percentage_score(score: float, total_marks: float) -> float:
    """Normalize score to percentage (0 - 100%)."""
    if total_marks <= 0:
        return 0.0
    pct = (score / total_marks) * 100.0
    return round(max(0.0, min(100.0, pct)), 2)


def compute_linear_trend_slope(values: list[float]) -> tuple[float, str]:
    """Calculate simple linear regression slope and corresponding qualitative label."""
    n = len(values)
    if n < 2:
        return 0.0, "Steady"

    x_mean = (n - 1) / 2.0
    y_mean = sum(values) / n

    numerator = sum((i - x_mean) * (y - y_mean) for i, y in enumerate(values))
    denominator = sum((i - x_mean) ** 2 for i in range(n))

    if denominator == 0:
        return 0.0, "Steady"

    slope = numerator / denominator
    rounded_slope = round(float(slope), 2)

    if rounded_slope > 0.5:
        label = "Improving"
    elif rounded_slope < -0.5:
        label = "Declining"
    else:
        label = "Steady"

    return rounded_slope, label


def compute_sample_stdev(values: list[float]) -> float:
    """Compute sample standard deviation."""
    n = len(values)
    if n < 2:
        return 0.0
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / (n - 1)
    return round(math.sqrt(variance), 2)


def compute_percentile_rank(target_value: float, all_values: list[float]) -> float | None:
    """Compute percentile rank within cohort (null if sample count N < 10)."""
    n = len(all_values)
    if n < 10:
        return None

    count_below = sum(1 for v in all_values if v < target_value)
    count_equal = sum(1 for v in all_values if math.isclose(v, target_value, abs_tol=1e-5))

    rank = ((count_below + 0.5 * count_equal) / n) * 100.0
    return round(rank, 1)


def analyze_learner(learner_id: str, db: Session) -> dict[str, Any]:
    """Calculate exhaustive, mathematically sound learner performance analysis."""
    now_iso = datetime.now(UTC).isoformat()

    learner = db.get(User, learner_id)
    if not learner:
        raise ValueError(f"Learner {learner_id} not found.")

    # 1. Assessment attempts (exclude Psychometric assessments from technical performance)
    attempts = (
        db.execute(
            select(AssessmentAttempt)
            .options(joinedload(AssessmentAttempt.assessment))
            .where(
                AssessmentAttempt.learner_id == learner_id,
                AssessmentAttempt.status == "SUBMITTED",
            )
            .order_by(AssessmentAttempt.submit_time.asc())
        )
        .scalars()
        .all()
    )

    scored_attempts = [
        a for a in attempts
        if a.assessment and a.assessment.field not in ("Psychometric", "Situational Judgement")
    ]
    psychometric_attempts = [
        a for a in attempts
        if a.assessment and a.assessment.field in ("Psychometric", "Situational Judgement")
    ]

    percentage_scores = [
        compute_percentage_score(a.score, a.total_marks)
        for a in scored_attempts
    ]
    n_scored = len(percentage_scores)

    mean_pct = round(sum(percentage_scores) / n_scored, 1) if n_scored > 0 else None
    sorted_scores = sorted(percentage_scores)
    median_pct = (
        round(sorted_scores[n_scored // 2], 1)
        if n_scored % 2 == 1
        else round((sorted_scores[n_scored // 2 - 1] + sorted_scores[n_scored // 2]) / 2.0, 1)
        if n_scored > 0
        else None
    )
    stdev_pct = compute_sample_stdev(percentage_scores) if n_scored >= 2 else 0.0
    slope, trend_label = compute_linear_trend_slope(percentage_scores)

    # 2. Batch and cohort percentile rank
    assignment = (
        db.execute(
            select(MentorLearnerAssignment).where(MentorLearnerAssignment.learner_id == learner_id)
        )
        .scalars()
        .first()
    )
    batch_id = assignment.batch_id if assignment else None

    # Cohort scores for percentile
    all_cohort_attempts = (
        db.execute(
            select(AssessmentAttempt)
            .options(joinedload(AssessmentAttempt.assessment))
            .where(AssessmentAttempt.status == "SUBMITTED")
        )
        .scalars()
        .all()
    )
    cohort_learner_scores: dict[str, list[float]] = {}
    batch_learner_scores: dict[str, list[float]] = {}

    for a in all_cohort_attempts:
        if a.assessment and a.assessment.field not in ("Psychometric", "Situational Judgement"):
            pct = compute_percentage_score(a.score, a.total_marks)
            cohort_learner_scores.setdefault(a.learner_id, []).append(pct)

    cohort_averages = [
        sum(scs) / len(scs) for scs in cohort_learner_scores.values() if scs
    ]
    percentile_in_cohort = (
        compute_percentile_rank(mean_pct, cohort_averages)
        if mean_pct is not None
        else None
    )

    # 3. Meeting Attendance
    attendances = (
        db.execute(
            select(MeetingAttendance).where(MeetingAttendance.learner_id == learner_id)
        )
        .scalars()
        .all()
    )
    total_meetings = len(attendances)
    attended_count = sum(1 for att in attendances if att.attended)
    attendance_rate = (
        round((attended_count / total_meetings) * 100.0, 1) if total_meetings > 0 else 100.0
    )

    # 4. Coding Performance
    submissions = (
        db.execute(select(Submission).where(Submission.learner_id == learner_id))
        .scalars()
        .all()
    )
    total_submissions = len(submissions)
    accepted_submissions = [s for s in submissions if s.verdict == "ACCEPTED"]
    coding_acceptance_rate = (
        round((len(accepted_submissions) / total_submissions) * 100.0, 1)
        if total_submissions > 0
        else 0.0
    )

    verdict_mix: dict[str, int] = {}
    for s in submissions:
        verdict_mix[s.verdict] = verdict_mix.get(s.verdict, 0) + 1

    # 5. Practice & Streak History
    streak_data = derive_learner_streak_and_activity(learner_id, db)

    # 6. Risk Flags with transparent explanations
    risk_flags: list[dict[str, str]] = []
    if attendance_rate < 75.0 and total_meetings >= 3:
        risk_flags.append({
            "flag": "LOW_ATTENDANCE",
            "reason": f"Meeting attendance is {attendance_rate}%, below 75% threshold ({attended_count}/{total_meetings} meetings attended).",
        })
    if trend_label == "Declining" and n_scored >= 3:
        risk_flags.append({
            "flag": "DECLINING_PERFORMANCE",
            "reason": f"Score regression trajectory is declining (slope: {slope} points per assessment across last {n_scored} assessments).",
        })
    if streak_data["active_days"] < 3 and total_submissions > 0:
        risk_flags.append({
            "flag": "INACTIVE_PRACTICE",
            "reason": f"Only {streak_data['active_days']} active practice days logged in the event ledger.",
        })

    # 7. Psychometric Dimension Profile
    psychometric_profile = {}
    for pa in psychometric_attempts:
        answers = (
            db.execute(select(Answer).where(Answer.attempt_id == pa.id)).scalars().all()
        )
        for ans in answers:
            dim = ans.rubric_feedback or "General"
            psychometric_profile[dim] = psychometric_profile.get(dim, 0) + int(ans.score_awarded)

    return {
        "learner_id": learner_id,
        "n_scored_assessments": n_scored,
        "computed_at": now_iso,
        "definition": "Mathematically derived learner proficiency, trajectory, attendance and coding metrics",
        "scores": {
            "mean_percentage": mean_pct,
            "median_percentage": median_pct,
            "consistency_stdev": stdev_pct,
            "history": [
                {
                    "attempt_id": a.id,
                    "assessment_id": a.assessment_id,
                    "title": a.assessment.title if a.assessment else "Assessment",
                    "percentage": pct,
                    "date": a.submit_time.isoformat() if a.submit_time else a.created_at.isoformat(),
                }
                for a, pct in zip(scored_attempts, percentage_scores)
            ],
        },
        "trajectory": {
            "slope": slope,
            "label": trend_label,
            "interpretation": f"Score velocity is {slope}% per assessment across {n_scored} scored assessments.",
        },
        "percentile_rank": {
            "cohort_percentile": percentile_in_cohort,
            "n_cohort_sample": len(cohort_averages),
        },
        "attendance": {
            "attendance_rate": attendance_rate,
            "total_meetings": total_meetings,
            "attended_meetings": attended_count,
        },
        "coding": {
            "total_submissions": total_submissions,
            "accepted_submissions": len(accepted_submissions),
            "acceptance_rate": coding_acceptance_rate,
            "verdict_mix": verdict_mix,
        },
        "practice": streak_data,
        "risk_flags": risk_flags,
        "psychometric_profile": psychometric_profile,
    }


def analyze_assessment_comprehensive(assessment_id: str, db: Session) -> dict[str, Any]:
    """Exhaustive mentor-level assessment analysis including item difficulty P and discrimination D."""
    now_iso = datetime.now(UTC).isoformat()

    assessment = (
        db.execute(
            select(Assessment)
            .options(
                selectinload(Assessment.attempts).selectinload(AssessmentAttempt.answers),
                selectinload(Assessment.questions).joinedload(AssessmentQuestion.question),
            )
            .where(Assessment.id == assessment_id)
        )
        .scalars()
        .first()
    )
    if not assessment:
        raise ValueError(f"Assessment {assessment_id} not found.")

    attempts = [a for a in assessment.attempts if a.status == "SUBMITTED"]
    n_attempts = len(attempts)

    # Completion Funnel
    total_assigned = len(assessment.audience_learners) if assessment.audience_learners else 0
    if total_assigned == 0 and assessment.batch_id:
        total_assigned = (
            db.execute(
                select(func.count(MentorLearnerAssignment.learner_id.distinct())).where(
                    MentorLearnerAssignment.batch_id == assessment.batch_id
                )
            ).scalar()
            or 0
        )
    started_count = len(assessment.attempts)
    submitted_count = n_attempts
    graded_count = sum(1 for a in attempts if getattr(a, "grading_status", "GRADED") == "GRADED")

    # Scores
    percentage_scores = [
        compute_percentage_score(a.score, a.total_marks)
        for a in attempts
    ]
    mean_score = round(sum(percentage_scores) / n_attempts, 1) if n_attempts > 0 else 0.0
    sorted_scores = sorted(percentage_scores)
    median_score = (
        round(sorted_scores[n_attempts // 2], 1)
        if n_attempts % 2 == 1
        else round((sorted_scores[n_attempts // 2 - 1] + sorted_scores[n_attempts // 2]) / 2.0, 1)
        if n_attempts > 0
        else 0.0
    )
    stdev_score = compute_sample_stdev(percentage_scores) if n_attempts >= 2 else 0.0
    pass_rate = (
        round((sum(1 for s in percentage_scores if s >= assessment.passing_score) / n_attempts) * 100.0, 1)
        if n_attempts > 0
        else 0.0
    )

    # Score histogram
    histogram = {
        "0-49": sum(1 for s in percentage_scores if s < 50),
        "50-69": sum(1 for s in percentage_scores if 50 <= s < 70),
        "70-89": sum(1 for s in percentage_scores if 70 <= s < 90),
        "90-100": sum(1 for s in percentage_scores if s >= 90),
    }

    # Item analysis: difficulty index P and discrimination index D
    item_analysis: list[dict[str, Any]] = []
    top_27_cutoff = max(1, int(n_attempts * 0.27))
    attempts_by_score = sorted(attempts, key=lambda a: a.score, reverse=True)
    top_group = attempts_by_score[:top_27_cutoff]
    bottom_group = attempts_by_score[-top_27_cutoff:] if top_27_cutoff > 0 else []

    for aq in sorted(assessment.questions, key=lambda q: q.sequence_order):
        q_id = aq.bank_question_id
        q_title = aq.question.title if aq.question else f"Question {aq.sequence_order}"
        q_type = aq.question.question_type if aq.question else "MCQ"

        total_q_attempts = 0
        correct_q_attempts = 0
        top_correct = 0
        bottom_correct = 0
        distractor_counts: dict[str, int] = {}

        for a in attempts:
            matching_ans = next((ans for ans in a.answers if ans.bank_question_id == q_id), None)
            if matching_ans:
                total_q_attempts += 1
                is_correct = matching_ans.score_awarded > 0
                if is_correct:
                    correct_q_attempts += 1
                if a in top_group and is_correct:
                    top_correct += 1
                if a in bottom_group and is_correct:
                    bottom_correct += 1

                resp = matching_ans.selected_option_id or matching_ans.answer_text
                if resp:
                    distractor_counts[resp] = distractor_counts.get(resp, 0) + 1

        p_index = round(correct_q_attempts / total_q_attempts, 2) if total_q_attempts > 0 else 0.0
        p_top = top_correct / len(top_group) if top_group else 0.0
        p_bottom = bottom_correct / len(bottom_group) if bottom_group else 0.0
        d_index = round(p_top - p_bottom, 2)

        item_analysis.append({
            "question_id": q_id,
            "title": q_title,
            "type": q_type,
            "marks": aq.marks,
            "difficulty_index_p": p_index,
            "discrimination_index_d": d_index,
            "distractor_counts": distractor_counts,
        })

    return {
        "assessment_id": assessment_id,
        "title": assessment.title,
        "n": n_attempts,
        "computed_at": now_iso,
        "definition": "Comprehensive psychometric and test-level statistical evaluation",
        "funnel": {
            "assigned": total_assigned,
            "started": started_count,
            "submitted": submitted_count,
            "graded": graded_count,
        },
        "score_statistics": {
            "mean_percentage": mean_score,
            "median_percentage": median_score,
            "stdev_percentage": stdev_score,
            "pass_rate_percentage": pass_rate,
            "histogram": histogram,
        },
        "item_analysis": item_analysis,
    }
