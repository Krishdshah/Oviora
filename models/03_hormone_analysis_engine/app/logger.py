"""
Oviora Hormone Intelligence
Structured Logging Module
"""

import logging
import logging.handlers
import uuid
from contextvars import ContextVar
from pathlib import Path

from app.config import settings

_request_id: ContextVar[str] = ContextVar("request_id", default="-")


class RequestIDFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = _request_id.get()
        return True


def set_request_id(request_id: str | None = None) -> str:
    """Assign a request ID for the current request context."""
    rid = request_id or str(uuid.uuid4())
    _request_id.set(rid)
    return rid


def get_request_id() -> str:
    return _request_id.get()


def configure_logger() -> logging.Logger:
    """
    Configure application logger with console + rotating file handlers.
    """
    log_dir = Path(settings.REPORT_FOLDER).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("oviora")
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(request_id)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    req_filter = RequestIDFilter()

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.addFilter(req_filter)

    file_handler = logging.handlers.RotatingFileHandler(
        filename=settings.LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.addFilter(req_filter)

    logger.addHandler(console)
    logger.addHandler(file_handler)
    logger.propagate = False
    return logger


logger = configure_logger()
