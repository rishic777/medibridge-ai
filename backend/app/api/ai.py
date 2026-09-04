from fastapi import APIRouter
from pydantic import BaseModel

from app.core.responses import success
from app.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["ai"])
ai_service = AIService()


class ExtractRequest(BaseModel):
    text: str


class QuestionRequest(BaseModel):
    condition: str
    answered_ids: list[str] = []


class SummaryRequest(BaseModel):
    patient_data: dict


@router.post("/extract")
async def extract(payload: ExtractRequest):
    data = await ai_service.extract_medical_information(payload.text)
    return success(data)


@router.post("/question")
async def next_question(payload: QuestionRequest):
    question = await ai_service.generate_next_question(payload.condition, payload.answered_ids)
    return success(question)


@router.post("/summary")
async def summary(payload: SummaryRequest):
    text = await ai_service.summarize_history(payload.patient_data)
    return success({"summary": text})
