"""Automated test suite for TRELLIS AI Gateway, Circuit Breaker, Telemetry, and Pool (WS2)."""

import pytest
import time
from unittest.mock import MagicMock

from app.ai.circuit_breaker import CircuitBreaker
from app.ai.gateway import AIGateway, ai_gateway
from app.ai.pool import VerifiedPoolManager
from app.ai.prompts import extract_json_payload
from app.ai.providers.procedural import ProceduralAIProvider
from app.ai.quality_gates import verify_coding_quality, verify_mcq_quality
from app.ai.schemas import GeneratedCodingProblem, GeneratedMcqProblem
from app.ai.telemetry import AITelemetry, redact_pii
from app.services.code_runner import CodeRunner


def test_circuit_breaker_lifecycle():
    cb = CircuitBreaker(name="test_cb", failure_threshold=3, recovery_timeout=0.1)
    assert cb.state == "CLOSED"
    assert cb.is_allowed() is True

    # Record failures up to threshold
    cb.record_failure(ValueError("Fail 1"))
    cb.record_failure(ValueError("Fail 2"))
    assert cb.state == "CLOSED"

    cb.record_failure(ValueError("Fail 3"))
    assert cb.state == "OPEN"
    assert cb.is_allowed() is False

    # Wait for recovery timeout
    time.sleep(0.15)
    assert cb.state == "HALF_OPEN"
    assert cb.is_allowed() is True

    # Success recovers back to CLOSED
    cb.record_success()
    assert cb.state == "CLOSED"

    # Manual trip and reset
    cb.trip()
    assert cb.state == "OPEN"
    cb.reset()
    assert cb.state == "CLOSED"


def test_pii_redaction():
    text = (
        "User learner.one@csmtech.com with phone +1-555-123-4567 submitted "
        "Authorization: Bearer eyJhbGciOiJIUzI1NiIsIn... and api_key='sk_live_secret12345678' "
        "and password='supersecretpass123'"
    )
    redacted = redact_pii(text)
    assert "learner.one@csmtech.com" not in redacted
    assert "[REDACTED_EMAIL]" in redacted
    assert "+1-555-123-4567" not in redacted
    assert "[REDACTED_PHONE]" in redacted
    assert "[REDACTED_TOKEN]" in redacted
    assert "sk_live_secret12345678" not in redacted
    assert "supersecretpass123" not in redacted


def test_telemetry_metrics_tracking():
    telemetry = AITelemetry()
    t0 = telemetry.record_request_start()
    time.sleep(0.01)
    telemetry.record_request_end(t0, success=True, validation_passed=True)

    t1 = telemetry.record_request_start()
    time.sleep(0.02)
    telemetry.record_request_end(t1, success=False, validation_passed=False)

    metrics = telemetry.get_metrics()
    assert metrics["total_requests"] == 2
    assert metrics["success_rate_percent"] == 50.0
    assert metrics["validation_pass_rate_percent"] == 50.0
    assert metrics["p50_latency_ms"] > 0.0


def test_extract_json_payload():
    raw_md = "```json\n{\"title\": \"Sample\", \"options\": [\"A\", \"B\", \"C\", \"D\"]}\n```"
    data = extract_json_payload(raw_md)
    assert data["title"] == "Sample"

    raw_text = "Some intro text: {\"key\": \"value\"} concluding remarks"
    data2 = extract_json_payload(raw_text)
    assert data2["key"] == "value"


def test_procedural_mcq_generation_across_fields():
    provider = ProceduralAIProvider()
    for field in ["Python", "SQL", "Java", "JavaScript", "Cloud", "Aptitude"]:
        mcq = provider.generate_mcq(field=field, difficulty="MEDIUM")
        assert isinstance(mcq, GeneratedMcqProblem)
        assert len(mcq.options) == 4
        assert len(set(mcq.options)) == 4
        assert mcq.correct_answer in mcq.options
        assert verify_mcq_quality(mcq) is True


