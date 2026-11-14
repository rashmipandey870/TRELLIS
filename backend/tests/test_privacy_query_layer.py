"""TRELLIS Test Suite: Privacy & Query Layer Data Projections."""

from app.services.privacy_service import (
    CANDIDATE_PII_FIELDS,
    enforce_k_anonymity_aggregation,
    sanitize_blind_grading_batch,
    sanitize_blind_grading_submission,
)


def test_blind_grading_projection_strips_all_candidate_pii() -> None:
    raw_submission = {
        "user_id": "usr_cand_999",
        "candidate_name": "Priya Candidate",
        "candidate_email": "priya.cand@csm.tech",
        "employee_code": "CSM-9921",
        "submission_text": "Solution to distributed ledger consensus problem.",
        "rubric_scores": {"architecture": 4, "code_quality": 5},
    }

    sanitized = sanitize_blind_grading_submission(raw_submission)

    # Invariant: No candidate identifying PII exists in output
    for pii_field in CANDIDATE_PII_FIELDS:
        assert pii_field not in sanitized

    # Invariant: Blind candidate token is generated deterministically
    assert "blind_candidate_token" in sanitized
    assert sanitized["blind_candidate_token"].startswith("blind_")

    # Invariant: Rubrics and content are preserved intact
    assert sanitized["submission_text"] == raw_submission["submission_text"]
    assert sanitized["rubric_scores"] == raw_submission["rubric_scores"]
    assert sanitized["is_blind_graded"] is True


def test_blind_grading_batch_sanitizes_multiple_records() -> None:
    batch = [
        {"user_id": f"usr_{i}", "candidate_name": f"User {i}", "score": 80 + i} for i in range(10)
    ]
    sanitized_batch = sanitize_blind_grading_batch(batch)
    assert len(sanitized_batch) == 10
    for item in sanitized_batch:
        assert "user_id" not in item
        assert "candidate_name" not in item
        assert "blind_candidate_token" in item


def test_k_anonymity_enforces_suppression_when_k_less_than_5() -> None:
    # 4 records in Cohort A (less than min_k = 5)
    small_cohort_records = [
        {"cohort_id": "cohort_alpha", "user_id": f"emp_{i}", "growth_score": 85.0} for i in range(4)
    ]

    result = enforce_k_anonymity_aggregation(
        records=small_cohort_records,
        group_by_fields=["cohort_id"],
        metric_keys=["growth_score"],
        min_k=5,
    )

    assert len(result) == 1
    row = result[0]
    assert row["cohort_id"] == "cohort_alpha"
    assert row["is_suppressed"] is True
    assert row["sample_size"] == "<5"
    assert row["metrics"]["growth_score"] is None
    assert "user_id" not in row


def test_k_anonymity_computes_aggregate_when_k_greater_or_equal_5() -> None:
    # 6 records in Cohort B (meets min_k = 5)
    sufficient_cohort_records = [
        {"cohort_id": "cohort_beta", "user_id": f"emp_{i}", "growth_score": 90.0} for i in range(6)
    ]

    result = enforce_k_anonymity_aggregation(
        records=sufficient_cohort_records,
        group_by_fields=["cohort_id"],
        metric_keys=["growth_score"],
        min_k=5,
    )

    assert len(result) == 1
    row = result[0]
    assert row["cohort_id"] == "cohort_beta"
    assert row["is_suppressed"] is False
    assert row["sample_size"] == 6
    assert row["metrics"]["growth_score"] == 90.0
    assert "user_id" not in row
