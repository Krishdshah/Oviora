from app.auth import verify_api_key

def test_import():
    assert verify_api_key is not None
