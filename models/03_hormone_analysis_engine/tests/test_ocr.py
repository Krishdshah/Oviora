"""
OCR Tests
"""
import numpy as np
from app.services.ocr import OCRService

def test_preprocess():
    img = np.full((100,100,3),255,dtype=np.uint8)
    out = OCRService.preprocess(img)
    assert out.shape[:2] == (100,100)

def test_service_created():
    svc = OCRService()
    assert svc is not None

def test_pil_conversion():
    from PIL import Image
    img = Image.new("RGB",(10,10),"white")
    arr = OCRService._pil_to_cv(img)
    assert arr.shape[0] == 10
