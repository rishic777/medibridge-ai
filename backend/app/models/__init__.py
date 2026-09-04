"""
Import every model here so Base.metadata knows about all tables when
Alembic (or create_all, in the prototype) builds the schema.
"""
from app.models.alert import Alert  # noqa: F401
from app.models.conversation import Conversation, ConversationMessage  # noqa: F401
from app.models.patient import Patient  # noqa: F401
from app.models.report import Report  # noqa: F401
from app.models.symptom import Symptom  # noqa: F401
from app.models.verification import VerificationRecord  # noqa: F401
