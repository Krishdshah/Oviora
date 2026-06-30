# Oviora AI Platform API Contracts

## Base URL
`/api/v1`

## Engines

### Clinical Risk Engine (CRE-v1.0)
Responsible for AI PCOS Risk Assessment and overall clinical risk profiling based on user data.

#### `POST /api/v1/clinical-risk/predict`
- **Description**: Analyzes clinical parameters and predicts PCOS risk score.
- **Request Body**: (to be defined by `feature_schema.json`)
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
    "dynamic_features": [<list of dynamic biomarkers>],
    "static_features": [<list of static patient features>],
    "fold_id": 1
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "prediction": 14.2,
    "confidence": 0.92,
    "cycle_phase": "ovulation",
    "predicted_days_to_ovulation": 2,
    "model": "ensemble_meta_learner_v2"
  }
  ```

#### `GET /api/v1/pcos-cycle/metrics`
- **Description**: Returns model performance metrics across all 5 folds.
- **Response**: `200 OK`
  ```json
  {
    "mae": 2.34,
    "rmse": 3.12,
    "r2_score": 0.88,
    "cross_validation_folds": 5,
    "ensemble_type": "meta_learner"
  }
  ```

#### `POST /api/v1/pcos-cycle/batch-predict`
- **Description**: Batch predictions for multiple patients.
- **Request Body**:
  ```json
  {
    "patients": [
      {"id": "p1", "dynamic_features": [...], "static_features": [...]},
      {"id": "p2", "dynamic_features": [...], "static_features": [...]}
    ]
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "results": [
      {"patient_id": "p1", "prediction": 14.2, "confidence": 0.92},
      {"patient_id": "p2", "prediction": 9.8, "confidence": 0.85}
    ],
    "batch_size": 2,
    "processing_time_ms": 145
  }
  ```

---

### Future Engines
- Lab Intelligence Engine (LIE-v1.0)
- Vision Intelligence Engine (VIE-v1.0)
- Recommendation Intelligence Engine (RIE-v1.0)
- Nutrition Intelligence Engine (NIE-v1.0)
- Conversational Medical Assistant (CMA-v1.0)
