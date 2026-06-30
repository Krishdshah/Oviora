from app.cache import memo

def test_cache():
    assert memo("x")=="x"
