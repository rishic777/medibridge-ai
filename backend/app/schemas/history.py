import uuid

from pydantic import BaseModel

from app.schemas.symptom import SymptomOut


class VerificationBadge(BaseModel):
    """
    Drives the three-layer UI badge:
    patient_reported -> document_supported -> physician_verified
    """
    status: str  # "patient_reported" | "document_supported" | "physician_verified"
    verified_by: str | None = None


class PatientHistoryOut(BaseModel):
    patient_id: uuid.UUID
    chief_complaint: str | None
    symptoms: list[SymptomOut]
    red_flags: list[str]
    ai_summary: str | None


class HistoryVerifyRequest(BaseModel):
    information_id: uuid.UUID
    information_type: str
    status: str  # "document_supported" | "physician_verified"
    verified_by: uuid.UUID | None = None


class ConversationMessageIn(BaseModel):
    text: str
    input_mode: str = "text"  # "text" | "voice"


class ConversationMessageOut(BaseModel):
    role: str
    content: str
    next_question: dict | None = None
