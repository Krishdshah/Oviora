import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nutrition_app.main import nutrition_app
from nutrition_app.data_pipeline.preprocessor import preprocess_patient_data
from nutrition_app.data_pipeline.schemas import PatientAdvancedInput

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model" in data
    assert "knowledge_graph" in data

def test_patient_derivation_fallback():
    # Test basic symptom-based derivation when advanced metrics are absent
    basic_input = PatientAdvancedInput(
        age=25.0,
        weight_kg=80.0,  # BMI ~32 (Obese)
        height_cm=158.0,
        waist_inch=36.0,
        hip_inch=40.0,
        cycle_regularity="irregular",
        dietary_preference="veg",
        allergies=[],
        symptoms=["acne", "weight_gain", "fatigue"],
        goals=["weight_loss"],
        exercise_hours_per_week=1.0
    )
    profile = preprocess_patient_data(basic_input)
    assert profile.bmi > 30.0
    assert profile.obesity_status == "Obese"
    assert profile.insulin_resistance_risk == "High"
    assert profile.hormonal_imbalance_severity == "High"
    assert profile.inflammation_risk == "High"
    assert profile.exercise_habits == "Sedentary"

def test_patient_derivation_clinical():
    # Test clinical-level exact calculation when lab values are present
    clinical_input = PatientAdvancedInput(
        age=30.0,
        weight_kg=55.0,
        height_cm=160.0,
        waist_inch=28.0,
        hip_inch=34.0,
        cycle_regularity="regular",
        dietary_preference="non-veg",
        allergies=[],
        symptoms=[],
        goals=["energy"],
        exercise_hours_per_week=4.0,
        fasting_glucose=85.0,
        fasting_insulin=5.0,  # HOMA-IR = (85 * 5)/405 = 1.04 (Low IR)
        lh=4.5,
        fsh=5.0,              # LH/FSH ratio = 0.9 (Normal/Low hormone severity)
        amh=2.1,
        vit_d=32.0,
        diabetes_status=False,
        hypertension_status=False
    )
    profile = preprocess_patient_data(clinical_input)
    assert profile.obesity_status == "Normal"
    assert profile.homa_ir == 1.05  # Rounded
    assert profile.lh_fsh_ratio == 0.9
    assert profile.insulin_resistance_risk == "Low"
    assert profile.hormonal_imbalance_severity == "Low"

def test_rank_endpoint():
    # Call rank endpoint with basic data
    payload = {
        "age": 28.0,
        "weight_kg": 65.0,
        "height_cm": 160.0,
        "waist_inch": 32.0,
        "hip_inch": 36.0,
        "cycle_regularity": "irregular",
        "dietary_preference": "veg",
        "allergies": [],
        "symptoms": ["acne"],
        "goals": ["regular_cycles"],
        "exercise_hours_per_week": 3.0
    }
    response = client.post("/api/v1/recommend/rank", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "patient_profile" in data
    assert "recommendations" in data
    assert len(data["recommendations"]) > 0
    # Top food should have SHAP explanations
    first_food = data["recommendations"][0]
    assert "explanation" in first_food
    assert "ranking_score" in first_food

def test_meal_plan_endpoint():
    payload = {
        "patient_data": {
            "age": 26.0,
            "weight_kg": 72.0,
            "height_cm": 165.0,
            "waist_inch": 34.0,
            "hip_inch": 38.0,
            "cycle_regularity": "irregular",
            "dietary_preference": "vegan",
            "allergies": ["nuts"],
            "symptoms": ["fatigue"],
            "goals": ["weight_loss"],
            "exercise_hours_per_week": 2.0
        },
        "cuisine_preference": "western",
        "duration_days": 1,
        "budget": "medium"
    }
    response = client.post("/api/v1/recommend/meal-plan", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "meal_plan" in data
    assert "grocery_list" in data
    assert "clinical_reasoning" in data
    assert len(data["meal_plan"]) == 1

def test_knowledge_graph_endpoint():
    # Query for a known food (Spinach is generated/contained in our dataset)
    response = client.get("/api/v1/knowledge-graph/food/Spinach")
    assert response.status_code == 200
    data = response.json()
    assert data["food_name"] == "Spinach"
    assert "attributes" in data
    assert "semantic_connections" in data
    assert len(data["semantic_connections"]) > 0
