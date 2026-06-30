from app.services.formatter import formatter
def test_formatter():
    r=formatter.build({"provider":"rule_engine","parsed_report":{"biomarkers":[],"missing_biomarkers":[]},"analysis":{}})
    assert "executive_summary" in r
