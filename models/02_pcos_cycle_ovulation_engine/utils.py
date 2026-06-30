
"""
utils.py
Shared utilities for PCOS Cycle Prediction V2
"""

import random
import numpy as np
import torch
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def save_checkpoint(model, optimizer, epoch, path):
    torch.save(
        {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
        },
        path,
    )


def load_checkpoint(model, optimizer, path, device="cpu"):
    ckpt = torch.load(path, map_location=device)
    model.load_state_dict(ckpt["model_state_dict"])
    if optimizer is not None:
        optimizer.load_state_dict(ckpt["optimizer_state_dict"])
    return ckpt["epoch"]


def regression_metrics(y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": rmse,
        "R2": r2_score(y_true, y_pred),
    }


def rolling_cv(series):
    m = np.mean(series)
    return 0.0 if abs(m) < 1e-8 else np.std(series) / m


def ema(values, alpha=0.3):
    out = []
    e = values[0]
    for v in values:
        e = alpha * v + (1 - alpha) * e
        out.append(e)
    return np.asarray(out)


def print_metrics(metrics: dict):
    print("-" * 40)
    for k, v in metrics.items():
        print(f"{k:5}: {v:.4f}")
    print("-" * 40)
