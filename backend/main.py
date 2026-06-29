from fastapi import FastAPI

app = FastAPI(title="Oviora Backend API")
@app.get("/")
def read_root():
    return {"message": "Welcome to Oviora API"}
from typing import Dict, Any
from models.clinical_risk_engine.inference import predict

@app.post("/api/v1/clinical-risk/predict")
def predict_clinical_risk(payload: Dict[str, Any]):
    return predict(payload)
