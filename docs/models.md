# Oviora Machine Learning Models

This document provides a detailed overview of the machine learning models and AI engines powering the Oviora platform. The platform is designed around a hybrid AI approach, utilizing deterministic physiological rules, traditional machine learning classifiers, and deep learning vision models.

---

## 1. Clinical Risk Engine

**Objective:** Predict the clinical probability of a user having Polycystic Ovary Syndrome (PCOS) based on a combination of clinical, hormonal, and lifestyle parameters.

- **Status:** ✅ Complete
- **Algorithm:** CatBoost Classifier
- **Dataset:** PCOS Dataset (without infertility) - 541 patients, 41 features.
- **Data Preprocessing:** Imputation of missing values, object-to-numeric conversion, correlation analysis, and feature selection.
- **Performance Metrics:**
  - Accuracy: **90.83%**
  - Precision: **90.62%**
  - Recall: **80.56%**
  - F1 Score: **85.29%**
  - ROC-AUC: **95.66%**

**Top Predictive Features:**
1. Follicle No. (Right & Left)
2. Hair Growth & Skin Darkening
3. Weight Gain & BMI
4. Anti-Müllerian Hormone (AMH)
5. Cycle Regularity

---

## 2. Cycle Intelligence Engine

**Objective:** Predict personalized menstrual cycle characteristics and generate physiological insights, factoring in both regular cycles and PCOS-affected irregular cycles.

- **Status:** ✅ Complete
- **Algorithm:** Linear Regression (for length prediction) + Deterministic Logic (Phase & Hormone Estimation)
- **Dataset:** FedCycle Dataset - 1665 cycles across 102 women.
- **Feature Engineering:** Uses rolling means, rolling standard deviations, BMI, and historical cycle lengths.
- **Data Splitting Strategy:** Group-aware splitting using `ClientID` to prevent data leakage (no patient overlaps between train/test).

**Core Components:**
- **Length Prediction (ML):** Predicts total cycle days based on historical patterns.
- **Day Calculator & Phase Engine:** Deterministically calculates current cycle day and assigns the phase (Follicular, Ovulatory, Luteal, Menstrual).
- **Hormone Estimation Engine:** Provides estimated baseline curves for Estrogen, Progesterone, LH, and FSH based on the predicted phase.

---

## 3. Lab Intelligence Engine (OCR)

**Objective:** Extract clinical biomarkers (e.g., Fasting Insulin, AMH, Testosterone) from uploaded medical lab reports using Optical Character Recognition (OCR) and map them to standard reference ranges.

- **Status:** ✅ Complete (Backend Integrated)
- **Architecture:** PaddleOCR End-to-End Deep Learning Pipeline
- **Pipeline Components:**
  1. **Document Analysis (`UVDoc`, `PP-LCNet`):** Dewarping and layout analysis. Corrects document skew and detects structural boundaries.
  2. **Text Detection (`PP-OCRv6_medium_det`):** Detects regions of text and generates bounding boxes.
  3. **Orientation Classification (`PP-LCNet_x1_0_textline_ori`):** Determines the orientation of text within bounding boxes and rotates it for accurate reading.
  4. **Text Recognition (`PP-OCRv6_medium_rec`):** Extracts string characters from the oriented bounding boxes.

---

## 4. Planned Future Models

The following AI engines are currently in the roadmap and are simulated via mock data in the frontend:
- **Nutrition Intelligence Engine:** To provide meal plans tailored to insulin resistance and current cycle phases.
- **Recommendation Engine:** To generate daily actionable tasks (e.g., taking specific supplements).
- **AI Health Coach:** Conversational LLM assistant utilizing user health context.
- **Clinician Summary Engine:** Generates PDF exports of user health trends formatted for OBGYN visits.
