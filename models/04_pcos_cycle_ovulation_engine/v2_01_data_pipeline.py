
"""
v2_01_data_pipeline.py

Production data pipeline for PCOS Cycle Prediction V2.
"""

from pathlib import Path
import json
import pickle
import numpy as np
import pandas as pd

from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

from config import (
    PERIOD_PATH,
    PROFILE_PATH,
    PROCESSED_DIR,
    STATIC_FEATURES,
    DYNAMIC_FEATURES,
    TARGET,
    SEQ_LEN,
    SEED,
)
from utils import set_seed

set_seed(SEED)

PERIOD = pd.read_csv(PERIOD_PATH)
PROFILE = pd.read_csv(PROFILE_PATH)

df = (
    PERIOD.merge(PROFILE, on="user_id", how="left")
          .sort_values(["user_id", "cycle_number"])
          .reset_index(drop=True)
)

# ---------- Feature Engineering ----------

g = df.groupby("user_id")

df["cycle_diff"] = df["cycle_length_days"] - df["prev_cycle_length"]

# Lags
for i in range(1, 7):
    df[f"lag{i}"] = g["cycle_length_days"].shift(i)

# Differences
df["diff1"] = df["lag1"] - df["lag2"]
df["diff2"] = df["lag2"] - df["lag3"]
df["diff3"] = df["lag3"] - df["lag4"]

# Rolling window=3, 5, 10
for w in (3, 5):
    df[f"rolling_mean_{w}"] = g["cycle_length_days"].transform(
        lambda x: x.shift().rolling(w, min_periods=1).mean()
    )

df["rolling_mean_10"] = g["cycle_length_days"].transform(
    lambda x: x.shift().rolling(10, min_periods=1).mean()
)

df["rolling_std"] = g["cycle_length_days"].transform(
    lambda x: x.shift().rolling(5, min_periods=1).std()
)

df["rolling_std_10"] = g["cycle_length_days"].transform(
    lambda x: x.shift().rolling(10, min_periods=1).std()
)

df["rolling_min"] = g["cycle_length_days"].transform(
    lambda x: x.shift().rolling(5, min_periods=1).min()
)

df["rolling_min_10"] = g["cycle_length_days"].transform(
    lambda x: x.shift().rolling(10, min_periods=1).min()
)

df["rolling_max"] = g["cycle_length_days"].transform(
    lambda x: x.shift().rolling(5, min_periods=1).max()
)

df["rolling_max_10"] = g["cycle_length_days"].transform(
    lambda x: x.shift().rolling(10, min_periods=1).max()
)

df["rolling_median"] = g["cycle_length_days"].transform(
    lambda x: x.shift().rolling(5, min_periods=1).median()
)

df["rolling_median_10"] = g["cycle_length_days"].transform(
    lambda x: x.shift().rolling(10, min_periods=1).median()
)

df["rolling_range"] = df["rolling_max_10"] - df["rolling_min_10"]

# IQR
rolling_q75 = g["cycle_length_days"].transform(
    lambda x: x.shift().rolling(5, min_periods=1).quantile(0.75)
)
rolling_q25 = g["cycle_length_days"].transform(
    lambda x: x.shift().rolling(5, min_periods=1).quantile(0.25)
)
df["rolling_iqr"] = rolling_q75 - rolling_q25

# Skew, Kurtosis, and MAD
df["rolling_skew"] = g["cycle_length_days"].transform(
    lambda x: x.shift().rolling(5, min_periods=3).skew()
)
df["rolling_kurt"] = g["cycle_length_days"].transform(
    lambda x: x.shift().rolling(5, min_periods=4).kurt()
)
df["cycle_mad"] = g["cycle_length_days"].transform(
    lambda x: x.shift().rolling(5, min_periods=1).apply(
        lambda r: np.mean(np.abs(r - np.mean(r))) if len(r) > 0 else 0.0, raw=True
    )
)

df["cycle_trend"] = g["cycle_length_days"].diff()
df["cycle_acceleration"] = df["cycle_trend"].diff()

df["ema_cycle"] = g["cycle_length_days"].transform(
    lambda x: x.shift().ewm(alpha=0.3).mean()
)

# Linear trend slope, intercept, r2 over last 6 cycles
def fit_trend(series):
    y = series
    n = len(y)
    if n < 3:
        return np.array([0.0, 0.0, 0.0])
    x = np.arange(n)
    slope, intercept = np.polyfit(x, y, 1)
    y_pred = slope * x + intercept
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    if ss_tot < 1e-8:
        r2 = 1.0
    else:
        ss_res = np.sum((y - y_pred) ** 2)
        r2 = 1.0 - (ss_res / ss_tot)
    return np.array([slope, intercept, r2])

