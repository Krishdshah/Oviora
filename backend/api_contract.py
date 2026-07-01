from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class PCOSCyclePredictRequest(BaseModel):
    last_period_start_date: str = Field(..., description="YYYY-MM-DD format")
    age: int = Field(25, ge=12, le=60)
    height: float = Field(165.0, description="Height in cm")
    weight: float = Field(65.0, description="Weight in kg")
    bmi: float = Field(23.9, gt=0)
    previous_cycle_lengths: List[int] = Field(..., min_items=1, description="List of previous cycle lengths")
    pcos_diagnosed: bool = Field(False, description="Is PCOS diagnosed?")
    sleep_hours: float = Field(7.0, description="Average sleep hours")
    stress_score: float = Field(4.0, description="Average stress score (0-10)")

class PCOSCyclePredictResponse(BaseModel):
    predicted_cycle_length: float
    prediction_confidence_score: float
    confidence_percent: int
    risk_level: str
    risk_score: float
    risk_color: str
    risk_description: str
    ovulation_day_of_cycle: int
    fertile_window_days: str
    last_period_start_date: Optional[str]
    estimated_next_period_date: Optional[str]
    estimated_ovulation_date: Optional[str]
    fertile_window_dates: Optional[str]
    days_until_ovulation: Optional[int]
    days_until_next_period: Optional[int]
    cycle_day_today: Optional[int]
    cycle_regularity: str
    pcos_profile_status: str
    why_this_prediction: str
    top_contributing_features: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    model_predictions_breakdown: Dict[str, float]
    model_agreement_std: float
    shap_plot: str
    generated_at: str
    engine: str

class CyclePredictRequest(BaseModel):
    last_period_start_date: str = Field(..., description="YYYY-MM-DD format")
    age: int = Field(25, ge=12, le=60)
    height: float = Field(165.0, description="Height in cm")
    weight: float = Field(65.0, description="Weight in kg")
    bmi: float = Field(23.9, gt=0)
    previous_cycle_lengths: List[int] = Field(..., min_items=1, description="List of previous cycle lengths")

class CycleFertileWindow(BaseModel):
    start: int
    end: int

class CyclePredictResponse(BaseModel):
    cycle_day: int
    phase: str
    phase_reason: str
    days_until_next_period: int
    predicted_cycle_length: int
    predicted_ovulation_day: int
    fertile_window: CycleFertileWindow
    hormones: Dict[str, int]
    confidence: int
    recommendation_context: Dict[str, bool]
    engine_version: str
    model_version: str

class ClinicalRiskPredictRequest(BaseModel):
    features: Dict[str, float] = Field(..., description="Dictionary of clinical features mapping to schema")

class ClinicalRiskPredictResponse(BaseModel):
    risk_score: float
    risk_level: str
    factors: List[str]

class HormoneAnalysisResponse(BaseModel):
    success: bool = True
    error: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class NutritionRankRequest(BaseModel):
    age: float = Field(..., ge=10, le=100)
    weight_kg: float = Field(..., ge=30, le=250)
    height_cm: float = Field(..., ge=100, le=250)
    waist_inch: float = Field(..., ge=20, le=100)
    hip_inch: float = Field(..., ge=20, le=100)
    cycle_regularity: str = Field(..., pattern="^(regular|irregular)$")
    dietary_preference: str = Field(..., pattern="^(Vegetarian|Non-Vegetarian|veg|non-veg)$")
    allergies: List[str] = Field(default=[])
    symptoms: List[str] = Field(default=[])
    goals: List[str] = Field(default=[])
    exercise_hours_per_week: float = Field(..., ge=0, le=100)
    fasting_glucose: Optional[float] = None
    fasting_insulin: Optional[float] = None
    lh: Optional[float] = None
    fsh: Optional[float] = None
    amh: Optional[float] = None
    vit_d: Optional[float] = None
    diabetes_status: bool = False
    hypertension_status: bool = False

class FoodRecommendation(BaseModel):
    food_id: int
    food_name: str
    category: str
    calories: float
    protein: float
    carbs: float
    fat: float
    fiber: float
    glycemic_index: float
    pcos_friendliness_score: float
    ranking_score: float
    is_avoided: bool
    explanation: str

class NutritionRankResponse(BaseModel):
    patient_profile: Dict[str, Any]
    recommendations: List[FoodRecommendation]

class MealPlanRequest(BaseModel):
    patient_data: NutritionRankRequest
    cuisine_preference: str = "Indian"
    duration_days: int = 5
    budget: str = "Medium"
    groq_model: str = "llama-3.3-70b-versatile"

class MealPlanResponse(BaseModel):
    success: bool = True
    meal_plan: Dict[str, Any]
    grocery_list: Dict[str, List[str]]
    healthy_swaps: List[Dict[str, str]]
    clinical_explanation: str
