"""
Safety / red-flag engine.

Rules are config-driven (see /config/red_flags/rules.json) so clinical
staff can add or adjust rules without a code deploy. The engine flags
symptom combinations for clinician attention -- it never outputs a
diagnosis (see safety/validators.py for the language guardrails).
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from app.core.config import settings


class RedFlagEngine:
    def __init__(self, rules_dir: Path | None = None):
        self.rules_dir = rules_dir or settings.RED_FLAGS_DIR

    @lru_cache(maxsize=1)
    def _load_rules(self) -> list[dict]:
        rules_file = self.rules_dir / "rules.json"
        if not rules_file.exists():
            return []
        data = json.loads(rules_file.read_text())
        return data.get("rules", [])

    def evaluate(self, present_symptom_ids: set[str]) -> list[dict]:
        """
        present_symptom_ids: normalized symptom/condition tags extracted
        from the conversation, e.g. {"chest_pain", "breathing_difficulty"}.

        Returns the list of rule dicts whose `conditions` are all present.
        """
        hits = []
        for rule in self._load_rules():
            conditions = set(rule.get("conditions", []))
            if conditions and conditions.issubset(present_symptom_ids):
                hits.append(rule)
        return hits


red_flag_engine = RedFlagEngine()
