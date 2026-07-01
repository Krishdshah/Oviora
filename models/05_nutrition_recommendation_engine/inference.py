import os
import sys
from typing import Dict, Any

# Ensure local path is first in sys.path to avoid name collision with top-level app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Force config to load data local to this model directory
os.environ["DATA_DIR"] = os.path.join(BASE_DIR, "data")

from nutrition_app.data_pipeline.schemas import PatientAdvancedInput
from nutrition_app.data_pipeline.preprocessor import preprocess_patient_data
from nutrition_app.recommendation.ranker import get_ranker_service, get_diverse_recommendations
from nutrition_app.recommendation.explainer import get_shap_explainer
from nutrition_app.llm.groq_service import generate_meal_plan_from_groq
from nutrition_app.knowledge_graph.graph_manager import get_graph_manager

ranker = None
explainer = None
graph = None

def load_model():
    global ranker, explainer, graph
    if ranker is None:
        ranker = get_ranker_service()
    if explainer is None:
        explainer = get_shap_explainer()
    if graph is None:
        graph = get_graph_manager()

def predict_rank(input_data: dict) -> dict:
    """
    Ranks food items using LightGBM LTR and explains recommendations using SHAP.
    """
    load_model()
    try:
        patient_input = PatientAdvancedInput(**input_data)
        profile = preprocess_patient_data(patient_input)
        ranked_foods = ranker.rank_foods_for_patient(profile)
        
        top_recs = []
        for food in ranked_foods:
            explanation = explainer.explain_recommendation(profile, food)
            food_rec = {
                "food_id": int(food["food_id"]),
                "food_name": str(food["food_name"]),
                "category": str(food["category"]),
                "calories": float(food["Calories"]),
                "protein": float(food["Protein"]),
                "carbs": float(food["Carbohydrates"]),
                "fat": float(food["Fat"]),
                "fiber": float(food["Fiber"]),
                "glycemic_index": float(food["GlycemicIndex"]),
                "pcos_friendliness_score": float(food["pcos_friendliness_score"]),
                "ranking_score": float(food["ranking_score"]),
                "is_avoided": bool(food["is_avoided"]),
                "explanation": explanation
            }
            top_recs.append(food_rec)
            
        return {
            "patient_profile": profile.model_dump(),
            "recommendations": top_recs
        }
    except Exception as e:
        return {"error": str(e)}

def predict_meal_plan(patient_data: dict, cuisine: str = "Indian", duration: int = 5, budget: str = "Medium", model_name: str = "llama-3.3-70b-versatile") -> dict:
    """
    Generates a personalized daily meal plan using LTR recommendations and Groq LLM.
    """
    load_model()
    try:
        patient_input = PatientAdvancedInput(**patient_data)
        profile = preprocess_patient_data(patient_input)
        all_ranked = ranker.rank_foods_for_patient(profile)
        
        diverse_recs = get_diverse_recommendations(all_ranked, profile, cuisine=cuisine, limit=15)
        
        for food in diverse_recs:
            food["explanation"] = explainer.explain_recommendation(profile, food)
            
        response = generate_meal_plan_from_groq(
            patient_profile=profile,
            ranked_foods=diverse_recs,
            cuisine=cuisine,
            duration=duration,
            budget=budget,
            model_name=model_name
        )
        return response
    except Exception as e:
        return {"error": str(e)}

def get_food_graph(food_name: str) -> dict:
    """
    Retrieves semantic node context from the NetworkX Knowledge Graph.
    """
    load_model()
    details = graph.get_food_context(food_name)
    return details
