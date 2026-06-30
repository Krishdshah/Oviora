from fastapi import FastAPI, File, UploadFile
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

from api_contract import (
    PCOSCyclePredictRequest, 
    PCOSCyclePredictResponse,
    CyclePredictRequest,
    CyclePredictResponse,
    ClinicalRiskPredictRequest,
    ClinicalRiskPredictResponse,
    HormoneAnalysisResponse
)

# Dynamically import clinical risk engine
clinical_module_name = "clinical_risk_engine_inference"
clinical_module_path = os.path.join(os.path.dirname(__file__), '..', 'models', '01_clinical_risk_engine', 'inference.py')
if os.path.exists(clinical_module_path):
    clinical_spec = importlib.util.spec_from_file_location(clinical_module_name, clinical_module_path)
    clinical_inference = importlib.util.module_from_spec(clinical_spec)
    sys.modules[clinical_module_name] = clinical_inference
    clinical_spec.loader.exec_module(clinical_inference)

@app.post("/api/v1/clinical-risk/predict", response_model=ClinicalRiskPredictResponse)
def predict_clinical_risk(payload: ClinicalRiskPredictRequest):
    if 'clinical_inference' in globals():
        return clinical_inference.predict(payload.features)
    return {"error": "Clinical risk engine not available"}

# Dynamically import pcos cycle ovulation engine
cycle_dir = os.path.join(os.path.dirname(__file__), '..', 'models', '04_pcos_cycle_ovulation_engine')
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

# Dynamically import standard cycle intelligence engine
std_cycle_dir = os.path.join(os.path.dirname(__file__), '..', 'models', '02_cycle_intelligence_engine')
if std_cycle_dir not in sys.path:
    sys.path.insert(0, std_cycle_dir)

try:
    from std_inference import predict as predict_std_cycle
except ImportError as e:
    print(f"Warning: Could not import Standard Cycle engine: {e}")
    predict_std_cycle = None

@app.post("/api/v1/cycle/predict", response_model=CyclePredictResponse)
def predict_standard_cycle(payload: CyclePredictRequest):
    if predict_std_cycle:
        return predict_std_cycle(payload.model_dump())
    return {"error": "Standard cycle engine not available"}

# Dynamically import hormone analysis engine
hormone_module_name = "hormone_inference"
hormone_module_path = os.path.join(os.path.dirname(__file__), '..', 'models', '03_hormone_analysis_engine', 'inference.py')
if os.path.exists(hormone_module_path):
    hormone_spec = importlib.util.spec_from_file_location(hormone_module_name, hormone_module_path)
    hormone_inference = importlib.util.module_from_spec(hormone_spec)
    sys.modules[hormone_module_name] = hormone_inference
    hormone_spec.loader.exec_module(hormone_inference)

@app.post("/api/v1/labs/upload", response_model=HormoneAnalysisResponse)
def upload_lab_report(file: UploadFile = File(...)):
    if 'hormone_inference' not in globals():
        return {"success": False, "error": "Hormone analysis engine not available"}
    
    try:
        # Create uploads directory if not exists
        uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        
        file_path = os.path.join(uploads_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())
            
        result = hormone_inference.predict(file_path)
        
        # Optionally clean up the file
        if os.path.exists(file_path):
            os.remove(file_path)
            
        if "error" in result:
            return {"success": False, "error": result["error"]}
            
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
