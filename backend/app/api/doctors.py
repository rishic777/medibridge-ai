from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import success
from app.db.session import get_db
from app.models.alert import Alert
from app.models.patient import Patient

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    """Summary counts for the doctor dashboard landing view."""
    total_patients = db.query(Patient).count()
    open_alerts = db.query(Alert).filter(Alert.acknowledged.is_(False)).count()
    urgent_alerts = (
        db.query(Alert).filter(Alert.acknowledged.is_(False), Alert.priority == "urgent").count()
    )
    return success(
        {
            "total_patients": total_patients,
            "open_alerts": open_alerts,
            "urgent_alerts": urgent_alerts,
        }
    )
