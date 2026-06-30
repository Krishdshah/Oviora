"""
LLM Service Tests
"""
from app.services.llm import llm
from app.services.rule_engine import rule_engine

def test_service_exists():
    assert llm is not None

def test_rule_engine_fallback():
    report={"biomarkers":[],"missing_biomarkers":[]}
    result=rule_engine.analyze(report)
    assert result["llm_used"] is False
    assert "confidence_score" in result

def test_generate_without_keys():
    report={"biomarkers":[],"missing_biomarkers":[]}
    result=llm.generate(report)
    assert "provider" in result
