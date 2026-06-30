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
