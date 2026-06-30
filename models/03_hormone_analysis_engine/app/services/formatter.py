"""
Oviora Hormone Intelligence
Formatter Service

Transforms parsed data and analysis into a consistent
presentation-ready structure.
"""

from __future__ import annotations

from datetime import datetime


class ReportFormatter:
    MEDICAL_DISCLAIMER = (
        "This report is an AI-assisted clinical decision-support "
        "prototype and is not a medical diagnosis. Please consult "
        "a qualified healthcare professional."
    )

    def executive_summary(self, analysis: dict) -> str:
        provider = analysis.get("provider", "rule_engine")
        analysis_data = analysis.get("analysis", {})
        confidence = None
        if isinstance(analysis_data, dict):
            confidence = analysis_data.get("confidence_score")
            
        if confidence is None:
            return f"Analysis generated using {provider}."
        return (
            f"Analysis generated using {provider}. "
            f"Overall confidence score: {confidence:.3f}."
        )

    def biomarker_table(self, parsed_report: dict) -> list[dict]:
        rows = []
        for b in parsed_report.get("biomarkers", []):
            rows.append({
                "Biomarker": b.get("canonical_name"),
                "Value": b.get("value"),
                "Unit": b.get("unit"),
                "Status": b.get("status"),
                "Reference Range": b.get("reference_range"),
            })
        return rows

    def build(self, analysis_result: dict) -> dict:
        parsed = analysis_result.get("parsed_report", {})
        analysis = analysis_result.get("analysis", {})
        if not isinstance(analysis, dict):
            analysis = {}

        return {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "provider": analysis_result.get("provider", "rule_engine"),
            "executive_summary": self.executive_summary(analysis_result),
            "biomarkers": self.biomarker_table(parsed),
            "missing_biomarkers": parsed.get("missing_biomarkers", []),
            "assessments": {
                "hormonal": analysis.get("hormonal_assessment", []),
                "thyroid": analysis.get("thyroid_assessment", []),
                "metabolic": analysis.get("metabolic_assessment", []),
                "vitamins": analysis.get("vitamin_assessment", []),
                "liver": analysis.get("liver_assessment", []),
                "inflammation": analysis.get("inflammation_assessment", []),
            },
            "derived_metrics": analysis.get("derived_metrics", {}),
            "confidence_score": analysis.get("confidence_score"),
            "disclaimer": self.MEDICAL_DISCLAIMER,
        }


formatter = ReportFormatter()
