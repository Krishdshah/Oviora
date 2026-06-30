"""
Oviora Hormone Intelligence
Analyze API

Runs the complete analysis pipeline.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.config import settings
from app.services.fallback import fallback_engine
from app.services.formatter import formatter
from app.services.report_generator import report_generator

router = APIRouter(prefix="/analyze", tags=["Analyze"])


@router.post("/{file_id}")
async def analyze_report(file_id: str):
    file_path = settings.UPLOAD_FOLDER / file_id

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Uploaded file not found.")

    result = fallback_engine.analyze_file(str(file_path))

    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "Analysis failed."))

    formatted = formatter.build(result)
    outputs = report_generator.save(formatted, Path(file_id).stem)

    return JSONResponse(
        content={
            "success": True,
            "provider": result.get("provider"),
            "report": formatted,
            "downloads": outputs,
            "pipeline": result.get("stages", {}),
        }
    )
