# Oviora NutriAI — Personalized PCOS Nutrition Engine

Oviora NutriAI is an AI-powered personalized nutrition recommendation system designed specifically for women with Polycystic Ovary Syndrome (PCOS). The system combines clinical patient data, comprehensive nutritional databases, and Large Language Models (LLMs) to generate highly personalized dietary recommendations.

Rather than treating nutrition as a classification problem (e.g., "healthy" vs. "unhealthy"), Oviora NutriAI implements a **Learning-to-Rank (LTR)** model using **LightGBM LambdaMART**. It learns to rank foods based on a patient's individual metabolic, inflammatory, and hormonal risk indicators, explains recommendation drivers using **SHAP (SHapley Additive exPlanations)**, and maps foods to a **NetworkX Semantic Knowledge Graph** before feeding them to **Groq** to generate complete, personalized meal plans.

---

## 🛠 Architecture & Modular Pipeline

```
                                 [ Clinical PCOS Dataset ]
                                 [ Food Nutrition Data   ]
                                             │
                                             ▼
                                  [ Data Engineering ]
                         (Standardizes, Cleans, Resolves Schemas)
                                             │
                 ┌───────────────────────────┴───────────────────────────┐
                 ▼                                                       ▼
      [ Patient Feature Store ]                               [ Food Feature Store ]
     - Tier 1: Basic Symptoms                                - Nutrient Density & Macros
     - Tier 2: Advanced Labs (Optional)                      - Glycemic Index & Glycemic Load
     - Fallback Inference Risk Scores                        - Heart, Hormone, Inflammation Scores
                 │                                                       │
                 │                      ┌────────────────────────────────┤
                 │                      │                                ▼
                 │                      │                  [ Food Knowledge Graph ]
                 │                      │                 - Nodes: Foods & Categories (Case-insensitive)
                 │                      │                 - Edges: Semantic properties
                 │                      │                                │
                 ▼                      ▼                                │
            [ Learning-to-Rank Engine (LTR) ]                            │
            (LightGBM LambdaMART Ranker Model)                           │
                         │                                               │
                         ▼                                               │
            [ SHAP Explainability Service ]                              │
            (Calculates feature attribution)                              │
                         │                                               │
                         └──────────────┬────────────────────────────────┘
                                        ▼
                                     [ Groq ]
                           (Llama 3.3 70B / Mixtral 8x7B)
                         (Generates Meal Plans & Groceries)
                                        │
                                        ▼
                                 [ FastAPI API ]
```

1. **Data Engineering Layer (`app/data_pipeline/preprocessor.py`)**:
   Cleans, validates, merges, and derives characteristics for both datasets.
   - **Patient Store**: Supports two-tier inputs (Basic Symptoms vs. Advanced Lab Reports). Missing clinical lab data triggers fallback heuristics to estimate insulin resistance, hormonal imbalances, and inflammation.
   - **Food Store**: Calculates custom clinical indices: *PCOS Friendliness*, *Insulin Resistance Suitability*, *Hormonal Health*, *Anti-Inflammatory Potential*, *Heart Health*, and *Weight Management Compatibility*.
2. **Food Knowledge Graph (`app/knowledge_graph/graph_manager.py`)**:
   Constructs a semantic graph using NetworkX linking foods to categories, glycemic classes, nutrient rich-attributes (e.g., Omega3-Rich, Zinc-Rich), and suitability profiles. Queries are fully case-insensitive.
3. **LTR Recommendation Engine (`app/recommendation/ranker.py`)**:
   Pairs patients with food items and computes a 0-5 suitability rating using clinical expert rules. Trains a `LightGBM` LambdaRank model grouped by `PatientID` to predict personalized food lists. Enforces **name-based deduplication** and **cuisine-specific filtering** (e.g. Indian/Mediterranean) so that recommended ingredient lists match the cuisine preference.
4. **SHAP Explainability (`app/recommendation/explainer.py`)**:
   Runs SHAP TreeExplainer on top of LightGBM predictions to output exact feature attributions, explaining *why* foods were suggested or penalized.
5. **Groq Reasoning Layer (`app/llm/groq_service.py`)**:
   Translates LTR food rankings, SHAP explanations, and semantic graph contexts into tailored daily meal plans, grocery shopping lists, and clinical explanations using Llama 3.3 or Mixtral models.

---

## 📂 Project Structure

