"""Pydantic schemas and output contracts for TRELLIS AI Gateway."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal
from pydantic import BaseModel, Field, model_validator


class Provenance(BaseModel):
    """Provenance and audit tracking metadata for every AI artifact."""
    model: str = Field(default="trellis-ai-v1")
    prompt_version: str = Field(default="1.2.0")
    served_from: Literal["live", "pool", "verified_fallback"] = Field(default="live")
    generated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class GeneratedMcqProblem(BaseModel):
    """Schema for AI-generated Multiple Choice Questions."""
    title: str = Field(..., min_length=2, max_length=255)
    question: str = Field(..., min_length=5)
    options: list[str] = Field(..., min_length=4, max_length=4)
    correct_answer: str = Field(..., min_length=1)
    explanation: str = Field(..., min_length=5)
    hints: list[str] = Field(default_factory=list)
    field: str
    difficulty: str = Field(default="MEDIUM")
    category: str = Field(default="Technical Knowledge")
    topic: str | None = None
    solver_verification: dict[str, Any] | None = None
    provenance: Provenance = Field(default_factory=Provenance)

    @model_validator(mode="after")
    def validate_options_and_answer(self) -> "GeneratedMcqProblem":
        if len(self.options) != 4:
            raise ValueError("MCQ must have exactly 4 options.")
        if len(set(self.options)) != 4:
            raise ValueError("MCQ options must be distinct.")
        if self.correct_answer not in self.options:
            raise ValueError(
                f"correct_answer '{self.correct_answer}' must match one of the 4 options: {self.options}"
            )
        return self


class GeneratedCodingProblem(BaseModel):
    """Schema for AI-generated Coding and SQL problems."""
    title: str = Field(..., min_length=2, max_length=255)
    question: str = Field(..., min_length=5)
    field: str
    difficulty: str = Field(default="MEDIUM")
    language: str = Field(default="python")  # python, sql, java, javascript, cpp
    constraints: str | None = None
    examples: list[dict[str, Any]] = Field(default_factory=list)
    starter_code: dict[str, str] = Field(default_factory=dict)
    reference_solution: str = Field(..., min_length=5)
    wrong_stub: str | None = None
    test_cases: list[dict[str, Any]] = Field(..., min_length=2)
    explanation: str = Field(..., min_length=5)
    hints: list[str] = Field(default_factory=list)
    category: str = Field(default="Coding")
    provenance: Provenance = Field(default_factory=Provenance)

    @model_validator(mode="after")
    def validate_starter_code_and_cases(self) -> "GeneratedCodingProblem":
        # Ensure starter code maps to the correct language key
        lang_key = self.language.lower().strip()
        if lang_key not in self.starter_code:
            if lang_key in ("sql", "sqlite", "postgresql"):
                self.starter_code["sql"] = "-- Write your SQL query here\nSELECT "
            elif lang_key == "java":
                self.starter_code["java"] = (
                    "public class Solution {\n    public static void main(String[] args) {\n        // Your code here\n    }\n}"
                )
            elif lang_key in ("javascript", "js"):
                self.starter_code["javascript"] = "function solve() {\n    // Your code here\n}"
            else:
                self.starter_code["python"] = "def solve():\n    pass"

        # Validate test cases have input_data and expected_output
        for idx, tc in enumerate(self.test_cases):
            if "expected_output" not in tc:
                raise ValueError(f"Test case #{idx} missing required key 'expected_output'")
        return self


class GeneratedSubjectiveProblem(BaseModel):
    """Schema for AI-generated Subjective, Scenario, or Communication questions."""
    title: str = Field(..., min_length=2, max_length=255)
    question: str = Field(..., min_length=10)
    field: str
    difficulty: str = Field(default="MEDIUM")
    category: str = Field(default="English & Communication")
    sample_solution: str = Field(..., min_length=10)
    rubric: list[dict[str, Any]] = Field(..., min_length=1)  # list of {criterion, weight, description}
    hints: list[str] = Field(default_factory=list)
    provenance: Provenance = Field(default_factory=Provenance)


class ChatResponse(BaseModel):
    """Schema for Gardener and role-based chat responses."""
    reply: str
    remaining_queries: int
    suggested_actions: list[str] = Field(default_factory=list)
    context_used: dict[str, Any] = Field(default_factory=dict)
    provenance: Provenance = Field(default_factory=Provenance)


class AIHealthResponse(BaseModel):
    """Schema for Admin AI Health dashboard and monitoring."""
    status: Literal["HEALTHY", "DEGRADED", "DOWN"]
    primary_provider: str
    active_instruct_model: str
    active_code_model: str
    circuit_breaker_state: Literal["CLOSED", "OPEN", "HALF_OPEN"]
    p50_latency_ms: float
    p95_latency_ms: float
    total_requests: int
    success_rate_percent: float
    validation_pass_rate_percent: float
    pool_counts: dict[str, int]
    queue_depth: int
    alerts: list[str] = Field(default_factory=list)
