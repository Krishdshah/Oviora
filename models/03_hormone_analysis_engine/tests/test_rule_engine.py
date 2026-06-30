"""
Oviora Hormone Intelligence
Rule Engine Tests
"""

from app.services.rule_engine import rule_engine


def test_lh_fsh_ratio():
    data = {
        "LH": {"value": 10.0},
        "FSH": {"value": 5.0},
    }
    assert rule_engine.calculate_lh_fsh_ratio(data) == 2.0


def test_lh_fsh_ratio_missing():
    assert rule_engine.calculate_lh_fsh_ratio({}) is None


def test_hormonal_assessment():
    data = {
        "LH": {"value": 12.0},
        "FSH": {"value": 4.0},
        "Testosterone": {"status": "high"},
    }
    findings = rule_engine.hormonal_assessment(data)
    assert any("LH/FSH Ratio" in f for f in findings)
    assert any("Testosterone" in f for f in findings)


def test_thyroid_assessment():
    findings = rule_engine.thyroid_assessment(
        {"TSH": {"status": "normal"}}
    )
    assert findings == ["TSH: normal"]


def test_metabolic_assessment():
    findings = rule_engine.metabolic_assessment(
        {
            "HbA1c": {"status": "normal"},
            "Fasting Glucose": {"status": "high"},
        }
    )
    assert len(findings) == 2


def test_confidence_score():
    biomarkers = [
        {"ocr_confidence": 0.9, "parser_confidence": 0.8},
        {"ocr_confidence": 1.0, "parser_confidence": 0.9},
    ]
    score = rule_engine.confidence(biomarkers)
    assert 0 <= score <= 1


def test_analyze():
    report = {
        "biomarkers": [
            {
                "canonical_name": "LH",
                "value": 10,
                "status": "normal",
                "ocr_confidence": 0.9,
                "parser_confidence": 0.9,
            },
            {
                "canonical_name": "FSH",
                "value": 5,
                "status": "normal",
                "ocr_confidence": 0.9,
                "parser_confidence": 0.9,
            },
        ],
        "missing_biomarkers": [],
    }
    result = rule_engine.analyze(report)
    assert "derived_metrics" in result
    assert result["derived_metrics"]["LH_FSH_Ratio"] == 2.0
