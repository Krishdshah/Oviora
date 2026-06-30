"""
v2_05_predict.py  —  OvulAI Core Engine v3
===========================================
Stacked Ensemble inference with:
  - Risk stratification
  - Clinical recommendations engine
  - SHAP narrative explanation
  - Data-driven confidence scoring
  - JSON output for dashboard API
"""

import os
import warnings
warnings.filterwarnings("ignore")
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import json
import pickle
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timedelta

PROCESSED_DIR = Path("processed")
MODEL_DIR     = Path("models")
FIGURE_DIR    = Path("figures")
OUTPUT_DIR    = Path("output")
FIGURE_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# ── Metadata ──────────────────────────────────────────────────────────────────
meta             = json.loads((PROCESSED_DIR / "metadata.json").read_text())
DYNAMIC_FEATURES = meta["dynamic_features"]
STATIC_FEATURES  = meta["static_features"]
NUM_DYNAMIC      = len(DYNAMIC_FEATURES)
NUM_STATIC       = len(STATIC_FEATURES)

# ── Scalers (safe — no OpenMP libs) ──────────────────────────────────────────
with open(PROCESSED_DIR / "fold_1" / "dynamic_scaler.pkl", "rb") as f:
    dynamic_scaler = pickle.load(f)
with open(PROCESSED_DIR / "fold_1" / "static_scaler.pkl", "rb") as f:
    static_scaler = pickle.load(f)

# ── Lazy ensemble cache ───────────────────────────────────────────────────────
_ensemble_cache: dict = {}

def _get_ensemble():
    if not _ensemble_cache:
        with open(MODEL_DIR / "ensemble_meta_learner.pkl", "rb") as f:
            meta_learner, model_xgb, model_lgb, model_cb = pickle.load(f)
        _ensemble_cache.update(
            meta=meta_learner, xgb=model_xgb, lgb=model_lgb, cb=model_cb
        )
    return (
        _ensemble_cache["meta"], _ensemble_cache["xgb"],
        _ensemble_cache["lgb"], _ensemble_cache["cb"],
    )


# ─────────────────────────────────────────────────────────────────────────────
# RISK STRATIFICATION
# ─────────────────────────────────────────────────────────────────────────────
def compute_risk(cycle_length: float, confidence: float, model_std: float) -> dict:
    """
    Rule-based risk stratification.
    Returns risk_level, risk_score (0–1), risk_color, risk_description.
    """
    if model_std > 2.0 or confidence < 0.35:
        level, score, color = "Highly Irregular", 0.9, "#EF4444"
        desc = "High model uncertainty — prediction should be used with caution."
    elif cycle_length < 21 or cycle_length > 38:
        level, score, color = "Irregular", 0.75, "#F97316"
        desc = "Cycle length is outside the typical 21–38 day range."
    elif (21 <= cycle_length < 24) or (35 < cycle_length <= 38) or confidence < 0.55:
        level, score, color = "Slightly Irregular", 0.45, "#EAB308"
        desc = "Mild irregularity detected. Monitor over the next 2 cycles."
    else:
        level, score, color = "Regular", 0.15, "#22C55E"
        desc = "Cycle pattern appears stable and within normal range."

    return {
        "risk_level": level,
        "risk_score": round(score, 2),
        "risk_color": color,
        "risk_description": desc,
    }


