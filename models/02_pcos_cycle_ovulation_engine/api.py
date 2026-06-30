"""
api.py — OvulAI Flask REST API
================================
Exposes the OvulAI prediction engine as a JSON API for frontend integration.

Endpoints
---------
GET  /health                          — liveness check
POST /api/predict                     — full prediction with all intelligence layers
GET  /api/last                        — return the most recently computed prediction
GET  /api/shap-plot                   — return the SHAP bar chart image
GET  /api/benchmark                   — return benchmark results for the model comparison card

CORS is fully open so any frontend origin can call this during development.
For production, restrict origins in CORSConfig below.
"""

import os
import sys
import json
import pickle
import warnings
warnings.filterwarnings("ignore")
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# ── Ensure we can import v2_05_predict from the same directory ────────────────
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
from pathlib import Path
from flask import Flask, request, jsonify, send_file, abort
from flask_cors import CORS

# ── Import the OvulAI engine ─────────────────────────────────────────────────
from v2_05_predict import (
    predict,
    DYNAMIC_FEATURES,
    STATIC_FEATURES,
    NUM_DYNAMIC,
    NUM_STATIC,
)

# ── App setup ────────────────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)  # open CORS for all origins — restrict in production

OUTPUT_DIR = Path("output")
FIGURE_DIR = Path("figures")

# ── Benchmark results (pre-computed, stored for the model-comparison card) ───
BENCHMARK_RESULTS = [
    {"model": "Mean Predictor",   "mae": 1.8183, "rmse": 2.3852, "r2": -0.0009},
    {"model": "Prev-Cycle Baseline","mae": 2.2264,"rmse": 2.8663, "r2": -0.4453},
    {"model": "Linear Regression","mae": 1.6931, "rmse": 2.1543, "r2":  0.1835},
    {"model": "Random Forest",    "mae": 1.6507, "rmse": 2.0923, "r2":  0.2299},
    {"model": "XGBoost (Tuned)",  "mae": 1.6532, "rmse": 2.0909, "r2":  0.2309},
    {"model": "LightGBM (Tuned)", "mae": 1.6556, "rmse": 2.0883, "r2":  0.2328},
    {"model": "CatBoost (Tuned)", "mae": 1.6566, "rmse": 2.0907, "r2":  0.2310},
    {"model": "Hybrid Model",     "mae": 1.6961, "rmse": 2.1537, "r2":  0.1840},
    {"model": "Stacked Ensemble", "mae": 1.6517, "rmse": 2.0878, "r2":  0.2332},
]


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def _parse_dynamic(history: list) -> np.ndarray:
    """
    Build the (6, NUM_DYNAMIC) input tensor from the API request's cycle history.

    Each item in `history` is a dict with any of:
      cycle_length, sleep_hours, stress_score

    The function fills up to 6 cycles (pads with the first entry if fewer).
    """
    # Pad or trim to exactly 6 cycles
    while len(history) < 6:
        history.insert(0, history[0] if history else {})
    history = history[-6:]

    dyn = np.zeros((6, NUM_DYNAMIC), dtype=np.float32)
    lengths = [float(h.get("cycle_length", 28)) for h in history]

    for i, h in enumerate(history):
        length = float(h.get("cycle_length", 28))
        sleep  = float(h.get("sleep_hours", 7.0))
        stress = float(h.get("stress_score", 4.0))

        window = lengths[max(0, i-2):i+1]
        window_all = lengths[:i+1]

        if "prev_cycle_length" in DYNAMIC_FEATURES:
            dyn[i, DYNAMIC_FEATURES.index("prev_cycle_length")] = length
        if "rolling_mean_3" in DYNAMIC_FEATURES:
            dyn[i, DYNAMIC_FEATURES.index("rolling_mean_3")] = float(np.mean(window))
        if "rolling_std" in DYNAMIC_FEATURES:
            dyn[i, DYNAMIC_FEATURES.index("rolling_std")] = float(np.std(window_all)) if i > 0 else 0.5
        if "rolling_mean" in DYNAMIC_FEATURES:
            dyn[i, DYNAMIC_FEATURES.index("rolling_mean")] = float(np.mean(window_all))
        if "sleep_hours_cycle" in DYNAMIC_FEATURES:
            dyn[i, DYNAMIC_FEATURES.index("sleep_hours_cycle")] = sleep
        if "stress_score_cycle" in DYNAMIC_FEATURES:
            dyn[i, DYNAMIC_FEATURES.index("stress_score_cycle")] = stress

        # Lag features
        for lag in range(1, 7):
            feat = f"lag{lag}"
            if feat in DYNAMIC_FEATURES and i - lag >= 0:
                dyn[i, DYNAMIC_FEATURES.index(feat)] = lengths[i - lag]

        # Diff features
        if "diff1" in DYNAMIC_FEATURES and i >= 1:
            dyn[i, DYNAMIC_FEATURES.index("diff1")] = lengths[i] - lengths[i-1]

    return dyn


# ─────────────────────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "engine": "OvulAI v3"})


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """
    POST /api/predict

    Request body (JSON):
    {
      "cycle_history": [
        {"cycle_length": 29, "sleep_hours": 6.5, "stress_score": 5},
        {"cycle_length": 28, "sleep_hours": 7.0, "stress_score": 4},
        ...
      ],
      "age": 28,
      "bmi": 24.5,
      "pcos_diagnosed": true,
      "last_period_start": "2026-06-01"   // optional
    }
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, description="Request body must be JSON.")

    # ── Parse inputs ──────────────────────────────────────────────────────────
    history     = data.get("cycle_history", [{"cycle_length": 28}])
    age         = float(data.get("age", 28))
    bmi         = float(data.get("bmi", 22))
    pcos        = bool(data.get("pcos_diagnosed", False))
    last_period = data.get("last_period_start", None)

    # Average lifestyle across provided history
    sleep_hours  = float(np.mean([h.get("sleep_hours",  7.0) for h in history]))
    stress_score = float(np.mean([h.get("stress_score", 4.0) for h in history]))

    dyn = _parse_dynamic(list(history))          # (6, NUM_DYNAMIC)
    sta = np.array([age, bmi, float(pcos)])       # (NUM_STATIC,)

    try:
        result = predict(
            dynamic_sequence    = dyn,
            static_features_arr = sta,
            last_period_start   = last_period,
            sleep_hours         = sleep_hours,
            stress_score        = stress_score,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(result)


@app.route("/api/last", methods=["GET"])
def api_last():
    """Return the most recently saved prediction from output/prediction.json."""
    path = OUTPUT_DIR / "prediction.json"
    if not path.exists():
        return jsonify({"error": "No prediction has been generated yet. Call POST /api/predict first."}), 404
    return jsonify(json.loads(path.read_text()))


@app.route("/api/shap-plot", methods=["GET"])
def api_shap_plot():
    """Return the SHAP local impact bar chart as a PNG image."""
    path = FIGURE_DIR / "shap_local_impact.png"
    if not path.exists():
        abort(404, description="SHAP plot not found. Run a prediction first.")
    return send_file(str(path), mimetype="image/png")


@app.route("/api/benchmark", methods=["GET"])
def api_benchmark():
    """Return the 9-model benchmark comparison table."""
    return jsonify({
        "benchmark": BENCHMARK_RESULTS,
        "best_model": "Stacked Ensemble",
        "dataset": "FitrWoman / PCOS-enriched menstrual cycle dataset",
        "folds": 5,
        "tuning": "Optuna (100 trials per model)",
    })


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  OvulAI API Server — v3")
    print("  http://localhost:5050")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5050, debug=False)
