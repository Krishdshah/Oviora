from app.services.pdf import PDFProcessor
def test_processor():
    assert PDFProcessor() is not None
