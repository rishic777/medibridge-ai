import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.responses import error, success
from app.db.session import get_db
from app.models.alert import Alert

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("")
def list_alerts(db: Session = Depends(get_db)):
    """All unacknowledged alerts across patients, for the doctor dashboard alert feed."""
    alerts = db.query(Alert).filter(Alert.acknowledged.is_(False)).order_by(Alert.created_at.desc()).all()
    return success(
        [
            {
                "id": str(a.id),
                "patient_id": str(a.patient_id),
                "rule_id": a.rule_id,
                "name": a.name,
                "priority": a.priority,
                "message": a.message,
            }
            for a in alerts
        ]
    )


@router.patch("/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: uuid.UUID, db: Session = Depends(get_db)):
    alert = db.get(Alert, alert_id)
    if alert is None:
        return error("INVALID_ALERT", "Alert could not be found.", status_code=404)
    alert.acknowledged = True
    db.commit()
    return success({"id": str(alert.id), "acknowledged": True})
