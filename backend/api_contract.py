from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class CyclePredictionRequest(BaseModel):
    last_period_start_date: str = Field(..., description="YYYY-MM-DD format")
    age: int = Field(25, ge=12, le=60)
    height: float = Field(165.0, description="Height in cm")
    weight: float = Field(65.0, description="Weight in kg")
    bmi: float = Field(23.9, gt=0)
    previous_cycle_lengths: List[int] = Field(..., min_items=1, description="List of previous cycle lengths")

class FertileWindow(BaseModel):
    start: int
    end: int

class HormoneLevels(BaseModel):
    estrogen: int
    progesterone: int
    lh: int
    fsh: int

class CyclePredictionResponse(BaseModel):
    cycle_day: int
    phase: str
    days_until_next_period: int
    predicted_cycle_length: int
    predicted_ovulation_day: int
    fertile_window: FertileWindow
    hormones: HormoneLevels
    confidence: int
