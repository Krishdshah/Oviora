from app.storage import exists
def test_exists_false():
    assert exists("nonexistent.file") is False
