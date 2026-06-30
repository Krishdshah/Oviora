"""
Oviora Hormone Intelligence
Parser Tests
"""

from app.services.parser import parser


def test_parse_single_tsh():
    ocr = [
        {
            "text": "TSH 2.35 0.40-4.00",
            "confidence": 0.98,
        }
    ]

    result = parser.parse(ocr)

    assert "biomarkers" in result
    assert len(result["biomarkers"]) == 1

    biomarker = result["biomarkers"][0]

    assert biomarker["canonical_name"] == "TSH"
    assert abs(float(biomarker["value"]) - 2.35) < 1e-6
    assert biomarker["ocr_confidence"] == 0.98


def test_alias_matching():
    ocr = [
        {
            "text": "Ultra Sensitive TSH 1.72",
            "confidence": 0.95,
        }
    ]

    result = parser.parse(ocr)

    assert result["biomarkers"][0]["canonical_name"] == "TSH"


def test_missing_biomarkers():
    result = parser.parse([])

    assert "missing_biomarkers" in result
    assert isinstance(result["missing_biomarkers"], list)


def test_parser_confidence_range():
    ocr = [
        {
            "text": "LH 8.2",
            "confidence": 0.91,
        }
    ]

    result = parser.parse(ocr)

    confidence = result["overall_parser_confidence"]

    assert 0.0 <= confidence <= 1.0


def test_reference_range_extraction():
    ocr = [
        {
            "text": "FSH 5.1 3.5-12.5",
            "confidence": 0.99,
        }
    ]

    result = parser.parse(ocr)

    biomarker = result["biomarkers"][0]

    assert biomarker["reference_range"] == "3.5-12.5"
