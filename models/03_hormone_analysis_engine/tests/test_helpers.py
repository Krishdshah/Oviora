from app.helpers import generate_id
def test_generate_id():
    assert len(generate_id())==32
