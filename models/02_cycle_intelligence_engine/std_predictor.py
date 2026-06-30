import os
import pickle
import numpy as np
from typing import List, Dict, Any

# Load model and features once at startup
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'cycle_length_model.pkl')
FEATURES_PATH = os.path.join(MODEL_DIR, 'feature_columns.pkl')

import joblib

try:
    model = joblib.load(MODEL_PATH)
    feature_columns = joblib.load(FEATURES_PATH)
except Exception as e:
    print(f"Warning: Could not load cycle length model: {e}")
    model = None
    feature_columns = None

def engineer_features(
    age: int,
    height: float,
    weight: float,
    bmi: float,
    previous_cycle_lengths: List[int]
) -> np.ndarray:
    """Engineers the features required by the Linear Regression model."""
    
    cycle_number = len(previous_cycle_lengths) + 1
    
    if len(previous_cycle_lengths) >= 1:
        prev_cycle = previous_cycle_lengths[-1]
    else:
        prev_cycle = 28 # Default fallback
        
    if len(previous_cycle_lengths) >= 2:
        prev2_cycle = previous_cycle_lengths[-2]
    else:
        prev2_cycle = prev_cycle
        
    if len(previous_cycle_lengths) >= 3:
        last_3 = previous_cycle_lengths[-3:]
        rolling_mean_3 = np.mean(last_3)
        rolling_std_3 = np.std(last_3)
    else:
        rolling_mean_3 = np.mean(previous_cycle_lengths) if previous_cycle_lengths else 28.0
        rolling_std_3 = np.std(previous_cycle_lengths) if len(previous_cycle_lengths) > 1 else 0.0

    # The order must match feature_columns: 
    # ['Age', 'Height', 'Weight', 'BMI', 'CycleNumber', 'Prev_Cycle_Length', 'Prev2_Cycle_Length', 'Rolling_Mean_3', 'Rolling_STD_3']
    features_dict = {
        'Age': age,
        'Height': height,
        'Weight': weight,
        'BMI': bmi,
        'CycleNumber': cycle_number,
        'Prev_Cycle_Length': prev_cycle,
        'Prev2_Cycle_Length': prev2_cycle,
        'Rolling_Mean_3': rolling_mean_3,
        'Rolling_STD_3': rolling_std_3
    }
    
    # Ensure exact order as expected by model
    features_array = np.array([features_dict[col] for col in feature_columns]).reshape(1, -1)
    return features_array

def predict_cycle_length(
    age: int,
    height: float,
    weight: float,
    bmi: float,
    previous_cycle_lengths: List[int]
) -> int:
    """Predicts the next cycle length using the trained ML model."""
    
    # Fallback to simple average if model isn't loaded
    if model is None or feature_columns is None:
        if previous_cycle_lengths:
            return int(round(np.mean(previous_cycle_lengths)))
        return 28
        
    features = engineer_features(age, height, weight, bmi, previous_cycle_lengths)
    
    # Model returns an array of predictions, take the first one
    prediction = model.predict(features)[0]
    
    # Bound the prediction between reasonable limits (e.g., 21 to 45)
    from std_config import MIN_CYCLE_LENGTH, MAX_CYCLE_LENGTH
    bounded_prediction = max(MIN_CYCLE_LENGTH, min(MAX_CYCLE_LENGTH, int(round(prediction))))
    
    return bounded_prediction
