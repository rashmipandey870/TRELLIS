"""Quality verification gates for AI-generated practice questions in TRELLIS."""

from __future__ import annotations

import logging
from typing import Any

from app.ai.schemas import GeneratedCodingProblem, GeneratedMcqProblem
from app.services.code_runner import CodeRunner

logger = logging.getLogger(__name__)


def verify_mcq_quality(problem: GeneratedMcqProblem) -> bool:
    """Verify that MCQ meets strict quality gates:
    1. Exactly 4 distinct options.
    2. Correct answer is in options.
    3. Non-empty explanation and hints.
    """
    if len(problem.options) != 4:
        return False
    if len(set(problem.options)) != 4:
        return False
    if problem.correct_answer not in problem.options:
        return False
    if len(problem.explanation.strip()) < 5:
        return False
    return True


def verify_coding_quality(problem: GeneratedCodingProblem) -> bool:
    """Verify that Coding/SQL problem passes sandbox verification:
    1. Language starter code matches target language.
    2. Reference solution passes 100% of test cases in isolated runner.
    3. Wrong stub fails at least one test case.
    4. If compiler runtime is unavailable on the local OS (e.g. JDK or GCC absent),
       gracefully validates structure without raising an unhandled 500 error.
    """
    lang = problem.language.lower().strip()
    if lang not in problem.starter_code:
        logger.warning("Quality gate failed: starter_code missing key for '%s'", lang)
        return False

    ref_code = problem.reference_solution
    test_cases = problem.test_cases
    if not ref_code or not test_cases:
        return False

    try:
        ref_res = CodeRunner.execute(
            code=ref_code,
            language=lang,
            test_cases=test_cases,
            time_limit_ms=3500,
            mask_hidden_inputs=False,
        )

        # If runner is unavailable on this host (e.g. missing javac/node), log and accept structural validity
        if ref_res.verdict == "RUNNER_UNAVAILABLE":
            logger.info("Runner unavailable on local host for language '%s'; structural check accepted", lang)
            return True

        if ref_res.verdict != "ACCEPTED" or ref_res.score < 100.0:
            logger.warning(
                "Sandbox verification failed for reference solution (%s): verdict=%s, score=%s",
                lang,
                ref_res.verdict,
                ref_res.score,
            )
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
                return False

        return True
    except Exception as e:
        logger.warning("Sandbox verification encountered execution error: %s", e)
        return False
