"""
Application entrypoint. Keeps main.py thin: it only wires together
config, logging, CORS, DB table creation (dev only), and routers --
all real logic lives in api/, services/, safety/, and models/.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import ai, alerts, conversations, doctors, history, patients, reports, safety
from app.core.config import settings
from app.core.logging import configure_logging, logger
from app.db.session import Base, engine

configure_logging()

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    # Prototype convenience only -- use Alembic migrations in production
    # instead of create_all(). See database/schema.sql for the canonical DDL.
    import app.models  # noqa: F401  (ensures models are registered on Base)

    Base.metadata.create_all(bind=engine)
    logger.info("%s started (environment=%s, ai_provider=%s)", settings.APP_NAME, settings.ENVIRONMENT, settings.AI_PROVIDER)


@app.get("/health")
def health_check():
    return {"success": True, "data": {"status": "ok", "app": settings.APP_NAME}, "error": None}


api_prefix = settings.API_V1_PREFIX
app.include_router(patients.router, prefix=api_prefix)
app.include_router(conversations.router, prefix=api_prefix)
app.include_router(reports.router, prefix=api_prefix)
app.include_router(alerts.router, prefix=api_prefix)
app.include_router(doctors.router, prefix=api_prefix)
app.include_router(ai.router, prefix=api_prefix)
app.include_router(safety.router, prefix=api_prefix)
app.include_router(history.router, prefix=api_prefix)
