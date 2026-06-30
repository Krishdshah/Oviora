from app.services.report_generator import report_generator
def test_json():
    assert report_generator.to_json({}).startswith("{")
