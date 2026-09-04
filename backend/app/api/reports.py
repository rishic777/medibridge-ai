import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.responses import error, success
from app.db.session import get_db
from app.models.report import Report
from app.services.ai_service import AIService
from app.services.ocr_service import OCRService

router = APIRouter(prefix="/reports", tags=["reports"])
ocr_service = OCRService()
ai_service = AIService()


@router.post("/upload")
def upload_report(patient_id: uuid.UUID, file: UploadFile, db: Session = Depends(get_db)):
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    dest = settings.UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename}"
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    report = Report(patient_id=patient_id, filename=file.filename, file_path=str(dest), source="document_supported")
    db.add(report)
    db.commit()
    db.refresh(report)
    return success({"id": str(report.id), "filename": report.filename}, status_code=201)


@router.post("/{report_id}/process")
async def process_report(report_id: uuid.UUID, db: Session = Depends(get_db)):
    """Run OCR + AI extraction on an uploaded report."""
    report = db.get(Report, report_id)
    if report is None:
        return error("INVALID_REPORT", "Report could not be found.", status_code=404)

    ocr_text = ocr_service.extract_text(report.file_path)
    extracted = await ai_service.analyse_document(ocr_text)

    report.ocr_text = ocr_text
    report.extracted_data = extracted
    db.commit()
    db.refresh(report)
    return success({"id": str(report.id), "ocr_text": report.ocr_text, "extracted_data": report.extracted_data})


@router.get("/{report_id}")
def get_report(report_id: uuid.UUID, db: Session = Depends(get_db)):
    report = db.get(Report, report_id)
    if report is None:
        return error("INVALID_REPORT", "Report could not be found.", status_code=404)
    return success(
        {
            "id": str(report.id),
            "filename": report.filename,
            "ocr_text": report.ocr_text,
            "extracted_data": report.extracted_data,
            "source": report.source,
        }
    )
