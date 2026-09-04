"""
Language guardrails: the system must never present AI output as a
diagnosis. Anything shown to a patient or clinician passes through here.
"""
from __future__ import annotations

import re

# Phrases the system must never emit toward a patient.
_DIAGNOSTIC_PATTERNS = [
    re.compile(r"\byou have\s+(?!been|not)\w", re.IGNORECASE),
    re.compile(r"\byou are diagnosed with\b", re.IGNORECASE),
    re.compile(r"\bthis (is|means) (a|an)\s+\w+ (disease|condition|infection)\b", re.IGNORECASE),
]

SAFE_RED_FLAG_MESSAGE_TEMPLATE = "Potential red flag detected — clinician assessment recommended."


def sanitize_patient_facing_text(text: str) -> str:
    """Strip/replace diagnostic-sounding language before it reaches a patient."""
    cleaned = text
    for pattern in _DIAGNOSTIC_PATTERNS:
        cleaned = pattern.sub("this may be relevant and", cleaned)
    return cleaned


def is_diagnostic_language(text: str) -> bool:
    return any(pattern.search(text) for pattern in _DIAGNOSTIC_PATTERNS)


def format_red_flag_message(rule: dict) -> str:
    """
    Always prefer the rule's own clinician-reviewed message; fall back to
    the safe generic template rather than ever inventing wording.
    """
    return rule.get("message") or SAFE_RED_FLAG_MESSAGE_TEMPLATE
