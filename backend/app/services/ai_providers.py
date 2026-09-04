"""
AI provider abstraction.

The rest of the application never imports Gemini/OpenAI/etc. directly --
it talks to `AIProvider`. Swapping providers means editing this file only
(and AI_PROVIDER in .env), nothing in api/, services/, or the frontend.
"""
from __future__ import annotations

import json
from abc import ABC, abstractmethod

from app.core.config import settings
from app.core.logging import logger


class AIProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Return a raw text completion for the given prompt."""
        raise NotImplementedError

    async def generate_json(self, prompt: str) -> dict:
        """Convenience wrapper: ask for JSON and parse it defensively."""
        raw = await self.generate(prompt)
        try:
            start = raw.index("{")
            end = raw.rindex("}") + 1
            return json.loads(raw[start:end])
        except (ValueError, json.JSONDecodeError):
            logger.warning("AI provider returned non-JSON output, falling back to empty dict")
            return {}


class GeminiProvider(AIProvider):
    """Google Gemini implementation. Requires AI_API_KEY in .env."""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    async def generate(self, prompt: str) -> str:
        import httpx

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={self.api_key}"
        )
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]


class OpenAIProvider(AIProvider):
    """OpenAI implementation. Requires AI_API_KEY in .env."""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    async def generate(self, prompt: str) -> str:
        import httpx

        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]


class LocalModelProvider(AIProvider):
    """
    Offline, dependency-free stand-in used when AI_PROVIDER=local (the
    default, so the prototype runs with no API key). Good enough to
    demo the pipeline end-to-end; swap for Gemini/OpenAI for real
    extraction quality.
    """

    async def generate(self, prompt: str) -> str:
        logger.info("LocalModelProvider.generate called (stub, no external call)")
        return "{}"


def get_ai_provider() -> AIProvider:
    provider = settings.AI_PROVIDER.lower()
    if provider == "gemini":
        return GeminiProvider(settings.AI_API_KEY, settings.AI_MODEL)
    if provider == "openai":
        return OpenAIProvider(settings.AI_API_KEY, settings.AI_MODEL)
    return LocalModelProvider()
