"""Abstract base interface for AI providers in TRELLIS."""

from __future__ import annotations

import abc
from typing import Any


class BaseAIProvider(abc.ABC):
    """Abstract interface for LLM backends (Ollama, Cloud, Procedural)."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Provider identifier."""
        raise NotImplementedError

    @abc.abstractmethod
    def generate_text(
        self,
        prompt: str,
        timeout: float = 30.0,
        model: str | None = None,
    ) -> str:
        """Generate raw text response from prompt."""
        raise NotImplementedError

    @abc.abstractmethod
    def generate_chat(
        self,
        messages: list[dict[str, str]],
        timeout: float = 30.0,
        model: str | None = None,
    ) -> str:
        """Generate conversational reply given structured message turns."""
        raise NotImplementedError

    @abc.abstractmethod
    def health_check(self) -> bool:
        """Verify upstream provider availability."""
        raise NotImplementedError
