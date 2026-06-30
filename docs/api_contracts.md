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

### Future Engines
- Lab Intelligence Engine (LIE-v1.0)
- Vision Intelligence Engine (VIE-v1.0)
- Recommendation Intelligence Engine (RIE-v1.0)
- Nutrition Intelligence Engine (NIE-v1.0)
- Conversational Medical Assistant (CMA-v1.0)
