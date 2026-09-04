import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SymptomCreate(BaseModel):
    name: str
    duration: str | None = None
    severity: str | None = None
    source: str = "patient_reported"
    confidence: float = 0.6


class SymptomOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    patient_id: uuid.UUID
    name: str
    duration: str | None
    severity: str | None
    source: str
    confidence: float
    created_at: datetime