```
.
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI entry point
│   ├── config.py                   # Configuration & Path specifications
│   ├── data_pipeline/
│   │   ├── preprocessor.py         # Merging, Cleaning & Feature Store builders
│   │   └── schemas.py              # Pydantic schemas (Basic & Advanced Inputs)
│   ├── knowledge_graph/
│   │   └── graph_manager.py        # NetworkX Semantic Graph Builder
│   ├── recommendation/
│   │   ├── ranker.py               # LTR training, rules & LGBMRanker service
│   │   └── explainer.py            # SHAP TreeExplainer service
│   └── llm/
│       └── groq_service.py         # Groq prompt assembly & meal plan compiler
├── scripts/
│   └── train_model.py              # Training execution script
└── tests/
    └── test_api.py                 # Automated testing suite
```

---

## ⚡️ Quickstart & Setup

### 1. Prerequisites & Virtual Environment
Ensure you have Python 3.10+ installed.

```bash
# Clone the repository
git clone https://github.com/Laksh718/Oviora.git
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory to set your Groq API key:
```env
GROQ_API_KEY=your_actual_groq_api_key_starts_with_gsk_
```
*(If the key is left unconfigured, the application strictly raises a runtime error when generating meal plans. No mock fallback data is used).*

### 3. Ingest & Train the LTR Model
Execute the training script to ingest the raw datasets, build the feature stores, and fit the LightGBM LambdaMART ranker:
```bash
python scripts/train_model.py
```
This output should confirm feature store creation and display model accuracy metrics (NDCG@10).

### 4. Start the FastAPI Server
```bash
uvicorn app.main:app --reload
```
The server will start at `http://127.0.0.1:8000`.

---

## 📊 Glassmorphic Testing Dashboard
Opening `http://127.0.0.1:8000/` in your browser will open a premium, interactive dark mode dashboard. You can select symptoms, input basic parameters, toggle advanced clinical metrics, click **Rank Foods (LTR)**, and request **Groq Meal Plans** to visualize the output immediately in a UI.

---

## 🔌 API Documentation

### 1. Health Status
`GET /api/v1/health`
- **Response**: Details of model loading state, feature stores, and knowledge graph dimensions.

### 2. Rank Foods (LTR + SHAP)
`POST /api/v1/recommend/rank`
- **Request Body (Basic Symptoms)**:
  ```json
  {
    "age": 26,
    "weight_kg": 68,
    "height_cm": 162,
    "waist_inch": 32,
    "hip_inch": 36,
    "cycle_regularity": "irregular",
    "dietary_preference": "veg",
    "allergies": [],
    "symptoms": ["acne", "weight_gain"],
    "goals": ["weight_loss", "regular_cycles"],
    "exercise_hours_per_week": 2.5
  }
  ```
- **Response**: Ranked foods along with SHAP explanations for top suggestions:
  ```json
  {
    "patient_profile": { ... },
    "recommendations": [
      {
        "food_id": 12,
        "food_name": "Spinach",
        "category": "Meal/Vegetable",
        "calories": 23,
        "protein": 2.9,
        "carbs": 3.6,
        "fat": 0.4,
        "fiber": 2.2,
        "glycemic_index": 15,
        "pcos_friendliness_score": 88.5,
        "ranking_score": 2.45,
        "is_avoided": false,
        "explanation": "Dietary fiber (+0.45) was recommended to help stabilize your insulin levels. Anti-inflammatory properties (+0.60) was boosted to help lower chronic systemic inflammation."
      }
    ]
  }
  ```

### 3. Generate Groq Meal Plan
`POST /api/v1/recommend/meal-plan`
- **Request Body**: Same as above (with optional fields `cuisine_preference`, `duration_days`, `budget`, and `groq_model` like `llama-3.3-70b-versatile`).
- **Response**: A complete JSON menu with ingredients, tips, grocery lists, healthy swaps, and clinical reasoning.

### 4. Query Knowledge Graph
`GET /api/v1/knowledge-graph/food/{food_name}`
- **Response**: The semantic attributes and outgoing relationships from NetworkX (e.g. `RICH_IN Magnesium-Rich` -> `IS_SUITABLE_FOR PCOS-Friendly`). Queries are case-insensitive.

---

## 🧪 Running Automated Tests
Run the test suite using pytest:
```bash
pytest tests/
```
