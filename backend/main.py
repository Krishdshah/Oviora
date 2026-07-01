from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Oviora Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://oviora-seven.vercel.app",
        "https://oviora.vercel.app"
    ],
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
    HormoneAnalysisResponse,
    NutritionRankRequest,
    NutritionRankResponse,
    MealPlanRequest,
    MealPlanResponse
)

# Dynamically import clinical risk engine
clinical_module_name = "clinical_risk_engine_inference"
clinical_module_path = os.path.join(os.path.dirname(__file__), '..', 'models', '01_clinical_risk_engine', 'inference.py')
if os.path.exists(clinical_module_path):
    clinical_spec = importlib.util.spec_from_file_location(clinical_module_name, clinical_module_path)
    clinical_inference = importlib.util.module_from_spec(clinical_spec)
    sys.modules[clinical_module_name] = clinical_inference
    clinical_spec.loader.exec_module(clinical_inference)

# Dynamically import nutrition recommendation engine
nutrition_module_name = "nutrition_inference"
nutrition_module_path = os.path.join(os.path.dirname(__file__), '..', 'models', '05_nutrition_recommendation_engine', 'inference.py')
try:
    if os.path.exists(nutrition_module_path):
        nutrition_spec = importlib.util.spec_from_file_location(nutrition_module_name, nutrition_module_path)
        nutrition_inference = importlib.util.module_from_spec(nutrition_spec)
        sys.modules[nutrition_module_name] = nutrition_inference
        nutrition_spec.loader.exec_module(nutrition_inference)
except Exception as e:
    print(f"Warning: Could not import nutrition recommendation engine: {e}")
    if nutrition_module_name in sys.modules:
        del sys.modules[nutrition_module_name]

@app.post("/api/v1/clinical-risk/predict", response_model=ClinicalRiskPredictResponse)
def predict_clinical_risk(payload: ClinicalRiskPredictRequest):
    if 'clinical_inference' in globals():
        return clinical_inference.predict(payload.features)
    return {"error": "Clinical risk engine not available"}

# Dynamically import pcos cycle ovulation engine
cycle_dir = os.path.join(os.path.dirname(__file__), '..', 'models', '04_pcos_cycle_ovulation_engine')
if cycle_dir not in sys.path:
    sys.path.insert(0, cycle_dir)

import os
from pathlib import Path

current_cwd = os.getcwd()
try:
    os.chdir(cycle_dir)
    from v2_05_predict import predict as predict_pcos
    import v2_05_predict
    from api import _parse_dynamic
    
    # Fix runtime paths inside the module to point to correct locations
    v2_05_predict.PROCESSED_DIR = Path(cycle_dir) / "processed"
    v2_05_predict.MODEL_DIR = Path(cycle_dir) / "models"
    v2_05_predict.FIGURE_DIR = Path(cycle_dir) / "figures"
    v2_05_predict.OUTPUT_DIR = Path(cycle_dir) / "output"
    os.chdir(current_cwd)
except ImportError as e:
    os.chdir(current_cwd)
    print(f"Warning: Could not import PCOS cycle engine: {e}")
    predict_pcos = None
    _parse_dynamic = None
except Exception as e:
    os.chdir(current_cwd)
    print(f"Warning: Exception while importing PCOS cycle engine: {e}")
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
try:
    if os.path.exists(hormone_module_path):
        hormone_spec = importlib.util.spec_from_file_location(hormone_module_name, hormone_module_path)
        hormone_inference = importlib.util.module_from_spec(hormone_spec)
        sys.modules[hormone_module_name] = hormone_inference
        hormone_spec.loader.exec_module(hormone_inference)
except Exception as e:
    print(f"Warning: Could not import hormone analysis engine: {e}")
    # Remove from sys.modules if it was added before failure
    if hormone_module_name in sys.modules:
        del sys.modules[hormone_module_name]

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

# Personalized Nutrition Recommendation Engine (PNRE-v1.0) Endpoints
@app.post("/api/v1/recommend/rank", response_model=NutritionRankResponse)
def rank_foods(payload: NutritionRankRequest):
    if 'nutrition_inference' not in globals() or not hasattr(nutrition_inference, 'predict_rank'):
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="Nutrition recommendation engine not available")
    
    result = nutrition_inference.predict_rank(payload.model_dump())
    if "error" in result:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/api/v1/recommend/meal-plan", response_model=MealPlanResponse)
def generate_meal_plan(payload: MealPlanRequest):
    if 'nutrition_inference' not in globals() or not hasattr(nutrition_inference, 'predict_meal_plan'):
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="Nutrition recommendation engine not available")
    
    result = nutrition_inference.predict_meal_plan(
        patient_data=payload.patient_data.model_dump(),
        cuisine=payload.cuisine_preference,
        duration=payload.duration_days,
        budget=payload.budget,
        model_name=payload.groq_model
    )
    if "error" in result:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/api/v1/knowledge-graph/food/{food_name}")
def get_food_knowledge_graph(food_name: str):
    if 'nutrition_inference' not in globals() or not hasattr(nutrition_inference, 'get_food_graph'):
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="Nutrition recommendation engine not available")
    
    result = nutrition_inference.get_food_graph(food_name)
    if "error" in result:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=result["error"])
    return result
