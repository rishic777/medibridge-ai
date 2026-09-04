"""
High-level AI operations used by the API layer. This is the ONLY place
that builds prompts and calls an AIProvider -- api/ routers call these
methods, never AIProvider directly.
"""
from __future__ import annotations

from app.services.ai_providers import AIProvider, get_ai_provider
from app.services.question_service import QuestionService


class AIService:
    def __init__(self, provider: AIProvider | None = None, question_service: QuestionService | None = None):
        self.provider = provider or get_ai_provider()
        self.questions = question_service or QuestionService()

    async def extract_medical_information(self, text: str) -> dict:
        """
        Turn free-text patient speech into structured symptom data, e.g.:
        {"symptoms": [{"name": "fever", "duration": "3 days", "severity": "moderate"}]}
        """
        prompt = (
            "You are a medical intake assistant. Extract structured symptom "
            "information from the patient's message as JSON with a top-level "
            '"symptoms" array. Each item has name, duration, severity (if known). '
            "Do not diagnose. Respond with JSON only.\n\n"
            f"Patient message: {text}"
        )
        data = await self.provider.generate_json(prompt)
        return data if data else self._fallback_extraction(text)

    async def generate_next_question(self, condition: str, answered_ids: list[str]) -> dict | None:
        """Delegate to the config-driven question engine (see question_service.py)."""
        return self.questions.next_question(condition, answered_ids)

    async def summarize_history(self, patient_data: dict) -> str:
        prompt = (
            "Summarize this patient's intake data in plain, warm, non-technical "
            "language for a treating physician to skim in 10 seconds. Do not "
            "diagnose or speculate beyond what is stated.\n\n"
            f"Patient data: {patient_data}"
        )
        summary = await self.provider.generate(prompt)
        return summary.strip() or "No AI summary available yet."

    async def analyse_document(self, ocr_text: str) -> dict:
        prompt = (
            "Extract structured clinical findings (test name, value, unit, "
            "reference range, flag) from this lab report OCR text as JSON "
            'with a top-level "findings" array. JSON only.\n\n'
            f"OCR text: {ocr_text}"
        )
        return await self.provider.generate_json(prompt)

    @staticmethod
    def _fallback_extraction(text: str) -> dict:
        """
        Very small heuristic fallback so the demo still produces something
        useful when running with AI_PROVIDER=local and no model attached.
        """
        keywords = ["fever", "cough", "headache", "chest pain", "breathing", "vomiting", "fatigue"]
        found = [k for k in keywords if k in text.lower()]
        return {"symptoms": [{"name": k, "duration": None, "severity": None} for k in found]}
