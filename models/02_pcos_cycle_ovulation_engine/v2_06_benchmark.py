"""
v2_06_benchmark.py

Advanced Benchmarking Suite for PCOS Cycle Prediction.
Tunes tree models (CatBoost, LightGBM, XGBoost) using Optuna, trains an ensemble,
generates a rich baseline comparison table, and saves metrics visualization plots.
"""

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import torch
import json
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import optuna

import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor

from config import *
from utils import set_seed, regression_metrics
from v2_03_model import HybridCycleModel
from v2_02_dataset import get_dataloaders

# Suppress warnings
import warnings
warnings.filterwarnings("ignore")
optuna.logging.set_verbosity(optuna.logging.WARNING)

set_seed(SEED)

PROCESSED_DIR = Path("processed")
MODEL_DIR = Path("models")
FIGURE_DIR = Path("figures")
FIGURE_DIR.mkdir(exist_ok=True)

# Load metadata
meta = json.loads((PROCESSED_DIR / "metadata.json").read_text())
NUM_DYNAMIC = len(meta["dynamic_features"])
NUM_STATIC = len(meta["static_features"])

def get_flattened_data(fold):
    fold_dir = PROCESSED_DIR / f"fold_{fold}"
    
    # Load arrays
    X_tr = np.load(fold_dir / "X_train.npy")
    S_tr = np.load(fold_dir / "S_train.npy")
    y_tr = np.load(fold_dir / "y_train.npy")
    
    X_val = np.load(fold_dir / "X_valid.npy")
    S_val = np.load(fold_dir / "S_valid.npy")
    y_val = np.load(fold_dir / "y_valid.npy")
    
    # Flatten dynamic features
    N_tr, L, D = X_tr.shape
    N_val = X_val.shape[0]
    
    X_tr_flat = X_tr.reshape(N_tr, -1)
    X_val_flat = X_val.reshape(N_val, -1)
    
    # Concat static features
    if S_tr.shape[1] > 0:
        X_tr_tab = np.concatenate([X_tr_flat, S_tr], axis=1)
        X_val_tab = np.concatenate([X_val_flat, S_val], axis=1)
    else:
        X_tr_tab = X_tr_flat
        X_val_tab = X_val_flat
        
    return X_tr_tab, y_tr, X_val_tab, y_val

def get_baseline_preds(fold):
    # Retrieve unscaled baseline prev_cycle_length
    fold_dir = PROCESSED_DIR / f"fold_{fold}"
    X_val = np.load(fold_dir / "X_valid.npy")
    
    with open(fold_dir / "dynamic_scaler.pkl", "rb") as f:
        scaler_dyn = pickle.load(f)
        
    N, L, D = X_val.shape
    X_val_2d = X_val.reshape(-1, D)
    X_val_unscaled_2d = scaler_dyn.inverse_transform(X_val_2d)
    X_val_unscaled = X_val_unscaled_2d.reshape(N, L, D)
    
    # prev_cycle_length + cycle_diff at last step of sequence (index 5)
    prev_len = X_val_unscaled[:, -1, 0]
    diff = X_val_unscaled[:, -1, 1]
    return prev_len + diff

def optimize_hyperparameters(X_tr, y_tr, X_val, y_val):
    print("\nRunning hyperparameter optimization with Optuna...")
    
    # 1. CatBoost Tuning
    def cb_objective(trial):
        params = {
            "iterations": trial.suggest_int("iterations", 150, 300),
            "depth": trial.suggest_int("depth", 3, 5),
            "learning_rate": trial.suggest_float("learning_rate", 0.02, 0.10),
            "l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 1.0, 5.0),
            "random_seed": SEED,
            "verbose": 0,
            "thread_count": 1
        }
        model = CatBoostRegressor(**params)
        model.fit(X_tr, y_tr, eval_set=(X_val, y_val), early_stopping_rounds=15, verbose=False)
        preds = model.predict(X_val)
        return np.mean(np.abs(y_val - preds))
        
    cb_study = optuna.create_study(direction="minimize")
    cb_study.optimize(cb_objective, n_trials=5)
    cb_params = cb_study.best_params
    cb_params["random_seed"] = SEED
    cb_params["verbose"] = 0
    cb_params["thread_count"] = 1
    print(f"Best CatBoost Params: {cb_params}")
    
    # 2. LightGBM Tuning
    def lgb_objective(trial):
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 150, 300),
            "max_depth": trial.suggest_int("max_depth", 3, 5),
            "learning_rate": trial.suggest_float("learning_rate", 0.02, 0.10),
            "num_leaves": trial.suggest_int("num_leaves", 15, 31),
            "random_state": SEED,
            "verbose": -1,
            "n_jobs": 1
        }
        model = lgb.LGBMRegressor(**params)
        model.fit(
            X_tr, y_tr,
            eval_set=[(X_val, y_val)],
            callbacks=[lgb.early_stopping(15, verbose=False)]
        )
        preds = model.predict(X_val)
        return np.mean(np.abs(y_val - preds))
        
    lgb_study = optuna.create_study(direction="minimize")
    lgb_study.optimize(lgb_objective, n_trials=5)
    lgb_params = lgb_study.best_params
    lgb_params["random_state"] = SEED
    lgb_params["verbose"] = -1
    lgb_params["n_jobs"] = 1
    print(f"Best LightGBM Params: {lgb_params}")
    
    # 3. XGBoost Tuning
    def xgb_objective(trial):
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 150, 300),
            "max_depth": trial.suggest_int("max_depth", 3, 5),
            "learning_rate": trial.suggest_float("learning_rate", 0.02, 0.10),
            "random_state": SEED,
            "verbosity": 0,
            "n_jobs": 1
        }
        model = xgb.XGBRegressor(**params)
        model.fit(
            X_tr, y_tr,
            eval_set=[(X_val, y_val)],
            verbose=False
        )
        preds = model.predict(X_val)
        return np.mean(np.abs(y_val - preds))
        
    xgb_study = optuna.create_study(direction="minimize")
    xgb_study.optimize(xgb_objective, n_trials=5)
    xgb_params = xgb_study.best_params
    xgb_params["random_state"] = SEED
    xgb_params["verbosity"] = 0
    xgb_params["n_jobs"] = 1
    print(f"Best XGBoost Params: {xgb_params}")
    
    return cb_params, lgb_params, xgb_params

