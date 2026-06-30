"""
Oviora Hormone Intelligence
Parser Service

Converts OCR output into structured biomarker records.
"""

from __future__ import annotations

import re
from datetime import datetime

from app.services.normalizer import normalizer
from app.services.validator import validator
from app.services.ontology import ontology_service


VALUE_RE = re.compile(r"(-?\d+(?:\.\d+)?)")
RANGE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)")


class ReportParser:
    def __init__(self) -> None:
        self.ontology = ontology_service

    def parse_line(self, line: dict) -> dict | None:
        """
        Expected OCR line:
        {
            "text": "...",
            "confidence": 0.96
        }
        """
        text = line.get("text", "").strip()
        if not text:
            return None

        canonical = self.ontology.canonicalize(text)
        if not canonical:
            for biomarker in self.ontology.all_biomarkers():
                if biomarker.lower() in text.lower():
                    canonical = biomarker
                    break

        if not canonical:
            return None

        value_match = VALUE_RE.search(text)
        range_match = RANGE_RE.search(text)

        unit = None
        meta = self.ontology.metadata(canonical)
        if meta.get("units"):
            unit = meta["units"][0]

        item = {
            "name": canonical,
            "canonical_name": canonical,
            "value": value_match.group(1) if value_match else None,
            "unit": unit,
            "reference_range": (
                f"{range_match.group(1)}-{range_match.group(2)}"
                if range_match
                else None
            ),
            "ocr_confidence": line.get("confidence", 0.0),
            "parser_confidence": min(
                1.0,
                line.get("confidence", 0.0) + (0.1 if value_match else 0),
            ),
        }

        return item

    def parse_metadata(self, ocr_lines: list[dict]) -> dict:
        meta = {
            "patient_name": None,
            "laboratory": None,
            "physician": None,
            "report_date": None,
        }

        date_re = re.compile(r"\b(\d{2}[/-]\d{2}[/-]\d{4})\b")

        for line in ocr_lines:
            txt = line.get("text", "")
            if meta["report_date"] is None:
                m = date_re.search(txt)
                if m:
                    try:
                        meta["report_date"] = datetime.strptime(
                            m.group(1).replace("/", "-"),
                            "%d-%m-%Y",
                        ).isoformat()
                    except Exception:
                        pass
        return meta

    def parse(self, ocr_lines: list[dict]) -> dict:
        biomarkers = []

        for line in ocr_lines:
            parsed = self.parse_line(line)
            if parsed:
                biomarkers.append(parsed)

        normalized = normalizer.normalize(biomarkers)
        validated = validator.validate(normalized)

        detected = {
            b["canonical_name"] for b in validated
        }

        missing = [
            b for b in self.ontology.all_biomarkers()
            if b not in detected
        ]

        confidence = (
            sum(i["parser_confidence"] for i in validated) / len(validated)
            if validated else 0.0
        )

        return {
            "metadata": self.parse_metadata(ocr_lines),
            "biomarkers": validated,
            "missing_biomarkers": missing,
            "overall_parser_confidence": round(confidence, 3),
        }


parser = ReportParser()
