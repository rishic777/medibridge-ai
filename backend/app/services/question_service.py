"""
Adaptive question engine. Questions live as JSON in /config/questions so a
non-programmer can add or edit them without touching backend code.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from app.core.config import settings


class QuestionService:
    def __init__(self, questions_dir: Path | None = None):
        self.questions_dir = questions_dir or settings.QUESTIONS_DIR

    @lru_cache(maxsize=32)
    def _load(self, condition: str) -> dict:
        path = self.questions_dir / f"{condition}.json"
        if not path.exists():
            return {"condition": condition, "questions": []}
        return json.loads(path.read_text())

    def next_question(self, condition: str, answered_ids: list[str]) -> dict | None:
        data = self._load(condition)
        questions = data.get("questions", [])
        # High-priority (safety-relevant) questions are asked first.
        ordered = sorted(questions, key=lambda q: 0 if q.get("priority") == "high" else 1)
        for question in ordered:
            if question["id"] not in answered_ids:
                return question
        return None

    def all_conditions(self) -> list[str]:
        if not self.questions_dir.exists():
            return []
        return [p.stem for p in self.questions_dir.glob("*.json")]