# ─────────────────────────────────────────────────────────────────────────────
# CLINICAL RECOMMENDATIONS
# ─────────────────────────────────────────────────────────────────────────────
def generate_recommendations(
    cycle_length: float,
    risk_level: str,
    pcos: bool,
    rolling_std: float,
    sleep_hours: float,
    stress_score: float,
    confidence: float,
) -> list:
    """
    Rule-based clinical recommendation engine.
    Returns a list of {category, message, priority, icon} dicts.
    """
    recs = []

    # ── Tracking ──────────────────────────────────────────────────────────────
    ovulation_day = max(10, round(cycle_length - 14))
    track_start   = max(ovulation_day - 4, 8)
    recs.append({
        "category": "Cycle Tracking",
        "message":  f"Track LH surge starting Day {track_start} using an OPK kit.",
        "priority": "high",
        "icon":     "📅",
    })

    # ── PCOS-specific ─────────────────────────────────────────────────────────
    if pcos:
        recs.append({
            "category": "PCOS Management",
            "message":  "Maintain a low-GI diet and regular light exercise to support hormonal balance.",
            "priority": "high",
            "icon":     "🩺",
        })
        if rolling_std > 3.0:
            recs.append({
                "category": "PCOS Monitoring",
                "message":  "Cycle variability is elevated — consider tracking basal body temperature (BBT) daily.",
                "priority": "high",
                "icon":     "🌡️",
            })

    # ── Irregular cycles ──────────────────────────────────────────────────────
    if risk_level in ("Irregular", "Highly Irregular"):
        recs.append({
            "category": "Medical Follow-up",
            "message":  "Irregular cycles detected. Consult a gynaecologist if pattern persists beyond 3 cycles.",
            "priority": "high",
            "icon":     "🏥",
        })
        recs.append({
            "category": "Monitoring",
            "message":  "Log any spotting or mid-cycle bleeding — it may indicate anovulation.",
            "priority": "medium",
            "icon":     "📝",
        })

    # ── Sleep ─────────────────────────────────────────────────────────────────
    if sleep_hours < 7.0:
        recs.append({
            "category": "Sleep",
            "message":  f"You averaged {sleep_hours:.1f}h of sleep. Aim for 7–8 hours — poor sleep disrupts LH and FSH secretion.",
            "priority": "medium",
            "icon":     "🌙",
        })

    # ── Stress ────────────────────────────────────────────────────────────────
    if stress_score > 6.0:
        recs.append({
            "category": "Stress Management",
            "message":  "High stress can suppress ovulation. Try 10 min of mindfulness or light yoga daily.",
            "priority": "medium",
            "icon":     "🧘",
        })

    # ── Confidence ────────────────────────────────────────────────────────────
    if confidence < 0.65:
        recs.append({
            "category": "Data Quality",
            "message":  "Logging more complete cycle data over the next 2–3 cycles will significantly improve prediction accuracy.",
            "priority": "low",
            "icon":     "📊",
        })

    # Always include hydration as a low-priority lifestyle tip
    recs.append({
        "category": "Lifestyle",
        "message":  "Stay hydrated (2–3 L/day). Dehydration can worsen PMS symptoms and cycle irregularity.",
        "priority": "low",
        "icon":     "💧",
    })

    # Sort by priority: high → medium → low
    order = {"high": 0, "medium": 1, "low": 2}
    recs.sort(key=lambda r: order[r["priority"]])
    return recs[:5]  # cap at 5 for dashboard


# ─────────────────────────────────────────────────────────────────────────────
# NARRATIVE EXPLANATION ("Why this prediction?")
# ─────────────────────────────────────────────────────────────────────────────

# Human-readable mappings for feature name fragments
_FEATURE_LABELS = {
    "pcos_diagnosed":   "PCOS diagnosis",
    "rolling_mean":     "historical cycle average",
    "rolling_std":      "cycle variability",
    "rolling_max":      "longest recent cycle",
    "rolling_min":      "shortest recent cycle",
    "rolling_median":   "median cycle length",
    "rolling_range":    "cycle length range",
    "rolling_skew":     "cycle length skew",
    "lag1":             "previous cycle length",
    "lag2":             "2-cycle-ago length",
    "lag3":             "3-cycle-ago length",
    "diff1":            "recent cycle-to-cycle change",
    "cycle_trend":      "long-term cycle trend",
    "sleep_hours":      "sleep duration",
    "stress_score":     "stress level",
    "bmi":              "BMI",
    "age":              "age",
}

def _readable_feature(raw_name: str) -> str:
    raw = raw_name.split("[")[0].strip()
    for key, label in _FEATURE_LABELS.items():
        if key in raw:
            return label
    return raw.replace("_", " ")

def build_narrative(top_indices, shap_values, feature_names, pcos: bool) -> str:
    sentences = []
    for rank, idx in enumerate(top_indices[:3]):
        val  = shap_values[idx]
        name = _readable_feature(feature_names[idx])
        direction = "increasing" if val >= 0 else "decreasing"
        impact = abs(val)

        if rank == 0:
            sentences.append(
                f"The strongest signal is your **{name}**, "
                f"{direction} the predicted cycle length by ~{impact:.1f} days."
            )
        elif rank == 1:
            sentences.append(
                f"Your **{name}** is also influential, "
                f"nudging the estimate {direction} by ~{impact:.1f} days."
            )
        else:
            sentences.append(
                f"Additionally, your **{name}** contributes a smaller "
                f"{'upward' if val >= 0 else 'downward'} adjustment of ~{impact:.1f} days."
            )

    if pcos:
        sentences.append(
            "PCOS typically introduces higher cycle variability, which is reflected in the model's confidence interval."
        )
    return " ".join(sentences)


