import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PatientCreate(BaseModel):
    name: str
    age: int | None = None
    gender: str | None = None
    preferred_language: str = "en"


class PatientOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    age: int | None
    gender: str | None
    preferred_language: str
    created_at: datetime
