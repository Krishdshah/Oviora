"""
Oviora Hormone Intelligence
Upload API

Handles secure report uploads.
"""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from app.config import settings

router = APIRouter(prefix="/upload", tags=["Upload"])


def _validate(file: UploadFile) -> None:
    suffix = Path(file.filename or "").suffix.lower()

    if suffix not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {suffix}",
        )


@router.post("")
async def upload_report(file: UploadFile = File(...)):
    """
    Upload a laboratory report.
    """
    _validate(file)

    data = await file.read()

    if len(data) > settings.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Uploaded file exceeds maximum allowed size.",
        )

    suffix = Path(file.filename).suffix.lower()
    filename = f"{uuid4().hex}{suffix}"
    destination = settings.UPLOAD_FOLDER / filename

    destination.write_bytes(data)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "success": True,
            "message": "File uploaded successfully.",
            "file_id": filename,
            "path": str(destination),
            "original_filename": file.filename,
            "size": len(data),
        },
    )
