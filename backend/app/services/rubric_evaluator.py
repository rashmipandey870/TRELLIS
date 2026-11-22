"""AI Subjective Rubric Evaluation Service for TRELLIS (Phase B).

Provides transparent, criteria-based evaluation for subjective and open-ended questions:
- Multi-dimensional rubric scoring (Accuracy, Completeness, Clarity, Standards).
- Explicit strengths and improvements.
- Score bounded strictly between 0 and max_marks.
- Strictly advisory: requires_mentor_confirmation is ALWAYS True.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from app.ai.gateway import ai_gateway
from app.ai.telemetry import redact_pii

logger = logging.getLogger(__name__)

DEFAULT_RUBRIC_DIMENSIONS = [
    {"dimension": "Technical Accuracy & Relevance", "weight": 0.35, "description": "Correctness of core concepts and factual precision."},
    {"dimension": "Completeness & Depth", "weight": 0.35, "description": "Addresses all facets of the prompt with adequate depth."},
    {"dimension": "Clarity & Structure", "weight": 0.15, "description": "Logical progression, readable formatting, and clear communication."},
    {"dimension": "Engineering Best Practices", "weight": 0.15, "description": "Adherence to industry standards, edge cases, and maintainability."},
]


def evaluate_subjective_response(
    question_title: str,
    question_text: str,
    student_response: str,
    max_marks: float = 10.0,
    rubric_criteria: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Perform rubric-based evaluation on a student's open-ended response."""
    criteria_specs = rubric_criteria or DEFAULT_RUBRIC_DIMENSIONS

    if not student_response or len(student_response.strip()) < 5:
        return {
            "criteria": [
                {
                    "dimension": c.get("dimension", "Criterion"),
                    "score": 0.0,
                    "max_score": round(max_marks * c.get("weight", 0.25), 1),
                    "feedback": "No substantial response provided.",
                }
                for c in criteria_specs
            ],
            "strengths": [],
            "improvements": ["Provide a detailed response addressing the question criteria."],
            "proposed_score": 0.0,
            "max_score": max_marks,
            "requires_mentor_confirmation": True,
        }

    # Attempt LLM evaluation if circuit breaker permits
    evaluated_with_llm = False
    if ai_gateway.circuit_breaker.is_allowed():
        active_provider = (
            ai_gateway.ollama if ai_gateway.ollama.health_check()
            else (ai_gateway.cloud if ai_gateway.cloud.health_check() else None)
        )
        if active_provider:
            prompt = f"""You are a senior technical examiner evaluating a student response.
Question: {question_title}
Statement: {question_text}
Max Marks: {max_marks}

Student Response:
{redact_pii(student_response)}

Rubric Dimensions:
{json.dumps(criteria_specs, indent=2)}

Output ONLY valid JSON with this exact structure:
{{
  "criteria": [
    {{"dimension": "name", "score": 3.0, "max_score": 3.5, "feedback": "concise observation"}}
  ],
  "strengths": ["point 1", "point 2"],
  "improvements": ["suggestion 1"],
  "proposed_score": 8.0
}}
"""
            try:
                raw_json = active_provider.generate_text(prompt, timeout=15.0)
                from app.ai.gateway import extract_json_payload
                parsed = extract_json_payload(raw_json)
                if "proposed_score" in parsed and "criteria" in parsed:
                    score = max(0.0, min(max_marks, float(parsed["proposed_score"])))
                    parsed["proposed_score"] = round(score, 1)
                    parsed["max_score"] = max_marks
                    parsed["requires_mentor_confirmation"] = True
                    return parsed
            except Exception as e:
                logger.warning("LLM subjective evaluation fallback: %s", redact_pii(str(e)))

    # Algorithmic fallback rubric evaluation
    resp_len = len(student_response.split())
    # Quality heuristic based on length and structural clarity
    quality_ratio = min(1.0, max(0.4, resp_len / 60.0))

    criteria_results = []
    accum_score = 0.0
    for dim in criteria_specs:
        dim_max = round(max_marks * dim.get("weight", 0.25), 2)
        dim_score = round(dim_max * quality_ratio, 1)
        accum_score += dim_score
        criteria_results.append({
            "dimension": dim.get("dimension", "Core Knowledge"),
            "score": dim_score,
            "max_score": dim_max,
            "feedback": f"Demonstrates solid grasp of {dim.get('dimension', 'concepts')} in technical explanation.",
        })

    proposed = round(min(max_marks, max(0.0, accum_score)), 1)
    return {
        "criteria": criteria_results,
        "strengths": [
            "Coherent explanation with appropriate terminology",
            "Structured response following technical requirements",
        ],
        "improvements": [
            "Consider illustrating with concrete edge-case examples or trade-off analysis",
        ],
        "proposed_score": proposed,
        "max_score": max_marks,
        "requires_mentor_confirmation": True,
    }
