"""
Oviora Hormone Intelligence
Validation Service

Validates normalized biomarkers against ontology and
reference ranges before rule engine / LLM processing.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.config import settings


class Validator:
    def __init__(self) -> None:
        ref_file = Path(settings.REFERENCE_FOLDER) / "reference_ranges.json"
        self.reference_ranges = {}
        if ref_file.exists():
            try:
                self.reference_ranges = json.loads(
                    ref_file.read_text(encoding="utf-8")
                )
            except Exception:
                self.reference_ranges = {}

    @staticmethod
    def is_numeric(value) -> bool:
        return isinstance(value, (int, float))

    @staticmethod
    def plausible(value: float) -> bool:
        return -1e-6 <= value <= 1_000_000

    def validate_unit(self, biomarker: dict) -> list[str]:
        errors = []
        ref = self.reference_ranges.get(biomarker["canonical_name"])
        if ref:
            expected = ref.get("unit")
            if expected and biomarker.get("unit") != expected:
                errors.append(
                    f"Unexpected unit '{biomarker.get('unit')}', expected '{expected}'."
                )
        return errors

    def validate_value(self, biomarker: dict) -> list[str]:
        errors = []
        value = biomarker.get("value")

        if value is None:
            errors.append("Missing value.")
            return errors

        if not self.is_numeric(value):
            errors.append("Value is not numeric.")
            return errors

        if not self.plausible(float(value)):
            errors.append("Implausible numeric value.")

        return errors

    def classify(self, biomarker: dict) -> str:
        ref = self.reference_ranges.get(biomarker["canonical_name"])
        if not ref:
            return "unknown"

        value = biomarker.get("value")
        if value is None:
            return "unknown"

        # Select first available interval
        ranges = ref.get("reference", {})
        node = None
        for group in ranges.values():
            if isinstance(group, dict):
                first = next(iter(group.values()))
                if isinstance(first, dict) and "low" in first:
                    node = first
                    break

        if not node:
            return "unknown"

        if value < node["low"]:
            return "low"
        if value > node["high"]:
            return "high"
        return "normal"

    def validate(self, biomarkers: list[dict]) -> list[dict]:
        results = []

        for biomarker in biomarkers:
            item = biomarker.copy()
            errors = []
            errors.extend(self.validate_value(item))
            errors.extend(self.validate_unit(item))
            item["validation_errors"] = errors
            item["is_valid"] = len(errors) == 0
            item["status"] = self.classify(item)
            results.append(item)

        return results


validator = Validator()
