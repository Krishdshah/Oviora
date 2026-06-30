from app.security import sha256

def test_sha():
    assert len(sha256("abc"))==64
