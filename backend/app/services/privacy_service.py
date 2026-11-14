"""TRELLIS Privacy & Data Sanitization Query Layer.

Implements query-level data projections for:
1. Blind Grading: Sanitizes candidate submissions by stripping identifying PII
   and replacing with cryptographically salted pseudonymous tokens.
2. Anonymized Aggregation: Enforces k-anonymity (k >= 5) on reporting/analytics queries.
   Suppresses buckets with fewer than k subjects and eliminates individual employee identifiers.
"""

from __future__ import annotations

import hashlib
from typing import Any

CANDIDATE_PII_FIELDS = {
    "candidate_name",
    "candidate_email",
    "employee_code",
    "user_id",
    "sub",
    "full_name",
    "email",
    "avatar_url",
    "phone_number",
}


def sanitize_blind_grading_submission(
    record: dict[str, Any],
    salt: str = "trellis_blind_grading_salt_2026",
) -> dict[str, Any]:
    """Project away all candidate identifying PII, preserving only rubrics and blind submission data."""
    sanitized = {k: v for k, v in record.items() if k not in CANDIDATE_PII_FIELDS}

    # Generate deterministic pseudonymous token if candidate identifier was present
    raw_id = record.get("user_id") or record.get("sub") or record.get("employee_code")
    if raw_id:
        hasher = hashlib.sha256(f"{raw_id}:{salt}".encode())
        sanitized["blind_candidate_token"] = f"blind_{hasher.hexdigest()[:16]}"

    sanitized["is_blind_graded"] = True
    return sanitized


def sanitize_blind_grading_batch(
    records: list[dict[str, Any]],
    salt: str = "trellis_blind_grading_salt_2026",
) -> list[dict[str, Any]]:
    """Sanitize a collection of candidate submissions for blind evaluation."""
    return [sanitize_blind_grading_submission(r, salt=salt) for r in records]


def enforce_k_anonymity_aggregation(
    records: list[dict[str, Any]],
    group_by_fields: list[str],
    metric_keys: list[str],
    min_k: int = 5,
) -> list[dict[str, Any]]:
    """Aggregate records across groups while enforcing k-anonymity (k >= min_k).

    Invariants:
    1. If a group contains fewer than min_k subjects, metric values are suppressed.
    2. Individual employee identifiers are strictly stripped from all aggregate outputs.
    """
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = {}

    for record in records:
        group_key = tuple(record.get(f) for f in group_by_fields)
        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append(record)

    output: list[dict[str, Any]] = []

    for group_key, group_records in groups.items():
        count = len(group_records)
        group_meta = dict(zip(group_by_fields, group_key, strict=True))

        if count < min_k:
            # Suppress metric results to protect small-cohort employee privacy
            output.append(
                {
                    **group_meta,
                    "sample_size": f"<{min_k}",
                    "is_suppressed": True,
                    "metrics": dict.fromkeys(metric_keys),
                }
            )
        else:
            # Compute aggregate metric averages
            aggregated_metrics: dict[str, float] = {}
            for metric in metric_keys:
                values = [
                    float(r[metric]) for r in group_records if metric in r and r[metric] is not None
                ]
                aggregated_metrics[metric] = round(sum(values) / len(values), 2) if values else 0.0

            output.append(
                {
                    **group_meta,
                    "sample_size": count,
                    "is_suppressed": False,
                    "metrics": aggregated_metrics,
                }
            )

    return output
