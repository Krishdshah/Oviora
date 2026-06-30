"""
Oviora Hormone Intelligence
Health API

Health and readiness endpoints.
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.config import settings

router = APIRouter(prefix="/health", tags=["Health"])


def _dir_ok(path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        test = path / ".healthcheck"
        test.write_text("ok", encoding="utf-8")
        test.unlink(missing_ok=True)
        return True
    except Exception:
        return False


@router.get("")
async def health():
    return JSONResponse(
        {
            "status": "healthy",
            "service": settings.APP_NAME,
            "version": settings.VERSION,
        }
    )


@router.get("/live")
async def live():
    return JSONResponse({"live": True})


@router.get("/ready")
async def ready():
    checks = {
        "uploads": _dir_ok(settings.UPLOAD_FOLDER),
        "reports": _dir_ok(settings.REPORT_FOLDER),
        "ontology": settings.ONTOLOGY_FOLDER.exists(),
        "reference_ranges": settings.REFERENCE_FOLDER.exists(),
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "groq_configured": bool(settings.GROQ_API_KEY),
    }

    ready = checks["uploads"] and checks["reports"]

    return JSONResponse(
        {
            "ready": ready,
            "checks": checks,
        },
        status_code=200 if ready else 503,
    )
