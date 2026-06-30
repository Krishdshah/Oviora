"""
Oviora Hormone Intelligence
Reports API

List, download and delete generated reports.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from app.config import settings

router = APIRouter(prefix="/reports", tags=["Reports"])

_ALLOWED = {
    "json": ".json",
    "markdown": ".md",
    "html": ".html",
    "pdf": ".pdf",
}


@router.get("")
async def list_reports():
    reports = []
    for ext in _ALLOWED.values():
        for f in settings.REPORT_FOLDER.glob(f"*{ext}"):
            reports.append(
                {
                    "id": f.stem,
                    "name": f.name,
                    "format": ext.lstrip("."),
                    "size": f.stat().st_size,
                }
            )
    reports.sort(key=lambda x: (x["id"], x["format"]))
    return JSONResponse({"success": True, "reports": reports})


@router.get("/{report_id}/{fmt}")
async def download_report(report_id: str, fmt: str):
    fmt = fmt.lower()
    if fmt not in _ALLOWED:
        raise HTTPException(status_code=400, detail="Unsupported report format.")

    path = settings.REPORT_FOLDER / f"{report_id}{_ALLOWED[fmt]}"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Report not found.")

    return FileResponse(
        path=str(path),
        filename=path.name,
        media_type="application/octet-stream",
    )


@router.delete("/{report_id}")
async def delete_report(report_id: str):
    deleted = []

    for ext in _ALLOWED.values():
        path = settings.REPORT_FOLDER / f"{report_id}{ext}"
        if path.exists():
            path.unlink()
            deleted.append(path.name)

    if not deleted:
        raise HTTPException(status_code=404, detail="Report not found.")

    return JSONResponse(
        {
            "success": True,
            "deleted": deleted,
        }
    )