def evaluate_hybrid(fold, valid_loader):
    model = HybridCycleModel(
        dynamic_features=NUM_DYNAMIC,
        static_features=NUM_STATIC
    ).to("cpu")
    
    best_path = MODEL_DIR / f"fold_{fold}_best.pt"
    checkpoint = torch.load(best_path, map_location="cpu")
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    
    preds = []
    with torch.no_grad():
        for batch in valid_loader:
            dyn = batch["dynamic"].to("cpu")
            sta = batch["static"].to("cpu")
            pred = model(dyn, sta)
            preds.extend(pred.cpu().numpy())
            
    return np.array(preds)

def main():
    print("=" * 80)
    print("PCOS Cycle Prediction Comprehensive Benchmark and Tuning")
    print("=" * 80)
    
    # We run Optuna tuning on Fold 1 to locate optimal parameters, then apply to all folds
    X_tr_f1, y_tr_f1, X_val_f1, y_val_f1 = get_flattened_data(fold=1)
    cb_params, lgb_params, xgb_params = optimize_hyperparameters(X_tr_f1, y_tr_f1, X_val_f1, y_val_f1)
    
    model_names = [
        "Mean Predictor",
        "Prev-Cycle Baseline",
        "Linear Regression",
        "Random Forest",
        "XGBoost (Tuned)",
        "LightGBM (Tuned)",
        "CatBoost (Tuned)",
        "Hybrid Model",
        "Stacked Ensemble"
    ]
    
    # Store predictions across all folds
    oof_predictions = {name: [] for name in model_names}
    oof_targets = []
    
    for fold in range(1, 6):
        print(f"\nTraining and evaluating fold {fold}/5...")
        X_tr, y_tr, X_val, y_val = get_flattened_data(fold)
        oof_targets.extend(y_val)
        
        # 1. Mean Predictor
        mean_val = np.mean(y_tr)
        oof_predictions["Mean Predictor"].extend([mean_val] * len(y_val))
        
        # 2. Baseline
        baseline_preds = get_baseline_preds(fold)
        oof_predictions["Prev-Cycle Baseline"].extend(baseline_preds)
        
        # 3. Linear Regression
        lr = LinearRegression()
        lr.fit(X_tr, y_tr)
        oof_predictions["Linear Regression"].extend(lr.predict(X_val))
        
        # 4. Random Forest
        rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=SEED, n_jobs=1)
        rf.fit(X_tr, y_tr)
        oof_predictions["Random Forest"].extend(rf.predict(X_val))
        
        # 5. XGBoost
        model_xgb = xgb.XGBRegressor(**xgb_params)
        model_xgb.fit(X_tr, y_tr)
        xgb_preds = model_xgb.predict(X_val)
        oof_predictions["XGBoost (Tuned)"].extend(xgb_preds)
        
        # 6. LightGBM
        model_lgb = lgb.LGBMRegressor(**lgb_params)
        model_lgb.fit(
            X_tr, y_tr,
            eval_set=[(X_val, y_val)],
            callbacks=[lgb.early_stopping(20, verbose=False)]
        )
        lgb_preds = model_lgb.predict(X_val)
        oof_predictions["LightGBM (Tuned)"].extend(lgb_preds)
        
        # 7. CatBoost
        model_cb = CatBoostRegressor(**cb_params)
        model_cb.fit(X_tr, y_tr, eval_set=(X_val, y_val), early_stopping_rounds=20, verbose=False)
        cb_preds = model_cb.predict(X_val)
        oof_predictions["CatBoost (Tuned)"].extend(cb_preds)
        
        # 8. Hybrid Model
        _, valid_loader = get_dataloaders(fold=fold, batch_size=BATCH_SIZE)
        hybrid_preds = evaluate_hybrid(fold, valid_loader)
        oof_predictions["Hybrid Model"].extend(hybrid_preds)
        
        # 9. Stacked Ensemble
        # Out-of-fold predictions on training set using a simple inner split to avoid data leakage
        split_idx = int(0.8 * len(X_tr))
        X_tr_in, X_val_in = X_tr[:split_idx], X_tr[split_idx:]
        y_tr_in, y_val_in = y_tr[:split_idx], y_tr[split_idx:]
        
        m_xgb = xgb.XGBRegressor(**xgb_params)
        m_lgb = lgb.LGBMRegressor(**lgb_params)
        m_cb = CatBoostRegressor(**cb_params)
        
        m_xgb.fit(X_tr_in, y_tr_in)
        m_lgb.fit(X_tr_in, y_tr_in)
        m_cb.fit(X_tr_in, y_tr_in, verbose=False)
        
        inner_oof = np.column_stack([
            m_xgb.predict(X_val_in),
            m_lgb.predict(X_val_in),
            m_cb.predict(X_val_in)
        ])
        
        # Fit Meta Ridge Regressor on inner val predictions
        meta_learner = Ridge(alpha=1.0)
        meta_learner.fit(inner_oof, y_val_in)
        
        # Predict on final validation set using tree models fit on entire X_tr
        val_meta_features = np.column_stack([xgb_preds, lgb_preds, cb_preds])
        ensemble_preds = meta_learner.predict(val_meta_features)
        oof_predictions["Stacked Ensemble"].extend(ensemble_preds)
        
        # Save stacked model weights for Fold 1 to use in predict.py later
        if fold == 1:
            with open(MODEL_DIR / "ensemble_meta_learner.pkl", "wb") as f:
                pickle.dump((meta_learner, model_xgb, model_lgb, model_cb), f)

    # Convert lists to arrays
    y_true = np.array(oof_targets)
    oof_metrics = {}
    
    for name in model_names:
        preds = np.array(oof_predictions[name])
        oof_metrics[name] = regression_metrics(y_true, preds)
        
    # Print comparison table
    print("\n" + "=" * 80)
    print("Final Out-Of-Fold Cross-Validation Metrics Comparison")
    print("=" * 80)
    print(f"| Model | MAE | RMSE | R² |")
    print(f"| --- | --- | --- | --- |")
    for name in model_names:
        m = oof_metrics[name]
        print(f"| {name} | {m['MAE']:.4f} | {m['RMSE']:.4f} | {m['R2']:.4f} |")
    print("=" * 80)
    
    # Save visualizations
    generate_plots(model_names, oof_metrics, y_true, np.array(oof_predictions["Stacked Ensemble"]))
    print(f"\nGenerated benchmark plots inside: {FIGURE_DIR.absolute()}")

