"""
Oviora Hormone Intelligence
Normalization Service
"""

from __future__ import annotations

import re
from collections import defaultdict

from app.services.ontology import ontology_service


class Normalizer:
    """Normalize biomarker names, values and units."""

    def __init__(self) -> None:
        self.ontology = ontology_service

    @staticmethod
    def clean_text(text: str) -> str:
        text = text.replace("µ", "u")
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    @staticmethod
    def clean_numeric(value: str | float | int):
        if isinstance(value, (int, float)):
            return float(value)

        value = value.replace(",", ".")
        value = re.sub(r"[^0-9.\-]", "", value)

        try:
            return float(value)
        except Exception:
            return None

    def normalize_name(self, name: str) -> str:
        cleaned = self.clean_text(name)
        canonical = self.ontology.canonicalize(cleaned)
        return canonical or cleaned

    @staticmethod
    def normalize_unit(unit: str | None) -> str | None:
        if not unit:
            return None

        unit = unit.strip()
        mapping = {
            "uiu/ml": "uIU/mL",
            "miu/l": "mIU/L",
            "iu/l": "IU/L",
            "u/l": "U/L",
            "ug/dl": "µg/dL",
            "umol/l": "µmol/L",
        }

        key = unit.lower()
        return mapping.get(key, unit)

    def normalize_biomarker(self, biomarker: dict) -> dict:
        result = biomarker.copy()

        result["original_name"] = biomarker.get("name", "")
        result["canonical_name"] = self.normalize_name(
            biomarker.get("name", "")
        )

        result["value"] = self.clean_numeric(
            str(biomarker.get("value", ""))
        )

        result["unit"] = self.normalize_unit(
            biomarker.get("unit")
        )

        return result

    def merge_duplicates(self, biomarkers: list[dict]) -> list[dict]:
        grouped = defaultdict(list)

        for item in biomarkers:
            grouped[item["canonical_name"]].append(item)

        merged = []

        for _, values in grouped.items():
            values.sort(
                key=lambda x: x.get("parser_confidence", 0),
                reverse=True,
            )
            merged.append(values[0])

        return merged

    def normalize(self, biomarkers: list[dict]) -> list[dict]:
        normalized = [
            self.normalize_biomarker(item)
            for item in biomarkers
        ]

        return self.merge_duplicates(normalized)


normalizer = Normalizer()
