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

from api_contract import CyclePredictionRequest, CyclePredictionResponse

# Dynamically import inference since directory starts with a number
module_name = "clinical_risk_engine_inference"
module_path = os.path.join(os.path.dirname(__file__), '..', 'ai', '01_clinical_risk_engine', 'inference.py')
spec = importlib.util.spec_from_file_location(module_name, module_path)
inference = importlib.util.module_from_spec(spec)
sys.modules[module_name] = inference
spec.loader.exec_module(inference)

@app.post("/api/v1/clinical-risk/predict")
def predict_clinical_risk(payload: Dict[str, Any]):
    return inference.predict(payload)

# Dynamically import cycle intelligence engine
cycle_module_name = "cycle_intelligence_engine_inference"
cycle_module_path = os.path.join(os.path.dirname(__file__), '..', 'ai', '02_cycle_intelligence_engine', 'inference.py')
cycle_spec = importlib.util.spec_from_file_location(cycle_module_name, cycle_module_path)
cycle_inference = importlib.util.module_from_spec(cycle_spec)
sys.modules[cycle_module_name] = cycle_inference
cycle_spec.loader.exec_module(cycle_inference)

@app.post("/api/v1/cycle/predict", response_model=CyclePredictionResponse)
def predict_cycle(payload: CyclePredictionRequest):
    return cycle_inference.predict(payload.model_dump())
