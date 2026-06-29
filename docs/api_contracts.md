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

### Future Engines
- Lab Intelligence Engine (LIE-v1.0)
- Vision Intelligence Engine (VIE-v1.0)
- Cycle Intelligence Engine (CIE-v1.0)
- Recommendation Intelligence Engine (RIE-v1.0)
- Nutrition Intelligence Engine (NIE-v1.0)
- Conversational Medical Assistant (CMA-v1.0)
