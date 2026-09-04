"""
Speech-to-text / text-to-speech abstraction, mirroring the AIProvider
pattern so ASR vendors can be swapped without touching callers.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from app.core.config import settings


class SpeechProvider(ABC):
    @abstractmethod
    async def transcribe(self, audio_bytes: bytes, language: str = "en") -> str:
        raise NotImplementedError


class BrowserWebSpeechProvider(SpeechProvider):
    """
    For the prototype, speech-to-text runs client-side via the Web Speech
    API in the browser (see frontend/src/hooks/useVoice.js) and only the
    resulting transcript is sent to the backend. This provider exists so
    a server-side ASR vendor can be dropped in later without changing the
    API contract.
    """

    async def transcribe(self, audio_bytes: bytes, language: str = "en") -> str:
        raise NotImplementedError(
            "Transcription happens client-side in this prototype. "
            "Implement a real provider (e.g. Whisper, Google STT) here to move it server-side."
        )


class SpeechService:
    def __init__(self, provider: SpeechProvider | None = None):
        self.provider = provider or BrowserWebSpeechProvider()

    async def transcribe(self, audio_bytes: bytes, language: str = "en") -> str:
        return await self.provider.transcribe(audio_bytes, language)
