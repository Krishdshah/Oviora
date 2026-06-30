"""
Normalizer Tests
"""
from app.services.normalizer import normalizer

def test_clean_numeric():
    assert normalizer.clean_numeric("12.5") == 12.5
    assert normalizer.clean_numeric("12,5") == 12.5

def test_normalize_name():
    assert normalizer.normalize_name("Ultra Sensitive TSH") == "TSH"

def test_normalize_unit():
    assert normalizer.normalize_unit("uiu/ml") == "uIU/mL"

def test_merge_duplicates():
    data = [
        {"canonical_name":"TSH","parser_confidence":0.8},
        {"canonical_name":"TSH","parser_confidence":0.9},
    ]
    merged = normalizer.merge_duplicates(data)
    assert len(merged) == 1
    assert merged[0]["parser_confidence"] == 0.9

def test_pipeline():
    out = normalizer.normalize([
        {"name":"TSH","value":"2.4","unit":"uiu/ml","parser_confidence":1.0}
    ])
    assert out[0]["canonical_name"] == "TSH"
