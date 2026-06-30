"""
Oviora Hormone Intelligence
Rule Engine

Deterministic clinical rule engine used before and
independently of the LLM.
"""

from __future__ import annotations

from typing import Any


class RuleEngine:
    def _index(self, biomarkers: list[dict]) -> dict[str, dict]:
        return {b["canonical_name"]: b for b in biomarkers}

    def calculate_lh_fsh_ratio(self, data: dict[str, dict]) -> float | None:
        lh = data.get("LH")
        fsh = data.get("FSH")
        if not lh or not fsh:
            return None
        try:
            if float(fsh["value"]) == 0:
                return None
            return round(float(lh["value"]) / float(fsh["value"]), 2)
        except Exception:
            return None

    def hormonal_assessment(self, data: dict[str, dict]) -> list[str]:
        findings = []
        ratio = self.calculate_lh_fsh_ratio(data)
        if ratio is not None:
            findings.append(f"LH/FSH Ratio: {ratio}")
            if ratio > 2:
                findings.append(
                    "Elevated LH/FSH ratio may be associated with PCOS in the appropriate clinical context."
                )
        for marker in ("Testosterone", "Free Testosterone", "DHEAS", "AMH", "Prolactin"):
            item = data.get(marker)
            if item and item.get("status") == "high":
                findings.append(f"{marker} is above the reference range.")
        return findings

    def thyroid_assessment(self, data: dict[str, dict]) -> list[str]:
        findings = []
        tsh = data.get("TSH")
        if tsh:
            findings.append(f"TSH: {tsh.get('status','unknown')}")
        return findings

    def metabolic_assessment(self, data: dict[str, dict]) -> list[str]:
        findings = []
        for marker in ("HbA1c", "Fasting Glucose", "Fasting Insulin"):
            item = data.get(marker)
            if item:
                findings.append(f"{marker}: {item.get('status','unknown')}")
        return findings

    def vitamin_assessment(self, data: dict[str, dict]) -> list[str]:
        findings = []
        for marker in ("Vitamin D", "Vitamin B12", "Ferritin"):
            item = data.get(marker)
            if item:
                findings.append(f"{marker}: {item.get('status','unknown')}")
        return findings

    def liver_assessment(self, data: dict[str, dict]) -> list[str]:
        return [
            f"{m}: {data[m]['status']}"
            for m in ("ALT", "AST")
            if m in data
        ]

    def inflammation_assessment(self, data: dict[str, dict]) -> list[str]:
        return [
            f"{m}: {data[m]['status']}"
            for m in ("CRP", "hs-CRP", "ESR")
            if m in data
        ]

    def confidence(self, biomarkers: list[dict]) -> float:
        if not biomarkers:
            return 0.0
        total = sum(
            (b.get("ocr_confidence", 0) + b.get("parser_confidence", 0)) / 2
            for b in biomarkers
        )
        return round(total / len(biomarkers), 3)

    def analyze(self, parsed_report: dict[str, Any]) -> dict[str, Any]:
        biomarkers = parsed_report.get("biomarkers", [])
        data = self._index(biomarkers)

        return {
            "derived_metrics": {
                "LH_FSH_Ratio": self.calculate_lh_fsh_ratio(data)
            },
            "hormonal_assessment": self.hormonal_assessment(data),
            "thyroid_assessment": self.thyroid_assessment(data),
            "metabolic_assessment": self.metabolic_assessment(data),
            "vitamin_assessment": self.vitamin_assessment(data),
            "liver_assessment": self.liver_assessment(data),
            "inflammation_assessment": self.inflammation_assessment(data),
            "missing_biomarkers": parsed_report.get("missing_biomarkers", []),
            "confidence_score": self.confidence(biomarkers),
            "llm_used": False,
        }


rule_engine = RuleEngine()
