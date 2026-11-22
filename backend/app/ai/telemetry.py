"""Telemetry, metrics tracking, and PII redaction for TRELLIS AI Gateway."""

from __future__ import annotations

import collections
import re
import threading
import time
from typing import Any

# PII redaction regular expressions
_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_PHONE_RE = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")
_BEARER_RE = re.compile(r"(Bearer\s+)[A-Za-z0-9\-._~+/]+=*", re.IGNORECASE)
_API_KEY_RE = re.compile(r"(api[_-]?key[:=]\s*['\"]?)[A-Za-z0-9_\-]{16,}(['\"]?)", re.IGNORECASE)
_PASSWORD_RE = re.compile(r"(password[:=]\s*['\"]?)[^\s'\"]{6,}(['\"]?)", re.IGNORECASE)


def redact_pii(text: str) -> str:
    """Scrub PII, credentials, and sensitive tokens from AI logs and telemetry."""
    if not text:
        return ""
    scrubbed = _EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    scrubbed = _PHONE_RE.sub("[REDACTED_PHONE]", scrubbed)
    scrubbed = _BEARER_RE.sub(r"\1[REDACTED_TOKEN]", scrubbed)
    scrubbed = _API_KEY_RE.sub(r"\1[REDACTED_KEY]\2", scrubbed)
    scrubbed = _PASSWORD_RE.sub(r"\1[REDACTED_PASSWORD]\2", scrubbed)
    return scrubbed


class AITelemetry:
    """Thread-safe telemetry collector for AI Gateway performance and reliability."""

    def __init__(self, max_samples: int = 500) -> None:
        self.max_samples = max_samples
        self._latencies_ms: collections.deque[float] = collections.deque(maxlen=max_samples)
        self._total_requests: int = 0
        self._successful_requests: int = 0
        self._failed_requests: int = 0
        self._validation_failures: int = 0
        self._queue_depth: int = 0
        self._lock = threading.Lock()

    def record_request_start(self) -> float:
        with self._lock:
            self._total_requests += 1
            self._queue_depth += 1
        return time.perf_counter()

    def record_request_end(self, start_time: float, success: bool, validation_passed: bool = True) -> None:
        duration_ms = (time.perf_counter() - start_time) * 1000.0
        with self._lock:
            self._queue_depth = max(0, self._queue_depth - 1)
            self._latencies_ms.append(duration_ms)
            if success:
                self._successful_requests += 1
            else:
                self._failed_requests += 1

            if not validation_passed:
                self._validation_failures += 1

    def get_metrics(self) -> dict[str, Any]:
        with self._lock:
            total = self._total_requests
            success = self._successful_requests
            val_failures = self._validation_failures
            queue = self._queue_depth
            latencies = sorted(self._latencies_ms)

        if latencies:
            n = len(latencies)
            p50 = latencies[int(n * 0.50)]
            p95 = latencies[min(int(n * 0.95), n - 1)]
        else:
            p50 = 0.0
            p95 = 0.0

        success_rate = round((success / total * 100.0) if total > 0 else 100.0, 1)
        val_pass_rate = round(((total - val_failures) / total * 100.0) if total > 0 else 100.0, 1)

        return {
            "total_requests": total,
            "success_rate_percent": success_rate,
            "validation_pass_rate_percent": val_pass_rate,
            "p50_latency_ms": round(p50, 1),
            "p95_latency_ms": round(p95, 1),
            "queue_depth": queue,
        }
