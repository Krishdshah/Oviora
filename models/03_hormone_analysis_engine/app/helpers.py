"""
Oviora Hormone Intelligence
Helper Utilities
"""

from __future__ import annotations

import hashlib
import json
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def generate_id() -> str:
    """Generate a random UUID4 hex string."""
    return uuid.uuid4().hex


def utc_now() -> str:
    """Return the current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def sha256_file(file_path: str | Path, chunk_size: int = 8192) -> str:
    """Compute the SHA-256 hash of a file."""
    digest = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def safe_filename(filename: str) -> str:
    """Return a filesystem-safe filename."""
    keep = "-_.() "
    cleaned = "".join(
        c if c.isalnum() or c in keep else "_" for c in filename
    )
    return cleaned.strip().replace(" ", "_")


def read_json(path: str | Path) -> dict[str, Any]:
    """Read a JSON file."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: str | Path, data: dict[str, Any]) -> None:
    """Write a JSON file."""
    Path(path).write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def average_confidence(values: list[float]) -> float:
    """Average confidence scores."""
    if not values:
        return 0.0
    return round(sum(values) / len(values), 3)


def temporary_directory() -> str:
    """Create and return a temporary directory."""
    return tempfile.mkdtemp(prefix="oviora_")


def ensure_directory(path: str | Path) -> Path:
    """Create a directory if it does not exist."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p
