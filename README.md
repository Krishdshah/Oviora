# 🌸 Oviora

> **Your AI Copilot for PCOS & Women's Health**

Oviora is an AI-powered women's healthcare platform designed to provide personalized PCOS risk assessment, cycle intelligence, lab report interpretation, nutrition guidance, clinician summaries, and conversational health support.

Unlike traditional period trackers, Oviora combines machine learning, deterministic physiological modeling, and Large Language Models into a unified AI ecosystem.

---

# Vision

Build the world's most comprehensive AI-powered PCOS management platform by combining:

- Clinical Machine Learning
- Time-Series Intelligence
- Document AI
- Explainable AI
- Personalized Health Recommendations

---

# AI Architecture

```
                    Oviora AI

        ┌──────────────────────────────┐
        │ Clinical Risk Engine         │
        └──────────────┬───────────────┘
                       │
        ┌──────────────▼───────────────┐
        │ Cycle Intelligence Engine    │
        └──────────────┬───────────────┘
                       │
        ┌──────────────▼───────────────┐
        │ Lab Intelligence Engine      │
        └──────────────┬───────────────┘
                       │
        ┌──────────────▼───────────────┐
        │ Nutrition Intelligence       │
        └──────────────┬───────────────┘
                       │
        ┌──────────────▼───────────────┐
        │ Recommendation Engine        │
        └──────────────┬───────────────┘
                       │
        ┌──────────────▼───────────────┐
        │ AI Health Coach              │
        └──────────────┬───────────────┘
                       │
        ┌──────────────▼───────────────┐
        │ Clinician Summary Engine     │
        └──────────────────────────────┘
```

---

# AI Models

| Model | Status | Progress |
|--------|--------|----------|
| Clinical Risk Engine | ✅ Complete | 100% |
| Cycle Intelligence Engine | ✅ Complete | 100% |
| Lab Intelligence Engine | ✅ Complete | 100% |
| Nutrition Intelligence Engine | ⏳ Planned | 0% |
| Recommendation Engine | ⏳ Planned | 0% |
| AI Coach | ⏳ Planned | 0% |
| Clinician Summary Engine | ⏳ Planned | 0% |

---

# Model 1 — Clinical Risk Engine

## Objective

Predict the probability of PCOS using clinical, hormonal, and lifestyle parameters.

### Dataset

**PCOS Data without Infertility**

- Patients: **541**
- Features: **41**
- Target:
  - PCOS (Yes/No)

### Data Cleaning

- Removed empty column
- Converted object columns to numeric
- Missing value imputation
- Correlation analysis
- Feature importance analysis

### Features

- Age
- BMI
- Weight
- Hormones
- Follicle Count
- Cycle Regularity
- Lifestyle
- Skin/Hair Symptoms
- Blood Markers
- Endometrium
- Ultrasound Measurements

### Algorithms Benchmarked

- Logistic Regression
- Random Forest
- XGBoost
- CatBoost

### Final Model

**CatBoost Classifier**

### Performance

| Metric | Score |
|---------|-------|
| Accuracy | **90.83%** |
| Precision | **90.62%** |
| Recall | **80.56%** |
| F1 Score | **85.29%** |
| ROC-AUC | **95.66%** |

### Top Predictive Features

1. Follicle No. (Right)
2. Follicle No. (Left)
3. Hair Growth
4. Skin Darkening
5. Weight Gain
6. AMH
7. Cycle Regularity
8. Pimples
9. BMI
10. Weight

---

# Model 2 — Cycle Intelligence Engine

## Objective

Predict personalized menstrual cycle characteristics and generate physiological insights.

### Dataset

**Menstrual Cycle Dataset (FedCycle)**

- Total Cycles: **1665**
- Usable Samples: **957**
- Unique Women: **102**
- Features: **80**

### Feature Engineering

- Previous Cycle Length
- Previous Two Cycle Lengths
- Rolling Mean
- Rolling Standard Deviation
- BMI
- Height
- Weight
- Age
- Cycle Number

### Leakage Prevention

Group-aware splitting using **ClientID**

No woman appears in both training and testing.

### Algorithms Benchmarked

| Algorithm | RMSE | MAE | R² |
|------------|------|------|------|
| Linear Regression | **3.52** | **2.40** | **0.421** |
| Random Forest | 3.76 | 2.56 | 0.340 |
| CatBoost | 4.02 | 2.63 | 0.245 |
| XGBoost | 4.17 | 2.86 | 0.185 |

### Final Model

**Linear Regression**

---

# Cycle Intelligence Engine

Components

- Cycle Length Prediction (ML)
- Cycle Day Calculator
- Ovulation Estimator
- Phase Engine
- Hormone Estimation Engine
- Response Builder

---

# Model 3 — Lab Intelligence Engine (OCR)

## Objective

Extract clinical biomarkers from medical lab reports using Optical Character Recognition (OCR) and map them to standard reference ranges.

### Architecture

**PaddleOCR End-to-End Pipeline**
- **Document Analysis**: UVDoc, PP-LCNet (Dewarping & Layout analysis)
- **Text Detection**: PP-OCRv6_medium_det (Bounding boxes)
- **Orientation**: PP-LCNet_x1_0_textline_ori (Text alignment)
- **Recognition**: PP-OCRv6_medium_rec (Text extraction)

---

# Tech Stack

## AI

- CatBoost
- Linear Regression
- Scikit-learn
- NumPy
- Pandas

## Backend

- FastAPI
- Pydantic
- Python

## Frontend

- React
- TypeScript
- Tailwind CSS

## Deployment

- Docker
- Render
- Vercel

---

# Datasets

## Clinical Risk Engine

PCOS Dataset without Infertility

Source:
https://www.kaggle.com/datasets/prasoonkottarathil/polycystic-ovary-syndrome-pcos

---

## Cycle Intelligence Engine

FedCycle Dataset

Source:
https://www.kaggle.com/datasets/nikitabisht/menstrual-cycle-data

Mirror:
https://www.kaggle.com/datasets/echekwuelijah/fertility-and-menstrual-health-data

---

# Repository Structure

```text
Oviora/
├── backend/       # FastAPI monolith backend
├── frontend/      # Next.js React frontend
├── models/        # AI models and training notebooks
└── docs/          # Documentation and assets
```

---

# Getting Started

## Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL (if applicable)

## Installation & Running

### 1. Clone the repository
```bash
git clone https://github.com/Krishdshah/Oviora.git
cd Oviora
```

### 2. Start the Backend (FastAPI)
```bash
cd backend
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
# source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```
*Note: Make sure to set up your `.env` file in the backend directory according to `.env.example` if one exists.*

### 3. Start the Frontend (Next.js)
Open a new terminal window:
```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000` and the backend API at `http://localhost:8000`.

---

# Current Progress

```
Clinical Risk Engine          ██████████ 100%

Cycle Intelligence Engine     ██████████ 100%

Lab Intelligence Engine       ██████████ 100%

Nutrition Engine              ░░░░░░░░░░ 0%

Recommendation Engine         ░░░░░░░░░░ 0%

AI Coach                      ░░░░░░░░░░ 0%

Clinician Summary             ░░░░░░░░░░ 0%
```

---

# Roadmap

### Phase 1 ✅

- Clinical Risk Prediction
- Cycle Intelligence
- Lab Intelligence Engine
- Backend APIs
- Frontend Dashboard

### Phase 2

- Nutrition Engine
- Recommendation Engine

### Phase 3

- AI Coach
- Clinician Summary
- Mobile App
- Wearable Integration

---

# License

MIT License

---

# Contributors

Developed by **Krish D Shah**