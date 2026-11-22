"""Automated test validating Answer-Key Distribution across all MCQ Question Bank Fixtures.

Phase 1.2 requirement:
No stored option position (A, B, C, D) may exceed 35% of total questions.
Keys must be balanced at ~25% per position.
"""

import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))

from scripts.fixtures.technical_questions import TECHNICAL_QUESTIONS
from scripts.fixtures.aptitude_reasoning import APTITUDE_REASONING_QUESTIONS
from scripts.fixtures.communication_psychometric import COMMUNICATION_PSYCHOMETRIC_QUESTIONS


def test_mcq_answer_key_distribution_is_balanced():
    """Verify that stored MCQ correct answer positions are balanced and no position exceeds 35%."""
    all_questions = TECHNICAL_QUESTIONS + APTITUDE_REASONING_QUESTIONS + COMMUNICATION_PSYCHOMETRIC_QUESTIONS
    positions = {0: 0, 1: 0, 2: 0, 3: 0}
    mcq_count = 0

    for q in all_questions:
        if q.get("question_type") == "MCQ":
            mcq_count += 1
            opts = q.get("options", [])
            ans = q.get("correct_answer")
            assert ans in opts, f"Question '{q.get('title')}' correct_answer not found in its options!"
            idx = opts.index(ans)
            assert 0 <= idx < 4, f"Option index {idx} out of range (must be 0..3) for '{q.get('title')}'"
            positions[idx] += 1

    assert mcq_count >= 200, f"Expected at least 200 MCQs, got {mcq_count}"

    for pos, count in positions.items():
        percentage = count / mcq_count
        label = chr(65 + pos)
        print(f"Position {pos} ({label}): {count}/{mcq_count} ({percentage*100:.1f}%)")
        assert percentage <= 0.35, f"Option position {label} has {percentage*100:.1f}%, exceeding the 35% maximum bias threshold!"
        assert percentage >= 0.15, f"Option position {label} has {percentage*100:.1f}%, falling below the 15% minimum representation threshold!"


def test_psychometric_likert_dimensions_and_rubrics():
    """Verify Psychometric questions use LIKERT format across 8 distinct dimensions with rubrics."""
    from app.schemas.category import AssessmentCategory, PSYCHOMETRIC_DISCLAIMER

    likert_items = [
        q for q in COMMUNICATION_PSYCHOMETRIC_QUESTIONS
        if q.get("category") == AssessmentCategory.PSYCHOMETRIC.value
    ]
    assert len(likert_items) == 48, f"Expected 48 Psychometric Likert items, got {len(likert_items)}"

    dimensions_found = set()
    reverse_keyed_count = 0

    for q in likert_items:
        assert q.get("question_type") == "LIKERT"
        assert q.get("correct_answer") is None, "Psychometric items must not have a right answer (no pass/fail)"
        assert len(q.get("options", [])) == 5
        rubric = q.get("rubric_json")
        assert rubric is not None
        assert "dimension" in rubric
        assert "reverse_keyed" in rubric
        dimensions_found.add(rubric["dimension"])
        if rubric["reverse_keyed"]:
            reverse_keyed_count += 1
        assert PSYCHOMETRIC_DISCLAIMER in q.get("explanation", "")

    assert len(dimensions_found) == 8, f"Expected 8 dimensions, found {len(dimensions_found)}: {dimensions_found}"
    assert reverse_keyed_count == 24, f"Expected exactly 24 reverse-keyed items (3 per dimension), got {reverse_keyed_count}"
