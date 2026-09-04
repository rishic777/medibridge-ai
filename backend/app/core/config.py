"""
Centralized application configuration.

Everything environment-specific (database URL, AI provider, secret keys)
is read from environment variables / .env here, and nowhere else in the
codebase. If you need a new setting, add it to this file only.
"""
from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    APP_NAME: str = "MediBridge AI"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Security
    SECRET_KEY: str = "CHANGE_ME"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # CORS
    CORS_ORIGINS: List[str] = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://192.168.1.8:5173",
]

    # Database
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/medibridge"

    # AI provider ("gemini" | "openai" | "local")
    AI_PROVIDER: str = "local"
    AI_API_KEY: str = ""
    AI_MODEL: str = "gemini-1.5-flash"

    # Speech-to-text provider
    ASR_PROVIDER: str = "local"
    ASR_API_KEY: str = ""

    # OCR
    OCR_PROVIDER: str = "paddleocr"

    # Config-driven content (questions / red flags / languages live here)
    QUESTIONS_DIR: Path = CONFIG_DIR / "questions"
    RED_FLAGS_DIR: Path = CONFIG_DIR / "red_flags"
    LANGUAGES_DIR: Path = CONFIG_DIR / "languages"

    # File uploads
    UPLOAD_DIR: Path = BASE_DIR / "backend" / "uploads"
    MAX_UPLOAD_MB: int = 15


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
