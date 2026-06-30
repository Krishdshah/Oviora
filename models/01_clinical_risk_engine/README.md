# Clinical Risk Engine (CRE-v1.0)

This directory contains the artifacts for the first AI engine of the Oviora platform.

## Files
- `training.ipynb`: Notebook used to train the model.
- `inference.py`: Python module exposing the `predict()` function for production inference.
- `clinical_risk_engine.cbm`: CatBoost model binary.
- `feature_schema.json`: Expected input schema for the model.
- `metrics.json`: Evaluation metrics from training.
