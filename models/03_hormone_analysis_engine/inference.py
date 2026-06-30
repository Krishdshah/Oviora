import os
import sys

# Resolve paths locally within this model directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.services.fallback import fallback_engine
from app.services.formatter import formatter

def predict(file_path: str) -> dict:
    """
    Runs the complete hormone analysis pipeline (OCR -> Normalization -> Rules -> LLM) 
    on a lab report file.
    """
    result = fallback_engine.analyze_file(file_path)
    if not result.get("success"):
        return {"error": result.get("error", "Analysis failed")}
    return formatter.build(result)
