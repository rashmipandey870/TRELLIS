"""Thread-safe circuit breaker for TRELLIS AI Gateway."""

from __future__ import annotations

import logging
import threading
import time
from typing import Literal

logger = logging.getLogger(__name__)


class CircuitBreaker:
    """Protects against cascading AI provider failures with auto-recovery and manual controls."""

    def __init__(
        self,
        name: str = "ai_gateway",
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
    ) -> None:
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self._state: Literal["CLOSED", "OPEN", "HALF_OPEN"] = "CLOSED"
        self._failure_count: int = 0
        self._last_failure_time: float = 0.0
        self._last_state_change: float = time.time()
        self._lock = threading.Lock()

    @property
    def state(self) -> Literal["CLOSED", "OPEN", "HALF_OPEN"]:
        with self._lock:
            if self._state == "OPEN":
                now = time.time()
                if now - self._last_failure_time >= self.recovery_timeout:
                    logger.info("CircuitBreaker '%s' entering HALF_OPEN state.", self.name)
                    self._state = "HALF_OPEN"
                    self._last_state_change = now
            return self._state

    def is_allowed(self) -> bool:
        """Check whether requests can proceed through the circuit."""
        current_state = self.state
        return current_state in ("CLOSED", "HALF_OPEN")

    def record_success(self) -> None:
        """Record successful upstream request."""
        with self._lock:
            if self._state in ("HALF_OPEN", "OPEN"):
                logger.info("CircuitBreaker '%s' recovered to CLOSED state.", self.name)
            self._state = "CLOSED"
            self._failure_count = 0

    def record_failure(self, error: Exception | None = None) -> None:
        """Record upstream error and transition to OPEN if threshold breached."""
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()
            if self._state == "HALF_OPEN" or self._failure_count >= self.failure_threshold:
                if self._state != "OPEN":
                    logger.warning(
                        "CircuitBreaker '%s' TRIPPED to OPEN after %s consecutive failures: %s",
                        self.name,
                        self._failure_count,
                        error,
                    )
                self._state = "OPEN"
                self._last_state_change = self._last_failure_time

    def trip(self) -> None:
        """Manually trip the circuit breaker (operator action)."""
        with self._lock:
            self._state = "OPEN"
            self._last_failure_time = time.time()
            self._last_state_change = self._last_failure_time
            logger.warning("CircuitBreaker '%s' MANUALLY TRIPPED by operator.", self.name)

    def reset(self) -> None:
        """Manually reset the circuit breaker (operator action)."""
        with self._lock:
            self._state = "CLOSED"
            self._failure_count = 0
            self._last_state_change = time.time()
            logger.info("CircuitBreaker '%s' MANUALLY RESET by operator.", self.name)
