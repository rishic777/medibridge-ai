from fastapi import APIRouter
from pydantic import BaseModel

from app.core.responses import success
from app.safety.red_flags import red_flag_engine
from app.safety.validators import format_red_flag_message

router = APIRouter(prefix="/safety", tags=["safety"])


class SafetyCheckRequest(BaseModel):
    symptom_tags: list[str]


@router.post("/check")
def check(payload: SafetyCheckRequest):
    hits = red_flag_engine.evaluate(set(payload.symptom_tags))
    return success(
        [
            {"rule_id": h["rule_id"], "priority": h.get("priority", "routine"), "message": format_red_flag_message(h)}
            for h in hits
        ]
    )
