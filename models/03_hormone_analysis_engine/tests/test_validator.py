"""
Oviora Hormone Intelligence
Validator Tests
"""

from app.services.validator import validator


def test_numeric_validation():
    biomarker = {
        "canonical_name": "TSH",
        "value": 2.5,
        "unit": "uIU/mL",
    }
    result = validator.validate([biomarker])[0]
    assert result["is_valid"] is True


def test_missing_value():
    biomarker = {
        "canonical_name": "TSH",
        "value": None,
        "unit": "uIU/mL",
    }
    result = validator.validate([biomarker])[0]
    assert result["is_valid"] is False
    assert "Missing value." in result["validation_errors"]


def test_implausible_value():
    biomarker = {
        "canonical_name": "TSH",
        "value": 1e9,
        "unit": "uIU/mL",
    }
    result = validator.validate([biomarker])[0]
    assert result["is_valid"] is False


def test_unit_validation():
    biomarker = {
        "canonical_name": "TSH",
        "value": 2.0,
        "unit": "mg/dL",
    }
    result = validator.validate([biomarker])[0]
    assert any("Unexpected unit" in e for e in result["validation_errors"])


def test_status_classification():
    biomarker = {
        "canonical_name": "TSH",
        "value": 10.0,
        "unit": "uIU/mL",
    }
    result = validator.validate([biomarker])[0]
    assert result["status"] in ("high", "unknown")
