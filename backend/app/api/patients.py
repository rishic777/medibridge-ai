import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import error, success
from app.db.session import get_db
from app.models.alert import Alert
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientOut

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("")
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    patient = Patient(**payload.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return success(PatientOut.model_validate(patient), status_code=201)


@router.get("/{patient_id}")
def get_patient(patient_id: uuid.UUID, db: Session = Depends(get_db)):
    patient = db.get(Patient, patient_id)
    if patient is None:
        return error("INVALID_PATIENT", "Patient could not be found.", status_code=404)
    return success(PatientOut.model_validate(patient))


@router.get("")
def list_patients(db: Session = Depends(get_db)):
    patients = db.query(Patient).order_by(Patient.created_at.desc()).all()
    return success([PatientOut.model_validate(p) for p in patients])


@router.get("/{patient_id}/alerts")
def get_patient_alerts(patient_id: uuid.UUID, db: Session = Depends(get_db)):
    alerts = db.query(Alert).filter(Alert.patient_id == patient_id).all()
    return success(
        [
            {
                "id": str(a.id),
                "rule_id": a.rule_id,
                "name": a.name,
                "priority": a.priority,
                "message": a.message,
                "acknowledged": a.acknowledged,
            }
            for a in alerts
        ]
    )
