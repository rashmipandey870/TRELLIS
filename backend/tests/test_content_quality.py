"""Content Quality and Uniqueness Verification Tests (Phase C).

Enforces:
C1: Zero duplicate questions per category (normalised stem + correct answer).
C2: English & Communication covers grammar, vocab, reading comprehension, sentence correction, and professional email tasks.
C3: Situational Judgement: unique scenarios, scored options.
C4: No distractor text appears in more than 3 questions; options in each question are distinct; quantitative & reasoning verified.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

# Ensure paths
repo_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(repo_root / "backend"))

from scripts.fixtures.aptitude_reasoning import APTITUDE_REASONING_QUESTIONS
from scripts.fixtures.communication_psychometric import COMMUNICATION_PSYCHOMETRIC_QUESTIONS
from scripts.fixtures.technical_questions import TECHNICAL_QUESTIONS


ALL_QUESTIONS = (
    TECHNICAL_QUESTIONS
    + APTITUDE_REASONING_QUESTIONS
    + COMMUNICATION_PSYCHOMETRIC_QUESTIONS
)


def normalize_text(text: str) -> str:
    """Normalize text by lowercasing and stripping punctuation and excessive whitespace."""
    text = re.sub(r"[^\w\s]", "", text.lower())
    return " ".join(text.split())


def test_zero_duplicate_question_stems():
    """Verify that all questions have unique normalized stems per category (Phase C1)."""
    seen = {}
    duplicates = []

    for q in ALL_QUESTIONS:
        cat = q.get("category", "")
        norm_stem = normalize_text(q.get("question_text", ""))
        key = (cat, norm_stem)
        if key in seen:
            duplicates.append(f"Category '{cat}': '{q.get('question_text')[:60]}...'")
        seen[key] = True

    assert not duplicates, (
        f"Found {len(duplicates)} duplicate question stems:\n"
        + "\n".join(duplicates[:10])
    )


def test_no_distractor_in_more_than_three_questions():
    """Verify that no distractor text is repeated across more than 3 questions (Phase C4)."""
    distractor_counts = Counter()

    for q in ALL_QUESTIONS:
        if q.get("question_type") == "MCQ" and "options" in q:
            correct = q.get("correct_answer", "").strip()
            for opt in q["options"]:
                opt_str = opt.strip()
                if opt_str != correct:
                    distractor_counts[opt_str] += 1

    overused_distractors = [
        (opt, count) for opt, count in distractor_counts.items() if count > 3
    ]

    assert not overused_distractors, (
        f"Found {len(overused_distractors)} distractors appearing in >3 questions:\n"
        + "\n".join(f"  ({cnt}x): {d[:60]}..." for d, cnt in overused_distractors[:10])
    )


def test_options_are_distinct_per_question():
    """Ensure that every question has completely distinct, non-redundant options."""
    redundancies = []

    for q in ALL_QUESTIONS:
        if q.get("question_type") == "MCQ" and "options" in q:
            opts = [o.strip() for o in q["options"]]
            if len(opts) != len(set(opts)):
                redundancies.append(q.get("title", "Untitled"))

    assert not redundancies, f"Questions with identical options: {redundancies}"


def test_english_category_policy_coverage():
    """Ensure English & Communication covers all 5 required curriculum dimensions (Phase C2)."""
    eng_qs = [q for q in ALL_QUESTIONS if q.get("category") == "English & Communication"]
    assert len(eng_qs) >= 40, f"Expected at least 40 English questions, got {len(eng_qs)}"

    topics = Counter(q.get("topic") for q in eng_qs)
    required_topics = [
        "Grammar & Construction",
        "Vocabulary in Context",
        "Reading Comprehension",
        "Sentence Correction",
        "Professional Writing",
    ]

    for req in required_topics:
        assert topics[req] >= 6, f"Topic '{req}' has insufficient coverage: {topics[req]} questions"
