import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.responses import error, success
from app.db.session import get_db
from app.models.conversation import Conversation, ConversationMessage
from app.models.symptom import Symptom
from app.safety.red_flags import red_flag_engine
from app.safety.validators import format_red_flag_message, sanitize_patient_facing_text
from app.models.alert import Alert
from app.services.ai_service import AIService
from app.schemas.history import ConversationMessageIn

router = APIRouter(prefix="/conversations", tags=["conversations"])
ai_service = AIService()


class ConversationCreate(BaseModel):
    patient_id: uuid.UUID


@router.post("")
def start_conversation(payload: ConversationCreate, db: Session = Depends(get_db)):
    conversation = Conversation(patient_id=payload.patient_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return success({"id": str(conversation.id), "patient_id": str(conversation.patient_id), "status": conversation.status}, status_code=201)


@router.get("/{conversation_id}")
def get_conversation(conversation_id: uuid.UUID, db: Session = Depends(get_db)):
    conversation = db.get(Conversation, conversation_id)
    if conversation is None:
        return error("INVALID_CONVERSATION", "Conversation could not be found.", status_code=404)
    messages = (
        db.query(ConversationMessage)
        .filter(ConversationMessage.conversation_id == conversation_id)
        .order_by(ConversationMessage.created_at.asc())
        .all()
    )
    return success(
        {
            "id": str(conversation.id),
            "status": conversation.status,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
        }
    )


@router.post("/{conversation_id}/message")
async def post_message(conversation_id: uuid.UUID, payload: ConversationMessageIn, db: Session = Depends(get_db)):
    """
    Core conversational turn:
    patient message -> AI extraction -> structured symptoms -> red-flag
    check -> next adaptive question.
    """
    conversation = db.get(Conversation, conversation_id)
    if conversation is None:
        return error("INVALID_CONVERSATION", "Conversation could not be found.", status_code=404)

    db.add(ConversationMessage(conversation_id=conversation_id, role="patient", content=payload.text))

    extraction = await ai_service.extract_medical_information(payload.text)
    extracted_symptoms = extraction.get("symptoms", [])

    saved_symptoms = []
    for item in extracted_symptoms:
        symptom = Symptom(
            patient_id=conversation.patient_id,
            name=item.get("name", "unknown"),
            duration=item.get("duration"),
            severity=item.get("severity"),
            source="patient_reported",
            confidence=0.6,
        )
        db.add(symptom)
        saved_symptoms.append(symptom)
    db.commit()

    # Safety check against everything reported so far for this patient.
    all_symptom_names = {
        s.name.lower().replace(" ", "_")
        for s in db.query(Symptom).filter(Symptom.patient_id == conversation.patient_id).all()
    }
    hits = red_flag_engine.evaluate(all_symptom_names)
    for rule in hits:
        exists = (
            db.query(Alert)
            .filter(Alert.patient_id == conversation.patient_id, Alert.rule_id == rule["rule_id"])
            .first()
        )
        if not exists:
            db.add(
                Alert(
                    patient_id=conversation.patient_id,
                    rule_id=rule["rule_id"],
                    name=rule["name"],
                    priority=rule.get("priority", "routine"),
                    message=format_red_flag_message(rule),
                )
            )
    db.commit()

    condition = saved_symptoms[0].name.lower().replace(" ", "_") if saved_symptoms else "general"
    answered_ids: list[str] = []
    next_question = await ai_service.generate_next_question(condition, answered_ids)

    ai_reply = "Thanks. I'll ask a few questions to understand this better."
    ai_reply = sanitize_patient_facing_text(ai_reply)
    db.add(ConversationMessage(conversation_id=conversation_id, role="ai", content=ai_reply))
    db.commit()

    return success(
        {
            "role": "ai",
            "content": ai_reply,
            "extracted_symptoms": [item for item in extracted_symptoms],
            "red_flags": [format_red_flag_message(r) for r in hits],
            "next_question": next_question,
        }
    )
