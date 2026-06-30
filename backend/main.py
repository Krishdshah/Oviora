from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Oviora Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"message": "Welcome to Oviora API"}
    
import sys
import os
import importlib.util
from typing import Dict, Any
import numpy as np

from api_contract import PCOSCyclePredictRequest, PCOSCyclePredictResponse

# Dynamically import clinical risk engine
clinical_module_name = "clinical_risk_engine_inference"
clinical_module_path = os.path.join(os.path.dirname(__file__), '..', 'models', '01_clinical_risk_engine', 'inference.py')
if os.path.exists(clinical_module_path):
    clinical_spec = importlib.util.spec_from_file_location(clinical_module_name, clinical_module_path)
    clinical_inference = importlib.util.module_from_spec(clinical_spec)
    sys.modules[clinical_module_name] = clinical_inference
    clinical_spec.loader.exec_module(clinical_inference)

@app.post("/api/v1/clinical-risk/predict")
def predict_clinical_risk(payload: Dict[str, Any]):
    if 'clinical_inference' in globals():
        return clinical_inference.predict(payload)
    return {"error": "Clinical risk engine not available"}

# Dynamically import pcos cycle ovulation engine
cycle_dir = os.path.join(os.path.dirname(__file__), '..', 'models', '09_pcos_cycle_ovulation_engine')
if cycle_dir not in sys.path:
    sys.path.insert(0, cycle_dir)

try:
    from v2_05_predict import predict as predict_pcos
    from api import _parse_dynamic
except ImportError as e:
    print(f"Warning: Could not import PCOS cycle engine: {e}")
    predict_pcos = None
    _parse_dynamic = None

@app.post("/api/v1/pcos-cycle/predict", response_model=PCOSCyclePredictResponse)
def predict_cycle(payload: PCOSCyclePredictRequest):
    if not predict_pcos or not _parse_dynamic:
        return {"error": "PCOS cycle engine not available"}
        
    history = []
    for length in payload.previous_cycle_lengths:
        history.append({
            "cycle_length": length,
            "sleep_hours": payload.sleep_hours,
            "stress_score": payload.stress_score
        })
    
    dyn = _parse_dynamic(history)
    sta = np.array([payload.age, payload.bmi, float(payload.pcos_diagnosed)])

    result = predict_pcos(
        dynamic_sequence=dyn,
        static_features_arr=sta,
        last_period_start=payload.last_period_start_date,
        sleep_hours=payload.sleep_hours,
        stress_score=payload.stress_score
    )
    return result
