import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class VerificationRecord(Base):
    """
    Tracks the verification lifecycle of a single piece of information
    (a symptom, a report finding, a history item) as it moves from
    patient-reported -> document-supported -> physician-verified.
    """

    __tablename__ = "verification_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id"))

    information_type: Mapped[str] = mapped_column(String(100))  # e.g. "symptom", "report_finding"
    information_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))

    status: Mapped[str] = mapped_column(String(50), default="patient_reported")

    verified_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