# ─────────────────────────────────────────────────────────────────────────────
# CYCLE METRICS
# ─────────────────────────────────────────────────────────────────────────────
def calculate_cycle_metrics(cycle_length: float, last_period_start: str = None) -> dict:
    ovulation_day  = max(10, round(cycle_length - 14))
    fertile_start  = max(1, ovulation_day - 5)
    fertile_end    = ovulation_day + 1

    metrics = {
        "ovulation_day_of_cycle": ovulation_day,
        "fertile_window_days":    f"Days {fertile_start} to {fertile_end}",
    }

    if last_period_start:
        try:
            start            = datetime.strptime(last_period_start, "%Y-%m-%d")
            next_period      = start + timedelta(days=round(cycle_length))
            ovulation_date   = start + timedelta(days=ovulation_day)
            fertile_s        = start + timedelta(days=fertile_start)
            fertile_e        = start + timedelta(days=fertile_end)
            today            = datetime.now()
            days_until_ovul  = (ovulation_date - today).days
            days_until_next  = (next_period - today).days

            metrics.update({
                "last_period_start_date":     last_period_start,
                "estimated_next_period_date": next_period.strftime("%Y-%m-%d"),
                "estimated_ovulation_date":   ovulation_date.strftime("%Y-%m-%d"),
                "fertile_window_dates": (
                    f"{fertile_s.strftime('%Y-%m-%d')} to "
                    f"{fertile_e.strftime('%Y-%m-%d')}"
                ),
                "days_until_ovulation": days_until_ovul,
                "days_until_next_period": days_until_next,
                "cycle_day_today": (today - start).days + 1,
            })
        except ValueError:
            metrics["error"] = "Invalid date format. Use YYYY-MM-DD."
    return metrics


# ─────────────────────────────────────────────────────────────────────────────
# MAIN PREDICT FUNCTION
# ─────────────────────────────────────────────────────────────────────────────
def predict(
    dynamic_sequence,
    static_features_arr,
    last_period_start: str = None,
    sleep_hours: float = 7.0,
    stress_score: float = 4.0,
) -> dict:
    """
    OvulAI full inference pipeline.

    Parameters
    ----------
    dynamic_sequence    : array-like (6, NUM_DYNAMIC)
    static_features_arr : array-like (NUM_STATIC,)  — [age, bmi, pcos_diagnosed]
    last_period_start   : str YYYY-MM-DD  (optional)
    sleep_hours         : float  (average over recent cycles)
    stress_score        : float  0–10
    """
    import shap

    dyn = np.asarray(dynamic_sequence, dtype=np.float32)
    sta = np.asarray(static_features_arr, dtype=np.float32)

    if dyn.shape != (6, NUM_DYNAMIC):
        raise ValueError(f"Expected dynamic shape (6,{NUM_DYNAMIC}), got {dyn.shape}")
    if sta.shape != (NUM_STATIC,):
        raise ValueError(f"Expected static shape ({NUM_STATIC},), got {sta.shape}")

    # ── Scale ────────────────────────────────────────────────────────────────
    dyn_scaled = dynamic_scaler.transform(dyn)
    sta_scaled = static_scaler.transform(sta.reshape(1, -1)) if NUM_STATIC > 0 else np.zeros((1, 0))
    tab        = np.concatenate([dyn_scaled.reshape(-1), sta_scaled.reshape(-1)]).reshape(1, -1)

    # ── Ensemble inference ───────────────────────────────────────────────────
    meta_learner, model_xgb, model_lgb, model_cb = _get_ensemble()
    xgb_pred = float(model_xgb.predict(tab)[0])
    lgb_pred = float(model_lgb.predict(tab)[0])
    cb_pred  = float(model_cb.predict(tab)[0])
    ens_pred = float(meta_learner.predict(np.array([[xgb_pred, lgb_pred, cb_pred]]))[0])

    # ── SHAP ─────────────────────────────────────────────────────────────────
    explainer   = shap.TreeExplainer(model_cb)
    shap_values = explainer(tab).values[0]

    feature_names = []
    for t in range(6):
        for f in DYNAMIC_FEATURES:
            feature_names.append(f"{f} [t-{5 - t}]")
    for s in STATIC_FEATURES:
        feature_names.append(s)

    top_idx      = np.argsort(np.abs(shap_values))[::-1][:6]
    top_features = []
    for idx in top_idx:
        val = shap_values[idx]
        top_features.append({
            "feature":    feature_names[idx],
            "label":      _readable_feature(feature_names[idx]),
            "shap_value": round(float(val), 3),
            "direction":  "positive" if val >= 0 else "negative",
        })

    # ── Save SHAP bar chart ───────────────────────────────────────────────────
    contrib = shap_values[top_idx[:4]]
    names   = [_readable_feature(feature_names[i]) for i in top_idx[:4]]
    colors  = ["#C084FC" if c >= 0 else "#818CF8" for c in contrib]
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.barh(names[::-1], contrib[::-1], color=colors[::-1], edgecolor="none")
    ax.axvline(x=0, color="white", linewidth=0.8, alpha=0.5)
    ax.set_facecolor("#0F0A1E")
    fig.patch.set_facecolor("#0F0A1E")
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.title.set_color("white")
    ax.set_xlabel("SHAP Impact (Days)")
    ax.set_title("OvulAI — Feature Contribution (CatBoost SHAP)")
    for spine in ax.spines.values():
        spine.set_edgecolor("#2D1B69")
    fig.tight_layout()
    shap_path = FIGURE_DIR / "shap_local_impact.png"
    fig.savefig(shap_path, dpi=150)
    plt.close(fig)

    # ── Confidence ───────────────────────────────────────────────────────────
    model_std          = float(np.std([xgb_pred, lgb_pred, cb_pred]))
    model_agreement    = float(np.exp(-model_std * 0.15))
    rolling_std_val    = float(dyn[-1, DYNAMIC_FEATURES.index("rolling_std")])
    history_factor     = float(np.exp(-rolling_std_val * 0.08))
    deviation          = abs(ens_pred - 28.0)
    uncertainty_factor = float(np.exp(-deviation * 0.02))
    confidence         = round(0.95 * model_agreement * history_factor * uncertainty_factor, 2)

    # ── Risk stratification ──────────────────────────────────────────────────
    pcos   = bool(sta[2])
    risk   = compute_risk(ens_pred, confidence, model_std)

    # ── Recommendations ──────────────────────────────────────────────────────
    recs   = generate_recommendations(
        cycle_length  = ens_pred,
        risk_level    = risk["risk_level"],
        pcos          = pcos,
        rolling_std   = rolling_std_val,
        sleep_hours   = sleep_hours,
        stress_score  = stress_score,
        confidence    = confidence,
    )

    # ── Narrative ────────────────────────────────────────────────────────────
    narrative = build_narrative(top_idx, shap_values, feature_names, pcos)

    # ── Cycle calendar ───────────────────────────────────────────────────────
    calendar  = calculate_cycle_metrics(ens_pred, last_period_start)

    # ── Assemble full payload ────────────────────────────────────────────────
    output = {
        # Core prediction
        "predicted_cycle_length":      round(ens_pred, 2),
        "prediction_confidence_score": confidence,
        "confidence_percent":          int(confidence * 100),

        # Risk
        **risk,

        # Calendar
        **calendar,

        # Profile
        "cycle_regularity":    "Regular" if 21 <= ens_pred <= 35 else "Irregular",
        "pcos_profile_status": "PCOS Confirmed" if pcos else "PCOS Negative",

        # Intelligence layers
        "why_this_prediction":      narrative,
        "top_contributing_features": top_features,
        "recommendations":           recs,

        # Model transparency
        "model_predictions_breakdown": {
            "XGBoost":          round(xgb_pred, 2),
            "LightGBM":         round(lgb_pred, 2),
            "CatBoost":         round(cb_pred, 2),
            "Stacked_Ensemble": round(ens_pred, 2),
        },
        "model_agreement_std": round(model_std, 3),

        # Assets
        "shap_plot": str(shap_path),

        # Meta
        "generated_at": datetime.now().isoformat(),
        "engine":       "OvulAI v3 — Stacked Ensemble (XGB + LGBM + CatBoost + Ridge Meta)",
    }

    # ── Write to output/prediction.json ──────────────────────────────────────
    out_path = OUTPUT_DIR / "prediction.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))

    return output


