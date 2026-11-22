"""In-memory verified question pool and background replenishment for TRELLIS AI Gateway."""

from __future__ import annotations

import collections
import logging
import threading
from typing import Any

from app.ai.prompts import PROMPT_VERSION
from app.ai.providers.procedural import ProceduralAIProvider
from app.ai.quality_gates import verify_coding_quality, verify_mcq_quality
from app.ai.schemas import Provenance

logger = logging.getLogger(__name__)


class VerifiedPoolManager:
    """Manages pre-verified problem queues to eliminate learner latency and prevent generation failures."""

    def __init__(self, target_per_bucket: int = 3) -> None:
        self.target_per_bucket = target_per_bucket
        self._pools: dict[str, collections.deque[dict[str, Any]]] = collections.defaultdict(collections.deque)
        self._lock = threading.Lock()
        self._procedural = ProceduralAIProvider()
        self._init_defaults()

    def _bucket_key(self, field: str, mode: str, difficulty: str = "MEDIUM") -> str:
        return f"{field.strip().lower()}:{mode.strip().lower()}:{difficulty.strip().lower()}"

    def _init_defaults(self) -> None:
        """Pre-populate core buckets on startup so questions are available instantly."""
        core_fields = ["Python", "SQL", "Java", "JavaScript", "DSA", "Web Dev", "Cloud", "Aptitude"]
        for field in core_fields:
            for mode in ["MCQ", "CODING"]:
                if mode == "CODING" and field in ("Aptitude", "Cloud"):
                    continue
                key = self._bucket_key(field, mode, "MEDIUM")
                self._fill_bucket(field, mode, "MEDIUM", count=2)

    def _fill_bucket(self, field: str, mode: str, difficulty: str, count: int) -> None:
        key = self._bucket_key(field, mode, difficulty)
        for _ in range(count):
            try:
                if mode.upper() == "MCQ":
                    prob = self._procedural.generate_mcq(field=field, difficulty=difficulty)
                    if verify_mcq_quality(prob):
                        prob.provenance.served_from = "pool"
                        with self._lock:
                            self._pools[key].append(prob.model_dump())
                else:
                    lang = "sql" if "sql" in field.lower() else ("java" if "java" in field.lower() else ("javascript" if "javascript" in field.lower() or "web" in field.lower() else "python"))
                    prob = self._procedural.generate_coding(field=field, difficulty=difficulty, language=lang)
                    if verify_coding_quality(prob):
                        prob.provenance.served_from = "pool"
                        with self._lock:
                            self._pools[key].append(prob.model_dump())
            except Exception as e:
                logger.warning("Error pre-filling bucket '%s': %s", key, e)

    def get_question(self, field: str, mode: str, difficulty: str = "MEDIUM") -> dict[str, Any] | None:
        """Retrieve a verified question from the pool and trigger background refill if needed."""
        key = self._bucket_key(field, mode, difficulty)
        item: dict[str, Any] | None = None
        with self._lock:
            q = self._pools.get(key)
            if q and len(q) > 0:
                item = q.popleft()

        # If pool is running low, replenish in background
        with self._lock:
            current_len = len(self._pools.get(key, []))

        if current_len < self.target_per_bucket:
            threading.Thread(
                target=self._fill_bucket,
                args=(field, mode, difficulty, self.target_per_bucket - current_len),
                daemon=True,
            ).start()

        if item:
            item.setdefault("provenance", {})["served_from"] = "pool"
        return item

    def get_pool_counts(self) -> dict[str, int]:
        """Return snapshot of current verified question counts per bucket."""
        with self._lock:
            return {k: len(v) for k, v in self._pools.items() if len(v) > 0}

    def refill_all(self) -> None:
        """Trigger refill for all buckets."""
        core_fields = ["Python", "SQL", "Java", "JavaScript", "DSA", "Web Dev", "Cloud", "Aptitude"]
        for field in core_fields:
            for mode in ["MCQ", "CODING"]:
                if mode == "CODING" and field in ("Aptitude", "Cloud"):
                    continue
                self._fill_bucket(field, mode, "MEDIUM", count=2)
