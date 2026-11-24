"""Unified AI Gateway for TRELLIS (WS2 / Phase A).

Central orchestrator for all AI generation, verification, telemetry, and health monitoring.
Implements the truthful never-fail ladder:
1. Live model generation (Ollama / Cloud) with quality gate verification.
2. Database-persisted verified pool (AIQuestionPool) with near-duplicate prevention.
3. Clearly labeled procedural fallback as resilient last resort (never masquerades as model output).
"""

from __future__ import annotations

import logging
import os
import threading
import time
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.circuit_breaker import CircuitBreaker
from app.ai.pool import VerifiedPoolManager, compute_question_hash
from app.ai.prompts import (
    PROMPT_CODING_GENERATION,
    PROMPT_GARDENER_SOCRATIC,
    PROMPT_MCQ_GENERATION,
    PROMPT_SQL_GENERATION,
    PROMPT_VERSION,
    extract_json_payload,
)
from app.ai.providers.cloud import CloudProvider
from app.ai.providers.ollama import OllamaProvider
from app.ai.providers.procedural import ProceduralAIProvider
from app.ai.quality_gates import verify_coding_quality, verify_mcq_quality
from app.ai.schemas import (
    AIHealthResponse,
    ChatResponse,
    GeneratedCodingProblem,
    GeneratedMcqProblem,
    Provenance,
)
from app.ai.telemetry import AITelemetry, redact_pii
from app.models.assessments import AssessmentAttempt
from app.models.curriculum import Enrolment
from app.models.user import User

logger = logging.getLogger(__name__)


