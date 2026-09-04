import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import error, success
from app.db.session import get_db
from app.schemas.history import HistoryVerifyRequest
from app.services.ai_service import AIService
from app.services.history_service import HistoryService

router = APIRouter(prefix="/history", tags=["history"])
ai_service = AIService()


@router.get("/{patient_id}")
def get_history(patient_id: uuid.UUID, db: Session = Depends(get_db)):
    history = HistoryService(db).get_patient_history(patient_id)
    if not history:
        return error("INVALID_PATIENT", "Patient could not be found.", status_code=404)
    return success(
        {
            "patient_id": str(history["patient_id"]),
            "chief_complaint": history["chief_complaint"],
            "symptoms": [
                {
                    "id": str(s.id),
                    "name": s.name,
                    "duration": s.duration,
                    "severity": s.severity,
                    "source": s.source,
                    "confidence": s.confidence,
                }
                for s in history["symptoms"]
            ],
            "red_flags": history["red_flags"],
        }
    )


@router.post("/{patient_id}/verify")
def verify_history_item(patient_id: uuid.UUID, payload: HistoryVerifyRequest, db: Session = Depends(get_db)):
    """
    Doctor-facing endpoint that moves one piece of information along the
    three-layer verification path: patient_reported -> document_supported
    -> physician_verified.
    """
    record = HistoryService(db).record_verification(
        patient_id=patient_id,
        information_type=payload.information_type,
        information_id=payload.information_id,
        status=payload.status,
        verified_by=payload.verified_by,
    )
    return success({"id": str(record.id), "status": record.status})
