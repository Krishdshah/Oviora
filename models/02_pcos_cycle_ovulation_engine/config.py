
"""
config.py
Central configuration for PCOS Cycle Prediction V2
"""

from pathlib import Path
import torch

PROJECT_DIR = Path(".")
PROCESSED_DIR = PROJECT_DIR / "processed"
MODEL_DIR = PROJECT_DIR / "models"
LOG_DIR = PROJECT_DIR / "logs"
FIGURE_DIR = PROJECT_DIR / "figures"

for d in [PROCESSED_DIR, MODEL_DIR, LOG_DIR, FIGURE_DIR]:
    d.mkdir(exist_ok=True)

PERIOD_PATH = "/Users/lakshbaweja/Programming/Samsung innovate/model 4 /dataset/archive (3)/Period_Log.csv"
PROFILE_PATH = "/Users/lakshbaweja/Programming/Samsung innovate/model 4 /dataset/archive (3)/User_Profile.csv"

SEED = 42
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")

SEQ_LEN = 6
TARGET = "cycle_length_days"

STATIC_FEATURES = [
    "age",
    "bmi",
    "pcos_diagnosed",
]

DYNAMIC_FEATURES = [
    "prev_cycle_length",
    "cycle_diff",
    "rolling_mean_3",
    "rolling_mean_5",
    "rolling_mean_10",
    "rolling_std",
    "rolling_std_10",
    "rolling_min",
    "rolling_min_10",
    "rolling_max",
    "rolling_max_10",
    "rolling_median",
    "rolling_median_10",
    "rolling_range",
    "rolling_iqr",
    "rolling_skew",
    "rolling_kurt",
    "cycle_mad",
    "cycle_trend",
    "cycle_acceleration",
    "ema_cycle",
    "lag1",
    "lag2",
    "lag3",
    "lag4",
    "lag5",
    "lag6",
    "diff1",
    "diff2",
    "diff3",
    "slope",
    "intercept",
    "r2_trend",
    "pain_level",
    "mood_score",
    "stress_score_cycle",
    "sleep_hours_cycle",
    "energy_level",
    "estrogen_pgml",
    "progesterone_ngml",
    "hormone_ratio",
    "delta_estrogen",
    "delta_progesterone",
    "stress_trend",
    "sleep_trend",
    "pain_trend",
    "mood_trend",
    "health_index",
    "relative_cycle",
]

BATCH_SIZE = 128
EPOCHS = 50
LEARNING_RATE = 3e-4
WEIGHT_DECAY = 1e-3
DROPOUT = 0.30

# Model Architecture
STATIC_HIDDEN = 64
LSTM_HIDDEN = 64
LSTM_LAYERS = 2
TRANSFORMER_LAYERS = 2
NUM_HEADS = 4

# Training Parameters
USE_AMP = False
EARLY_STOPPING = 10

BEST_MODEL = MODEL_DIR / "best_model.pt"
LAST_MODEL = MODEL_DIR / "last_model.pt"
