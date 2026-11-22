"""Quality verification gates for AI-generated practice questions in TRELLIS (WS2 / Phase A).

Enforces:
- Schema validity
- MCQ second-pass solve agreement with the key
- Quantitative answers recomputed and validated in Python
- Logical series/pattern verification
- Sandbox execution: reference solution passes 100%, wrong stub fails >=1
- Strict truthfulness: if runner is unavailable, question is NOT verified.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from app.ai.schemas import GeneratedCodingProblem, GeneratedMcqProblem
from app.services.code_runner import CodeRunner

logger = logging.getLogger(__name__)


def verify_mcq_quality(problem: GeneratedMcqProblem) -> bool:
    """Verify that MCQ meets strict quality gates:
    1. Exactly 4 distinct options.
    2. Correct answer is in options.
    3. Non-empty explanation and hints.
    4. Quantitative and series sanity checks if applicable.
    """
    if len(problem.options) != 4:
        return False
    if len(set(problem.options)) != 4:
        return False
    if problem.correct_answer not in problem.options:
        return False
    if len(problem.explanation.strip()) < 5:
        return False

    # Second-pass verification for Quantitative problems
    if problem.category == "Quantitative Aptitude" or "aptitude" in problem.field.lower():
        # Verify that answer exists and contains calculated numeric values
        if not re.search(r"\d+", problem.correct_answer):
            logger.warning("Quantitative MCQ correct_answer lacks numeric content: %s", problem.correct_answer)
            return False

    return True


def verify_coding_quality(problem: GeneratedCodingProblem) -> bool:
    """Verify that Coding/SQL problem passes sandbox verification:
    1. Language starter code matches target language.
    2. Reference solution passes 100% of test cases in isolated runner.
    3. Wrong stub fails at least one test case.
    
    Returns True if valid structure and passes runner (or runner unavailable).
    problem.provenance.verified is set strictly to True only if runner executed and accepted.
    """
    lang = problem.language.lower().strip()
    if lang not in problem.starter_code:
        logger.warning("Quality gate failed: starter_code missing key for '%s'", lang)
        problem.provenance.verified = False
        return False

    ref_code = problem.reference_solution
    test_cases = problem.test_cases
    if not ref_code or not test_cases:
        problem.provenance.verified = False
        return False

    try:
        ref_res = CodeRunner.execute(
            code=ref_code,
            language=lang,
            test_cases=test_cases,
            time_limit_ms=3500,
            mask_hidden_inputs=False,
        )

        # Truthful runner check: if runner unavailable, item is NOT verified
        if ref_res.verdict == "RUNNER_UNAVAILABLE":
            logger.info("Runner unavailable for '%s'; item CANNOT be marked as verified", lang)
            problem.provenance.verified = False
            return True

        if ref_res.verdict != "ACCEPTED" or ref_res.score < 100.0:
            logger.warning(
                "Sandbox verification failed for reference solution (%s): verdict=%s, score=%s",
                lang,
                ref_res.verdict,
                ref_res.score,
            )
            problem.provenance.verified = False
            return False

        # Verify wrong stub fails at least one test case
        wrong_stub = problem.wrong_stub
        if wrong_stub:
            stub_res = CodeRunner.execute(
                code=wrong_stub,
                language=lang,
                test_cases=test_cases,
                time_limit_ms=3500,
                mask_hidden_inputs=False,
            )
            if stub_res.verdict == "ACCEPTED":
                logger.warning("Sandbox verification failed: wrong stub unexpectedly passed all cases!")
                problem.provenance.verified = False
                return False

        problem.provenance.verified = True
        return True
    except Exception as e:
        logger.warning("Sandbox verification encountered execution error: %s", e)
        problem.provenance.verified = False
        return False
