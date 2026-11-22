"""Cloud AI provider adapter (Anthropic / OpenAI / Gemini compatible) for TRELLIS."""

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


class CloudProvider(BaseAIProvider):
    """Integrates with standard OpenAI/Anthropic compatible HTTP APIs."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str = "gpt-4o-mini",
    ) -> None:
        self.api_key = api_key or os.getenv("AI_API_KEY") or getattr(settings, "AI_API_KEY", "")
        self.base_url = (
            base_url
            or os.getenv("AI_API_BASE")
            or "https://api.openai.com/v1"
        ).rstrip("/")
        self.model = os.getenv("AI_CLOUD_MODEL", model)

    @property
    def name(self) -> str:
        return "cloud"

    def health_check(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 5)

    def generate_text(
        self,
        prompt: str,
        timeout: float = 30.0,
        model: str | None = None,
    ) -> str:
        if not self.health_check():
            raise RuntimeError("Cloud provider API key not configured")

        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model or self.model,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"},
            "temperature": 0.3,
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            choices = body.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "")
            return ""

    def generate_chat(
        self,
        messages: list[dict[str, str]],
        timeout: float = 30.0,
        model: str | None = None,
    ) -> str:
        if not self.health_check():
            raise RuntimeError("Cloud provider API key not configured")

        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model or self.model,
            "messages": messages,
            "temperature": 0.5,
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            choices = body.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "")
            return ""