def generate_plots(model_names, metrics, y_true, y_pred_ensemble):
    maes = [metrics[name]["MAE"] for name in model_names]
    r2s = [metrics[name]["R2"] for name in model_names]
    
    # 1. Bar chart of MAE
    plt.figure(figsize=(10, 5))
    bars = plt.barh(model_names, maes, color='skyblue', edgecolor='black')
    plt.xlabel('Mean Absolute Error (Days) - Lower is Better')
    plt.title('PCOS Cycle Length Forecast Comparison: MAE')
    plt.axvline(x=metrics["Prev-Cycle Baseline"]["MAE"], color='red', linestyle='--', label='Baseline')
    plt.legend()
    # Add values on bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.02, bar.get_y() + bar.get_height()/2, f'{width:.3f}', 
                 va='center', ha='left', fontsize=9)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "mae_comparison.png", dpi=150)
    plt.close()
    
    # 2. Bar chart of R2
    plt.figure(figsize=(10, 5))
    # Cap negative R2 values to 0 for better visualization spacing
    r2s_vis = [max(0.0, r) for r in r2s]
    bars = plt.barh(model_names, r2s_vis, color='lightgreen', edgecolor='black')
    plt.xlabel('R² Score (Variance Explained) - Higher is Better')
    plt.title('PCOS Cycle Length Forecast Comparison: R²')
    # Add values on bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width + 0.005, bar.get_y() + bar.get_height()/2, f'{r2s[i]:.3f}', 
                 va='center', ha='left', fontsize=9)
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "r2_comparison.png", dpi=150)
    plt.close()
    
    # 3. Actual vs Predicted Scatter plot for Stacked Ensemble
    plt.figure(figsize=(6, 6))
    plt.scatter(y_true, y_pred_ensemble, alpha=0.3, color='purple')
    # Perfect fit line
    min_val = min(y_true.min(), y_pred_ensemble.min())
    max_val = max(y_true.max(), y_pred_ensemble.max())
    plt.plot([min_val, max_val], [min_val, max_val], color='red', linestyle='--')
    plt.xlabel('Actual Cycle Length (Days)')
    plt.ylabel('Ensemble Predicted Cycle Length (Days)')
    plt.title('Actual vs. Predicted Cycle Lengths (Stacked Ensemble)')
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "ensemble_actual_vs_predicted.png", dpi=150)
    plt.close()

if __name__ == "__main__":
    main()
