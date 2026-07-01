from pydantic import BaseModel, Field
from typing import List, Optional

class PatientBasicInput(BaseModel):
    age: float = Field(..., description="Age in years", ge=10, le=100)
    weight_kg: float = Field(..., description="Weight in kilograms", ge=30, le=250)
    height_cm: float = Field(..., description="Height in centimeters", ge=100, le=250)
    waist_inch: float = Field(..., description="Waist circumference in inches", ge=20, le=100)
    hip_inch: float = Field(..., description="Hip circumference in inches", ge=20, le=100)
    cycle_regularity: str = Field(..., description="Menstrual cycle regularity: 'regular' or 'irregular'")
    dietary_preference: str = Field(..., description="Dietary preference: 'veg', 'non-veg', or 'vegan'")
    allergies: List[str] = Field(default=[], description="List of food allergies (e.g. ['nuts', 'dairy'])")
    symptoms: List[str] = Field(default=[], description="List of PCOS symptoms (e.g. ['acne', 'hirsutism', 'weight_gain', 'fatigue'])")
    goals: List[str] = Field(default=[], description="User health goals (e.g. ['weight_loss', 'fertility', 'energy'])")
    exercise_hours_per_week: float = Field(default=0.0, description="Hours of physical exercise per week", ge=0)

class PatientAdvancedInput(PatientBasicInput):
    # Optional clinical values from lab reports
    fasting_glucose: Optional[float] = Field(None, description="Fasting Blood Glucose in mg/dL")
    fasting_insulin: Optional[float] = Field(None, description="Fasting Insulin in uIU/mL")
    lh: Optional[float] = Field(None, description="Luteinizing Hormone in mIU/mL")
    fsh: Optional[float] = Field(None, description="Follicle Stimulating Hormone in mIU/mL")
    amh: Optional[float] = Field(None, description="Anti-Müllerian Hormone in ng/mL")
    tsh: Optional[float] = Field(None, description="Thyroid Stimulating Hormone in uIU/mL")
    prolactin: Optional[float] = Field(None, description="Prolactin in ng/mL")
    progesterone: Optional[float] = Field(None, description="Progesterone in ng/mL")
    vit_d: Optional[float] = Field(None, description="Vitamin D3 in ng/mL")
    follicle_num_l: Optional[int] = Field(None, description="Antral Follicle Count Left Ovary")
    follicle_num_r: Optional[int] = Field(None, description="Antral Follicle Count Right Ovary")
    follicle_size_l: Optional[float] = Field(None, description="Average Follicle Size Left Ovary in mm")
    follicle_size_r: Optional[float] = Field(None, description="Average Follicle Size Right Ovary in mm")
    diabetes_status: Optional[bool] = Field(False, description="Whether patient is diagnosed with diabetes")
    hypertension_status: Optional[bool] = Field(False, description="Whether patient is diagnosed with hypertension")

class PatientProfile(BaseModel):
    # Base input variables
    age: float
    weight_kg: float
    height_cm: float
    waist_inch: float
    hip_inch: float
    cycle_regularity: str
    dietary_preference: str
    allergies: List[str]
    symptoms: List[str]
    goals: List[str]
    exercise_hours_per_week: float
    
    # Advanced variables (might be None)
    fasting_glucose: Optional[float] = None
    fasting_insulin: Optional[float] = None
    lh: Optional[float] = None
    fsh: Optional[float] = None
    amh: Optional[float] = None
    tsh: Optional[float] = None
    prolactin: Optional[float] = None
    progesterone: Optional[float] = None
    vit_d: Optional[float] = None
    follicle_num_l: Optional[int] = None
    follicle_num_r: Optional[int] = None
    follicle_size_l: Optional[float] = None
    follicle_size_r: Optional[float] = None
    diabetes_status: bool
    hypertension_status: bool
    
    # Derived clinical variables
    bmi: float
    waist_to_hip_ratio: float
    homa_ir: Optional[float] = None
    lh_fsh_ratio: Optional[float] = None
    obesity_status: str
    insulin_resistance_risk: str
    hormonal_imbalance_severity: str
    inflammation_risk: str
    cardiovascular_risk: str
    exercise_habits: str
    caloric_requirement: float
    protein_requirement_g: float

class FoodItem(BaseModel):
    food_id: int
    food_name: str
    category: str
    calories: float
    protein: float
    carbs: float
    fat: float
    fiber: float
    glycemic_index: float
    glycemic_load: float
    sodium_mg: float
    potassium_mg: Optional[float] = None
    magnesium_mg: Optional[float] = None
    calcium_mg: Optional[float] = None
    vitamin_d_mcg: Optional[float] = None
    zinc_mg: Optional[float] = None
    omega3_g: Optional[float] = None
    saturated_fat_g: Optional[float] = None
    
    # Custom Derived health scores
    pcos_friendliness_score: float
    insulin_resistance_suitability: float
    hormonal_health_score: float
    anti_inflammatory_potential: float
    weight_management_score: float
    heart_health_indicator: float

class MealPlanRequest(BaseModel):
    patient_data: PatientAdvancedInput
    cuisine_preference: Optional[str] = Field("indian", description="Cuisine style preference (e.g. 'indian', 'mediterranean', 'western')")
    duration_days: Optional[int] = Field(1, description="Generate meal plan for N days (1 to 7)", ge=1, le=7)
    budget: Optional[str] = Field("medium", description="Budget constraints: 'low', 'medium', 'high'")
    groq_model: Optional[str] = Field("llama-3.3-70b-versatile", description="Groq model name to use")
