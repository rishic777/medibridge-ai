"""
Assembles the structured patient history shown in the doctor dashboard,
combining symptoms, reports, and red-flag alerts, each tagged with a
verification layer (patient_reported / document_supported / physician_verified).
"""
from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.patient import Patient
from app.models.symptom import Symptom
from app.models.verification import VerificationRecord
from app.services.ai_service import AIService


class HistoryService:
    def __init__(self, db: Session, ai_service: AIService | None = None):
        self.db = db
        self.ai_service = ai_service or AIService()

    def get_patient_history(self, patient_id: uuid.UUID) -> dict:
        patient = self.db.get(Patient, patient_id)
        if patient is None:
            return {}

        symptoms = self.db.query(Symptom).filter(Symptom.patient_id == patient_id).all()
        alerts = self.db.query(Alert).filter(Alert.patient_id == patient_id).all()
        chief_complaint = symptoms[0].name if symptoms else None

        return {
            "patient_id": patient_id,
            "chief_complaint": chief_complaint,
            "symptoms": symptoms,
            "red_flags": [a.message for a in alerts],
            "ai_summary": None,  # populated on demand via /ai/summary to avoid a slow call on every page load
        }

    def record_verification(
        self,
        patient_id: uuid.UUID,
        information_type: str,
        information_id: uuid.UUID,
        status: str,
        verified_by: uuid.UUID | None = None,
    ) -> VerificationRecord:
        from datetime import datetime

        record = VerificationRecord(
            patient_id=patient_id,
            information_type=information_type,
            information_id=information_id,
            status=status,
            verified_by=verified_by,
            verified_at=datetime.utcnow() if status == "physician_verified" else None,
        )
        self.db.add(record)

        # Keep the underlying symptom's `source` column in sync so simple
        # reads (list endpoints) don't need to join verification_records.
        if information_type == "symptom":
            symptom = self.db.get(Symptom, information_id)
            if symptom is not None:
                symptom.source = status

        self.db.commit()
        self.db.refresh(record)
        return record
