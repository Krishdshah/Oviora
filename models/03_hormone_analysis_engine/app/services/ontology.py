"""
Oviora Hormone Intelligence
Ontology Service

Loads biomarker ontology from JSON files if available.
Falls back to an embedded default ontology so the application
remains functional during initial development.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from rapidfuzz import fuzz

from app.config import settings

DEFAULT_ONTOLOGY: dict[str, dict[str, Any]] = {
    "TSH": {
        "aliases": ["TSH", "Serum TSH", "Ultra Sensitive TSH", "TSH 3rd Generation"],
        "category": "thyroid",
        "units": ["uIU/mL", "mIU/L"],
    },
    "LH": {
        "aliases": ["LH", "Luteinizing Hormone"],
        "category": "hormone",
        "units": ["mIU/mL"],
    },
    "FSH": {
        "aliases": ["FSH", "Follicle Stimulating Hormone"],
        "category": "hormone",
        "units": ["mIU/mL"],
    },
    "AMH": {
        "aliases": ["AMH", "Anti Mullerian Hormone", "Anti-Müllerian Hormone"],
        "category": "hormone",
        "units": ["ng/mL"],
    },
    "Testosterone": {
        "aliases": ["Testosterone", "Total Testosterone"],
        "category": "androgen",
        "units": ["ng/dL"],
    },
}


class OntologyService:
    def __init__(self) -> None:
        self.ontology = self._load()

    def _load(self) -> dict[str, dict]:
        merged: dict[str, dict] = {}
        folder = Path(settings.ONTOLOGY_FOLDER)
        if folder.exists():
            for file in folder.glob("*.json"):
                try:
                    data = json.loads(file.read_text(encoding="utf-8"))
                    if isinstance(data, dict):
                        merged.update(data)
                except Exception:
                    pass
        if not merged:
            merged = DEFAULT_ONTOLOGY
        return merged

    def canonicalize(self, name: str, threshold: int = 88) -> str | None:
        text = name.strip().lower()
        best = None
        score = 0
        for canonical, meta in self.ontology.items():
            names = [canonical] + meta.get("aliases", [])
            for alias in names:
                s = fuzz.ratio(text, alias.lower())
                if s > score:
                    score = s
                    best = canonical
        return best if score >= threshold else None

    def metadata(self, canonical_name: str) -> dict[str, Any]:
        return self.ontology.get(canonical_name, {})

    def all_biomarkers(self) -> list[str]:
        return sorted(self.ontology.keys())


ontology_service = OntologyService()