# ─────────────────────────────────────────────────────────────────────────────
# CLI DEMO
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    SEP = "=" * 72
    print(SEP)
    print("  OvulAI — Cycle & Ovulation Intelligence Engine")
    print("  Powered by Stacked Ensemble + SHAP Explainability")
    print(SEP)

    # Demo patient
    demo_dynamic = np.zeros((6, NUM_DYNAMIC), dtype=np.float32)
    history_lengths = [29.0, 28.0, 30.0, 27.0, 28.0, 29.0]
    for i, length in enumerate(history_lengths):
        demo_dynamic[i, DYNAMIC_FEATURES.index("prev_cycle_length")]  = length
        demo_dynamic[i, DYNAMIC_FEATURES.index("rolling_mean_3")]     = np.mean(history_lengths[max(0, i-2):i+1])
        demo_dynamic[i, DYNAMIC_FEATURES.index("rolling_std")]        = np.std(history_lengths[:i+1]) if i > 0 else 0.5
        demo_dynamic[i, DYNAMIC_FEATURES.index("sleep_hours_cycle")]  = 6.5
        demo_dynamic[i, DYNAMIC_FEATURES.index("stress_score_cycle")] = 6.8

    demo_static = np.array([28.0, 24.5, 1.0])

    result = predict(
        demo_dynamic,
        demo_static,
        last_period_start="2026-06-01",
        sleep_hours=6.5,
        stress_score=6.8,
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(SEP)
    print(f"  ✓ Saved to: {OUTPUT_DIR / 'prediction.json'}")
    print(f"  ✓ SHAP plot: {result['shap_plot']}")
    print(SEP)
