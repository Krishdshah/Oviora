import os
import sys
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import Dict, Any, List

from nutrition_app.config import settings
from nutrition_app.data_pipeline.schemas import PatientAdvancedInput, PatientProfile, MealPlanRequest
from nutrition_app.data_pipeline.preprocessor import preprocess_patient_data, build_feature_stores
from nutrition_app.knowledge_graph.graph_manager import get_graph_manager, FoodKnowledgeGraph
from nutrition_app.recommendation.ranker import get_ranker_service, LGBMRankerService
from nutrition_app.recommendation.explainer import get_shap_explainer, SHAPExplainerService
from nutrition_app.llm.groq_service import get_groq_service, GroqMealPlannerService

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-powered personalized nutrition recommendation system for women with PCOS",
    version="1.0.0"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global status tracker
training_in_progress = False

@app.on_event("startup")
def startup_event():
    print("Starting Oviora NutriAI Backend...")
    # 1. Build features if missing
    if not os.path.exists(settings.PATIENT_STORE_PATH) or not os.path.exists(settings.FOOD_STORE_PATH):
        try:
            build_feature_stores()
        except Exception as e:
            print(f"Warning: Could not build feature stores on startup: {e}")
            
    # 2. Trigger graph initialization
    try:
        get_graph_manager()
    except Exception as e:
        print(f"Warning: Could not initialize Knowledge Graph on startup: {e}")
        
    # 3. Trigger ranker load
    try:
        get_ranker_service()
    except Exception as e:
        print(f"Warning: Could not load LTR model on startup: {e}")

@app.get("/api/v1/health")
def health_check():
    ranker = get_ranker_service()
    graph = get_graph_manager()
    
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "feature_stores": {
            "patient_store_exists": os.path.exists(settings.PATIENT_STORE_PATH),
            "food_store_exists": os.path.exists(settings.FOOD_STORE_PATH)
        },
        "model": {
            "loaded": ranker.model is not None,
            "path": settings.MODEL_PATH
        },
        "knowledge_graph": {
            "nodes_count": graph.graph.number_of_nodes() if graph.graph else 0,
            "edges_count": graph.graph.number_of_edges() if graph.graph else 0
        }
    }

@app.post("/api/v1/pipeline/train")
def train_pipeline(background_tasks: BackgroundTasks):
    global training_in_progress
    if training_in_progress:
        return {"status": "error", "message": "Model training already in progress."}
        
    ranker = get_ranker_service()
    
    # Run preprocessor if data files are missing
    if not os.path.exists(settings.PATIENT_STORE_PATH) or not os.path.exists(settings.FOOD_STORE_PATH):
        build_feature_stores()
        
    def train_task():
        global training_in_progress
        try:
            ranker.train()
        finally:
            training_in_progress = False
            
    training_in_progress = True
    background_tasks.add_task(train_task)
    return {"status": "success", "message": "Training job started in background."}

@app.post("/api/v1/recommend/rank")
def get_recommendations(patient_input: PatientAdvancedInput):
    # 1. Preprocess and derive metrics
    profile = preprocess_patient_data(patient_input)
    
    # 2. Get ranked foods from LTR model
    ranker = get_ranker_service()
    if ranker.model is None:
        raise HTTPException(
            status_code=503, 
            detail="LightGBM Ranker model is not loaded. Please train the model first by POSTing to /api/v1/pipeline/train."
        )
        
    ranked_foods = ranker.rank_foods_for_patient(profile)
    
    # 3. Add SHAP explanations for top 5 and bottom 5 (to avoid heavy computation on all)
    explainer = get_shap_explainer()
    
    # Explain Top 5
    for food in ranked_foods[:5]:
        explanation = explainer.explain_recommendation(profile, food)
        food['explanation'] = explanation.get('narrative_explanation', '')
        food['shap_score'] = explanation.get('shap_score', 0.0)
        
    # Explain Bottom 5
    for food in [f for f in ranked_foods if f['is_avoided']][:5]:
        explanation = explainer.explain_recommendation(profile, food)
        food['explanation'] = explanation.get('narrative_explanation', '')
        food['shap_score'] = explanation.get('shap_score', 0.0)
        
    return {
        "patient_profile": profile,
        "recommendations": ranked_foods
    }

@app.post("/api/v1/recommend/meal-plan")
def get_meal_plan(request: MealPlanRequest):
    # 1. Derive profile and rank foods
    profile = preprocess_patient_data(request.patient_data)
    ranker = get_ranker_service()
    if ranker.model is None:
        raise HTTPException(
            status_code=503,
            detail="LightGBM Ranker model is not loaded. Please train the model first by POSTing to /api/v1/pipeline/train."
        )
        
    all_ranked = ranker.rank_foods_for_patient(profile)
    
    # 2. Select diverse top 15 foods for the meal planner context
    from nutrition_app.recommendation.ranker import get_diverse_recommendations
    ranked_foods = get_diverse_recommendations(all_ranked, profile, cuisine=request.cuisine_preference, limit=15)
    
    # 3. Compute SHAP for the diverse recommended items
    explainer = get_shap_explainer()
    for food in ranked_foods:
        explanation = explainer.explain_recommendation(profile, food)
        food['explanation'] = explanation.get('narrative_explanation', '')
        
    # 4. Call Groq service
    groq = get_groq_service()
    meal_plan = groq.generate_meal_plan(
        profile=profile,
        ranked_foods=ranked_foods,
        cuisine=request.cuisine_preference,
        duration_days=request.duration_days,
        budget=request.budget,
        model_name=request.groq_model
    )
    
    return meal_plan

@app.get("/api/v1/knowledge-graph/food/{food_name}")
def get_food_graph_details(food_name: str):
    graph = get_graph_manager()
    details = graph.get_food_context(food_name)
    if "error" in details:
        raise HTTPException(status_code=404, detail=details["error"])
    return details

@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    # We will read the dashboard index.html from a template or serve a built-in string
    template_path = os.path.join(settings.BASE_DIR, "app", "templates", "index.html")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "<h3>Dashboard template app/templates/index.html not found.</h3>"