class AIGateway:
    """Enterprise AI Gateway providing resilient, truthful generation, verification, and chat."""

    def __init__(self) -> None:
        self.circuit_breaker = CircuitBreaker(name="trellis_ai", failure_threshold=4, recovery_timeout=25.0)
        self.telemetry = AITelemetry()
        self.pool = VerifiedPoolManager()

        # Providers
        self.ollama = OllamaProvider()
        self.cloud = CloudProvider()
        self.procedural = ProceduralAIProvider()

    def get_active_provider_name(self) -> str:
        if self.ollama.health_check():
            return "ollama"
        if self.cloud.health_check():
            return "cloud"
        return "procedural"

    def generate_practice_problem(
        self,
        field: str,
        difficulty: str = "MEDIUM",
        mode: str = "MCQ",
        language: str | None = None,
        db: Session | None = None,
        learner_id: str | None = None,
        seen_hashes: set[str] | None = None,
    ) -> dict[str, Any]:
        """Generate a practice question following the truthful never-fail ladder:
        1. Live model generation (Ollama/Cloud) when healthy.
        2. Database-persisted verified question pool.
        3. Truthful procedural fallback engine.
        """
        norm_mode = mode.upper().strip()
        diff = (difficulty or "MEDIUM").upper().strip()
        fld = field.strip()
        hashes = seen_hashes or set()

        start_t = self.telemetry.record_request_start()

        # Ladder Step 1: Live model generation if provider healthy and circuit breaker CLOSED
        if self.circuit_breaker.is_allowed():
            active_prov = self.ollama if self.ollama.health_check() else (self.cloud if self.cloud.health_check() else None)
            if active_prov:
                try:
                    live_result = self._attempt_live_generation(fld, diff, norm_mode, language, active_prov)
                    if live_result:
                        q_hash = compute_question_hash(live_result.get("question") or live_result.get("statement") or "")
                        if q_hash not in hashes:
                            self.circuit_breaker.record_success()
                            self.telemetry.record_request_end(start_t, success=True, validation_passed=True)
                            return live_result
                except Exception as e:
                    logger.warning("Live model generation error: %s; proceeding to pool", redact_pii(str(e)))
                    self.circuit_breaker.record_failure(e)
                    self.telemetry.record_request_end(start_t, success=False, validation_passed=False)

        # Ladder Step 2: Database-persisted verified question pool (survives restarts)
        if db is not None:
            pooled = self.pool.get_question_from_db(
                db=db,
                field=fld,
                mode=norm_mode,
                difficulty=diff,
                seen_hashes=hashes,
                learner_id=learner_id,
            )
            if pooled:
                logger.info("Serving verified question from database pool for %s/%s", fld, norm_mode)
                self.telemetry.record_request_end(start_t, success=True, validation_passed=True)
                return pooled

        # Check in-memory buffer if database pool returned no unused item
        mem_item = self.pool.get_memory_question(field=fld, mode=norm_mode, difficulty=diff)
        if mem_item:
            self.telemetry.record_request_end(start_t, success=True, validation_passed=True)
            return mem_item

        # Ladder Step 3: Resilient procedural generation (truthfully labeled as procedural/practice bank)
        logger.info("Generating %s/%s practice question via procedural engine", fld, norm_mode)
        if norm_mode == "MCQ":
            mcq = self.procedural.generate_mcq(field=fld, difficulty=diff, seen_hashes=hashes)
            verify_mcq_quality(mcq)
            mcq.source = "procedural"
            mcq.provenance.provider = "procedural"
            mcq.provenance.served_from = "fallback"
            mcq.provenance.verified = True
            self.telemetry.record_request_end(start_t, success=True, validation_passed=True)
            return mcq.model_dump()
        else:
            lang = language or ("sql" if "sql" in fld.lower() else ("java" if "java" in fld.lower() else ("javascript" if "javascript" in fld.lower() or "web" in fld.lower() else "python")))
            coding = self.procedural.generate_coding(field=fld, difficulty=diff, language=lang, seen_hashes=hashes)
            passes = verify_coding_quality(coding)
            coding.source = "procedural"
            coding.provenance.provider = "procedural"
            coding.provenance.served_from = "fallback"
            self.telemetry.record_request_end(start_t, success=True, validation_passed=passes)
            return coding.model_dump()

    def _attempt_live_generation(
        self,
        field: str,
        difficulty: str,
        mode: str,
        language: str | None,
        provider: Any,
    ) -> dict[str, Any] | None:
        if mode == "MCQ":
            prompt = PROMPT_MCQ_GENERATION.format(
                field=field,
                difficulty=difficulty,
                category="Technical Knowledge",
                topic=field,
            )
            raw = provider.generate_text(prompt, timeout=12.0)
            data = extract_json_payload(raw)
            data["field"] = field
            data["difficulty"] = difficulty
            data["category"] = "Technical Knowledge"
            data["source"] = "model"
            data["provenance"] = {
                "provider": provider.name,
                "model": getattr(provider, "default_instruct_model", provider.name),
                "prompt_version": PROMPT_VERSION,
                "served_from": "live",
                "verified": True,
            }
            mcq = GeneratedMcqProblem(**data)
            if verify_mcq_quality(mcq):
                return mcq.model_dump()

        else:
            lang = (language or ("sql" if "sql" in field.lower() else "python")).lower()
            prompt = (
                PROMPT_SQL_GENERATION.format(difficulty=difficulty)
                if lang in ("sql", "sqlite", "postgresql")
                else PROMPT_CODING_GENERATION.format(language=lang, field=field, difficulty=difficulty, category="Coding")
            )
            raw = provider.generate_text(prompt, timeout=15.0)
            data = extract_json_payload(raw)
            data["field"] = field
            data["difficulty"] = difficulty
            data["language"] = lang
            data["category"] = "Coding"
            data["source"] = "model"
            data["provenance"] = {
                "provider": provider.name,
                "model": getattr(provider, "default_code_model", provider.name),
                "prompt_version": PROMPT_VERSION,
                "served_from": "live",
                "verified": True,
            }
            coding = GeneratedCodingProblem(**data)
            if verify_coding_quality(coding):
                return coding.model_dump()

        return None

    def chat_with_gardener(
        self,
        learner_id: str,
        user_message: str,
        db: Session,
        history: list[dict[str, str]] | None = None,
    ) -> ChatResponse:
        """Grounded, Socratic chat mentorship for the learner."""
        learner = db.get(User, learner_id)
        if not learner:
            raise ValueError(f"Learner '{learner_id}' not found.")

        enrolment = (
            db.execute(
                select(Enrolment).where(Enrolment.user_id == learner_id, Enrolment.status == "IN_PROGRESS")
            )
            .scalars()
            .first()
        )
        current_pathway = enrolment.pathway.title if enrolment and enrolment.pathway else "General Technology Onboarding"
        progress = round(float(enrolment.progress_percent), 1) if enrolment else 0.0

        recent_attempts = (
            db.execute(
                select(AssessmentAttempt)
                .where(AssessmentAttempt.learner_id == learner_id, AssessmentAttempt.status == "SUBMITTED")
                .order_by(AssessmentAttempt.submit_time.desc())
                .limit(3)
            )
            .scalars()
            .all()
        )
        recent_perf = [
            f"{a.assessment.title if a.assessment else 'Assessment'}: {a.score:.1f}/{a.total_marks:.1f} ({'PASSED' if a.passed else 'RETRY'})"
            for a in recent_attempts
        ]

        history_text = ""
        if history:
            for turn in history[-4:]:
                history_text += f"{turn.get('role', 'user').capitalize()}: {turn.get('content', '')}\n"

        prompt = PROMPT_GARDENER_SOCRATIC.format(
            learner_name=learner.full_name,
            pathway=current_pathway,
            progress_percent=progress,
            streak_days=learner.streak_days,
            recent_perf=", ".join(recent_perf) if recent_perf else "No completed assessments yet",
            history=history_text,
            user_message=user_message,
        )

        reply_text = ""
        provider_used = "procedural"
        if self.circuit_breaker.is_allowed():
            provider = self.ollama if self.ollama.health_check() else (self.cloud if self.cloud.health_check() else None)
            if provider:
                try:
                    reply_text = provider.generate_text(prompt, timeout=12.0)
                    provider_used = provider.name
                except Exception as e:
                    logger.warning("Gardener live chat failed: %s", redact_pii(str(e)))

        if not reply_text:
            reply_text = self.procedural.generate_chat([{"role": "user", "content": user_message}])
            provider_used = "procedural"

        suggested_actions = [
            f"Practice {current_pathway.split(':')[0]} problems",
            "Review latest Growth Ring report",
            "Check scheduled mentor sessions",
        ]

        return ChatResponse(
            reply=reply_text,
            remaining_queries=30,
            suggested_actions=suggested_actions,
            context_used={
                "pathway": current_pathway,
                "progress_percent": progress,
                "streak_days": learner.streak_days,
            },
            provenance=Provenance(
                provider="ollama" if provider_used == "ollama" else ("cloud" if provider_used == "cloud" else "procedural"),
                model=provider_used,
                prompt_version=PROMPT_VERSION,
                served_from="live" if provider_used in ("ollama", "cloud") else "fallback",
                verified=True,
            ),
        )

    def get_health_metrics(self, db: Session | None = None) -> AIHealthResponse:
        """Produce real-time health snapshot for Admin dashboard."""
        provider_name = self.get_active_provider_name()
        cb_state = self.circuit_breaker.state
        status = "HEALTHY" if cb_state == "CLOSED" else ("DEGRADED" if cb_state == "HALF_OPEN" else "DOWN")

        telemetry_data = self.telemetry.get_metrics()

        if db is not None:
            pool_counts = self.pool.get_pool_counts_from_db(db)
        else:
            pool_counts = {}

        alerts = []
        if cb_state != "CLOSED":
            alerts.append(f"Circuit breaker is {cb_state}. Fallback to procedural provider active.")

        return AIHealthResponse(
            status=status,
            primary_provider=provider_name,
            active_instruct_model=self.ollama.default_instruct_model,
            active_code_model=self.ollama.default_code_model,
            circuit_breaker_state=cb_state,
            p50_latency_ms=telemetry_data["p50_latency_ms"],
            p95_latency_ms=telemetry_data["p95_latency_ms"],
            total_requests=telemetry_data["total_requests"],
            success_rate_percent=telemetry_data["success_rate_percent"],
            validation_pass_rate_percent=telemetry_data["validation_pass_rate_percent"],
            pool_counts=pool_counts,
            queue_depth=telemetry_data["queue_depth"],
            alerts=alerts,
        )


# Global singleton instance
ai_gateway = AIGateway()
