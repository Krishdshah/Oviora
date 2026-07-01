# Oviora AI Platform API Contracts

## Base URL
`/api/v1`

## Engines

### Clinical Risk Engine (CRE-v1.0)
Responsible for AI PCOS Risk Assessment and overall clinical risk profiling based on user data.

#### `POST /api/v1/clinical-risk/predict`
- **Description**: Analyzes clinical parameters and predicts PCOS risk score.
- **Request Body**:
  ```json
  {
    "features": {
      " Age (yrs)": 28,
      "Weight (Kg)": 65,
      "...": "..."
    }
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "risk_score": 0.85,
    "risk_level": "High",
    "factors": ["High BMI", "Irregular Cycles"]
  }
  ```

---

### PCOS Cycle & Ovulation Intelligence Engine (POE-v2.0)
Predicts PCOS cycle patterns and ovulation timing using ensemble machine learning models with 5-fold cross-validation.

#### `POST /api/v1/pcos-cycle/predict`
- **Description**: Predicts ovulation timing and cycle phase based on PCOS patient features.
- **Request Body**:
  ```json
  {
    "last_period_start_date": "2026-06-15",
    "age": 28,
    "height": 165.0,
    "weight": 65.0,
    "bmi": 23.9,
    "previous_cycle_lengths": [30, 29, 31, 28, 30],
    "pcos_diagnosed": true,
    "sleep_hours": 6.5,
    "stress_score": 5.0
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "predicted_cycle_length": 32.5,
    "prediction_confidence_score": 0.88,
    "confidence_percent": 88,
    "risk_level": "Slightly Irregular",
    "risk_score": 0.45,
    "ovulation_day_of_cycle": 18
  }
  ```

---

### Standard Cycle Intelligence Engine
Predicts standard cycle patterns and ovulation timing for users without PCOS.

#### `POST /api/v1/cycle/predict`
- **Description**: Predicts cycle data.
- **Request Body**:
  ```json
  {
    "last_period_start_date": "2026-06-15",
    "age": 25,
    "height": 165.0,
    "weight": 65.0,
    "bmi": 23.9,
    "previous_cycle_lengths": [28, 29, 28]
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "cycle_day": 16,
    "predicted_cycle_length": 28,
    "predicted_ovulation_day": 14
  }
  ```

---

### Hormone Analysis Engine
Responsible for OCR parsing and AI analysis of laboratory test reports.

#### `POST /api/v1/labs/upload`
- **Description**: Uploads a lab report file (PDF/Image) for parsing and AI analysis.
- **Request Format**: `multipart/form-data`
  - `file`: The lab report file.
- **Response**: `200 OK`
  ```json
  {
    "success": true,
    "data": {
       "executive_summary": "...",
       "hormonal_assessment": "..."
    }
  }
  ```
---

### Personalized Nutrition Recommendation Engine (PNRE-v1.0)
Uses LightGBM LambdaMART ranking and SHAP explainability combined with Groq LLM to rank clinical foods and generate customized, cuisine-aware daily meal plans.

#### `POST /api/v1/recommend/rank`
- **Description**: Computes dynamic personalized food rankings based on basic symptoms or advanced clinical lab profiles.
- **Request Body**: `NutritionRankRequest`
- **Response**: `200 OK` (`NutritionRankResponse`)
  ```json
  {
    "patient_profile": { ... },
    "recommendations": [
      {
        "food_id": 12,
        "food_name": "Spinach",
        "category": "Meal/Vegetable",
        "calories": 23.0,
        "protein": 2.9,
        "carbs": 3.6,
        "fat": 0.4,
        "fiber": 2.2,
        "glycemic_index": 15.0,
        "pcos_friendliness_score": 88.5,
        "ranking_score": 2.45,
        "is_avoided": false,
        "explanation": "Dietary fiber (+0.45) supports stable glucose levels."
      }
    ]
  }
  ```

#### `POST /api/v1/recommend/meal-plan`
- **Description**: Generates multi-day, cuisine-filtered personalized meal plans, grocery shopping lists, and clinical explanations using Llama 3.3 or Mixtral models.
- **Request Body**: `MealPlanRequest`
- **Response**: `200 OK` (`MealPlanResponse`)

#### `GET /api/v1/knowledge-graph/food/{food_name}`
- **Description**: Queries semantic node contextual details and relations from the NetworkX Knowledge Graph case-insensitively.
- **Response**: `200 OK`

---

### Future Engines
- Lab Intelligence Engine (LIE-v1.0)
- Vision Intelligence Engine (VIE-v1.0)
- Recommendation Intelligence Engine (RIE-v1.0)
- Conversational Medical Assistant (CMA-v1.0)