df["slope"] = g["cycle_length_days"].transform(
    lambda x: x.shift().rolling(6, min_periods=1).apply(lambda r: fit_trend(r)[0], raw=True)
)
df["intercept"] = g["cycle_length_days"].transform(
    lambda x: x.shift().rolling(6, min_periods=1).apply(lambda r: fit_trend(r)[1], raw=True)
)
df["r2_trend"] = g["cycle_length_days"].transform(
    lambda x: x.shift().rolling(6, min_periods=1).apply(lambda r: fit_trend(r)[2], raw=True)
)

if {"estrogen_pgml", "progesterone_ngml"}.issubset(df.columns):
    df["hormone_ratio"] = (
        df["estrogen_pgml"] / (df["progesterone_ngml"] + 1e-3)
    )
    df["delta_estrogen"] = g["estrogen_pgml"].diff()
    df["delta_progesterone"] = g["progesterone_ngml"].diff()
else:
    for c in ["hormone_ratio", "delta_estrogen", "delta_progesterone"]:
        df[c] = 0

for col, out in [
    ("stress_score_cycle", "stress_trend"),
    ("sleep_hours_cycle", "sleep_trend"),
    ("pain_level", "pain_trend"),
    ("mood_score", "mood_trend"),
]:
    if col in df.columns:
        df[out] = g[col].diff()
    else:
        df[out] = 0

if {"energy_level", "stress_score_cycle", "sleep_hours_cycle"}.issubset(df.columns):
    df["health_index"] = (
        df["energy_level"]
        - df["stress_score_cycle"]
        + df["sleep_hours_cycle"]
    )
else:
    df["health_index"] = 0

mx = g["cycle_number"].transform("max")
df["relative_cycle"] = df["cycle_number"] / mx

df = df.replace([np.inf, -np.inf], np.nan).fillna(0)

dynamic = [c for c in DYNAMIC_FEATURES if c in df.columns]
static = [c for c in STATIC_FEATURES if c in df.columns]

print("Dynamic:", len(dynamic))
print("Static :", len(static))

gkf = GroupKFold(n_splits=5)

for fold, (tr_idx, va_idx) in enumerate(
    gkf.split(df, groups=df["user_id"]), start=1
):
    train = df.iloc[tr_idx].copy()
    valid = df.iloc[va_idx].copy()

    scaler_dyn = StandardScaler()
    scaler_sta = StandardScaler()

    train[dynamic] = scaler_dyn.fit_transform(train[dynamic])
    valid[dynamic] = scaler_dyn.transform(valid[dynamic])

    if static:
        train[static] = scaler_sta.fit_transform(train[static])
        valid[static] = scaler_sta.transform(valid[static])

    def build_sequences(frame):
        xs, ss, ys = [], [], []

        for _, u in frame.groupby("user_id"):
            u = u.sort_values("cycle_number")
            if len(u) <= SEQ_LEN:
                continue

            dvals = u[dynamic].values
            svals = u[static].values if static else np.empty((len(u),0))
            target = u[TARGET].values

            for i in range(len(u)-SEQ_LEN):
                xs.append(dvals[i:i+SEQ_LEN])
                ss.append(svals[i+SEQ_LEN] if static else [])
                ys.append(target[i+SEQ_LEN])

        return (
            np.asarray(xs, np.float32),
            np.asarray(ss, np.float32),
            np.asarray(ys, np.float32),
        )

    Xtr, Str, ytr = build_sequences(train)
    Xva, Sva, yva = build_sequences(valid)

    fold_dir = PROCESSED_DIR / f"fold_{fold}"
    fold_dir.mkdir(exist_ok=True)

    np.save(fold_dir / "X_train.npy", Xtr)
    np.save(fold_dir / "S_train.npy", Str)
    np.save(fold_dir / "y_train.npy", ytr)

    np.save(fold_dir / "X_valid.npy", Xva)
    np.save(fold_dir / "S_valid.npy", Sva)
    np.save(fold_dir / "y_valid.npy", yva)

    with open(fold_dir / "dynamic_scaler.pkl", "wb") as f:
        pickle.dump(scaler_dyn, f)

    with open(fold_dir / "static_scaler.pkl", "wb") as f:
        pickle.dump(scaler_sta, f)

meta = {
    "sequence_length": SEQ_LEN,
    "dynamic_features": dynamic,
    "static_features": static,
    "target": TARGET,
}

with open(PROCESSED_DIR / "metadata.json", "w") as f:
    json.dump(meta, f, indent=2)

print("Pipeline complete.")
