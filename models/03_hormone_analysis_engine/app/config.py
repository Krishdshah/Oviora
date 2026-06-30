"""
Oviora Hormone Intelligence
Configuration Module

Centralized configuration management using Pydantic Settings.
"""

from pathlib import Path
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    APP_NAME: str = "Oviora Hormone Intelligence"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    GEMINI_API_KEY: str = Field(default="")
    GROQ_API_KEY: str = Field(default="")

    GEMINI_MODEL: str = "gemini-2.5-flash"
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    MAX_OUTPUT_TOKENS: int = 4096
    TEMPERATURE: float = 0.2
    LLM_TIMEOUT: int = 60
    MAX_RETRIES: int = 3

    OCR_LANGUAGE: str = "en"
    OCR_USE_GPU: bool = False
    OCR_MIN_CONFIDENCE: float = 0.60

    MAX_UPLOAD_SIZE_MB: int = 20
    ALLOWED_EXTENSIONS: tuple[str, ...] = (
        ".pdf", ".png", ".jpg", ".jpeg", ".bmp", ".tiff"
    )

    UPLOAD_FOLDER: Path = BASE_DIR / "uploads"
    REPORT_FOLDER: Path = BASE_DIR / "reports"
    TEMP_FOLDER: Path = BASE_DIR / "temp"
    ONTOLOGY_FOLDER: Path = BASE_DIR / "app" / "data" / "ontology"
    REFERENCE_FOLDER: Path = BASE_DIR / "app" / "data" / "reference_ranges"

    SECRET_KEY: str = "CHANGE_ME"

    ENABLE_RATE_LIMIT: bool = True

    DEFAULT_REPORT_FORMAT: str = "json"
    SAVE_REPORTS: bool = True

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "oviora.log"

    @property
    def max_upload_size_bytes(self) -> int:
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    def create_directories(self) -> None:
        self.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
        self.REPORT_FOLDER.mkdir(parents=True, exist_ok=True)
        self.TEMP_FOLDER.mkdir(parents=True, exist_ok=True)
        self.ONTOLOGY_FOLDER.mkdir(parents=True, exist_ok=True)
        self.REFERENCE_FOLDER.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.create_directories()
    return settings


settings = get_settings()
