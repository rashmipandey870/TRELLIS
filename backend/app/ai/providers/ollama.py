"""Self-hosted Ollama AI provider for TRELLIS."""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
from typing import Any

from app.ai.providers.base import BaseAIProvider
from app.core.config import settings

logger = logging.getLogger(__name__)


class OllamaProvider(BaseAIProvider):
    """Integrates with local/containerized Ollama model server."""

    def __init__(
        self,
        base_url: str | None = None,
        default_instruct_model: str = "llama3:8b",
        default_code_model: str = "deepseek-coder:6.7b",
    ) -> None:
        self.base_url = (
            base_url
            or os.getenv("OLLAMA_BASE_URL")
            or getattr(settings, "OLLAMA_BASE_URL", "http://localhost:11434")
        ).rstrip("/")
        self.default_instruct_model = os.getenv("AI_INSTRUCT_MODEL", default_instruct_model)
        self.default_code_model = os.getenv("AI_CODE_MODEL", default_code_model)

    @property
    def name(self) -> str:
        return "ollama"

    def health_check(self) -> bool:
        url = f"{self.base_url}/api/tags"
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                return resp.status == 200
        except Exception:
            return False

    def generate_text(
        self,
        prompt: str,
        timeout: float = 30.0,
        model: str | None = None,
    ) -> str:
        target_model = model or self.default_instruct_model
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": target_model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.3},
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body.get("response", "")

    def generate_chat(
        self,
        messages: list[dict[str, str]],
        timeout: float = 30.0,
        model: str | None = None,
    ) -> str:
        target_model = model or self.default_instruct_model
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": target_model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.4},
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body.get("message", {}).get("content", "")
