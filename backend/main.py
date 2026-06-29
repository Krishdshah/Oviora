from fastapi import FastAPI

app = FastAPI(title="Oviora Backend API")
@app.get("/")
def read_root():
    return {"message": "Welcome to Oviora API"}
    
import sys
import os
import importlib.util
from typing import Dict, Any

# Dynamically import inference since directory starts with a number
module_name = "clinical_risk_engine_inference"
module_path = os.path.join(os.path.dirname(__file__), '..', 'models', '01_clinical_risk_engine', 'inference.py')
spec = importlib.util.spec_from_file_location(module_name, module_path)
inference = importlib.util.module_from_spec(spec)
sys.modules[module_name] = inference
spec.loader.exec_module(inference)

@app.post("/api/v1/clinical-risk/predict")
def predict_clinical_risk(payload: Dict[str, Any]):
    return inference.predict(payload)
