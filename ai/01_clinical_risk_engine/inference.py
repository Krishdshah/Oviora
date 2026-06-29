import json
import os
import joblib
import pandas as pd
from catboost import CatBoostClassifier

# Resolve model paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_CBM = os.path.join(BASE_DIR, "clinical_risk_engine.cbm")
MODEL_PKL = os.path.join(BASE_DIR, "clinical_risk_engine.pkl")
SCHEMA_FILE = os.path.join(BASE_DIR, "feature_schema.json")

# Initialize global model variable
model = None

def load_model():
    """Loads the model into memory. Prefers CBM over PKL."""
    global model
    if model is not None:
        return model
        
    try:
        if os.path.exists(MODEL_CBM):
            model = CatBoostClassifier()
            model.load_model(MODEL_CBM)
        elif os.path.exists(MODEL_PKL):
            model = joblib.load(MODEL_PKL)
        else:
            raise Exception("No model file found.")
    except Exception as e:
        print(f"Error loading model: {e}")
    return model

def predict(input_data: dict) -> dict:
    """
    Runs inference for the Clinical Risk Engine.
    """
    model_instance = load_model()
    if not model_instance:
        return {"error": "Model not loaded properly"}

    with open(SCHEMA_FILE, 'r') as f:
        schema = json.load(f)
        
    features = schema.get("features", [])
    
    # Construct input array in the correct order
    input_list = []
    for f in features:
        input_list.append(input_data.get(f, 0)) # default to 0 if missing
        
    # Convert to dataframe to match feature names if needed
    df = pd.DataFrame([input_list], columns=features)
    
    # Predict probabilities (PCOS Risk Score)
    if hasattr(model_instance, 'predict_proba'):
        prob = float(model_instance.predict_proba(df)[0][1])
    else:
        prob = float(model_instance.predict(df)[0])
        
    risk_level = "High" if prob > 0.5 else "Low"
    
    return {
        "risk_score": round(prob, 4),
        "risk_level": risk_level,
        "factors": ["Check input params to determine specific factors"] # Placeholder for SHAP values
    }