def test_procedural_coding_generation_sql():
    provider = ProceduralAIProvider()
    sql_prob = provider.generate_coding(field="SQL", difficulty="MEDIUM", language="sql")
    assert isinstance(sql_prob, GeneratedCodingProblem)
    assert sql_prob.language == "sql"
    assert "sql" in sql_prob.starter_code
    assert sql_prob.starter_code["sql"].startswith("-- Write your query")
    assert len(sql_prob.test_cases) >= 2
    assert verify_coding_quality(sql_prob) is True

    # Sandbox execution check on SQL problem
    res = CodeRunner.execute(
        code=sql_prob.reference_solution,
        language="sql",
        test_cases=sql_prob.test_cases,
    )
    assert res.verdict == "ACCEPTED"
    assert res.score == 100.0


def test_procedural_coding_generation_python():
    provider = ProceduralAIProvider()
    py_prob = provider.generate_coding(field="Python", difficulty="MEDIUM", language="python")
    assert isinstance(py_prob, GeneratedCodingProblem)
    assert py_prob.language == "python"
    assert "python" in py_prob.starter_code
    assert verify_coding_quality(py_prob) is True

    # Sandbox execution check
    res = CodeRunner.execute(
        code=py_prob.reference_solution,
        language="python",
        test_cases=py_prob.test_cases,
    )
    assert res.verdict == "ACCEPTED"
    assert res.score == 100.0


def test_verified_pool_manager():
    pool = VerifiedPoolManager(target_per_bucket=2)
    counts = pool.get_pool_counts()
    assert len(counts) > 0

    item = pool.get_question(field="Python", mode="MCQ", difficulty="MEDIUM")
    assert item is not None
    assert item.get("provenance", {}).get("served_from") == "pool"


def test_ai_gateway_never_fail_ladder():
    gateway = AIGateway()

    # 1. Normal generation serves from verified pool or live/procedural
    q = gateway.generate_practice_problem(field="SQL", difficulty="MEDIUM", mode="CODING")
    assert q is not None
    assert "title" in q
    assert q.get("language") == "sql"
    assert "sql" in q.get("starter_code", {})

    # 2. Trip circuit breaker: gateway must still return valid question without 500
    gateway.circuit_breaker.trip()
    assert gateway.circuit_breaker.state == "OPEN"

    q_tripped = gateway.generate_practice_problem(field="Python", difficulty="HARD", mode="MCQ")
    assert q_tripped is not None
    assert len(q_tripped["options"]) == 4

    # 3. Health metrics reflect degraded/down status with alert
    metrics = gateway.get_health_metrics()
    assert metrics.circuit_breaker_state == "OPEN"
    assert len(metrics.alerts) > 0

    # Reset
    gateway.circuit_breaker.reset()
    assert gateway.circuit_breaker.state == "CLOSED"


def test_procedural_output_never_labeled_as_model_output():
    """CI Integrity Check (Phase A): Procedural output MUST NEVER be labeled as model output."""
    provider = ProceduralAIProvider()
    mcq = provider.generate_mcq(field="Python")
    assert mcq.source != "model", "Procedural MCQ was untruthfully labeled as 'model'"
    assert mcq.provenance.provider == "procedural"
    assert mcq.source in ("procedural", "curated")

    coding = provider.generate_coding(field="SQL")
    assert coding.source != "model", "Procedural Coding problem was untruthfully labeled as 'model'"
    assert coding.provenance.provider == "procedural"
    assert coding.source in ("procedural", "curated")

    # Gateway fallback check
    gateway = AIGateway()
    gateway.circuit_breaker.trip()  # force offline
    problem = gateway.generate_practice_problem(field="Java", mode="CODING")
    assert problem["source"] != "model", "Gateway fallback was untruthfully labeled as 'model'"
    assert problem.get("provenance", {}).get("provider") == "procedural"
    gateway.circuit_breaker.reset()
