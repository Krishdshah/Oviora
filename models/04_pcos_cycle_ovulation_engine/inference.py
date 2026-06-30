"""
Inference module for PCOS Cycle & Ovulation Intelligence Engine
"""

import json
import pickle
import numpy as np
from pathlib import Path

class PCOSInferenceEngine:
    def __init__(self, model_dir=None):
        if model_dir is None:
            model_dir = Path(__file__).parent / "models"
        
        self.model_dir = Path(model_dir)
        self.scalers = {}
        self.models = {}
        self.load_models()
    
    def load_models(self):
        """Load ensemble models and scalers"""
        meta_learner_path = self.model_dir / "ensemble_meta_learner.pkl"
        if meta_learner_path.exists():
            with open(meta_learner_path, 'rb') as f:
                self.meta_learner = pickle.load(f)
        
        fold_1_path = Path(__file__).parent / "processed" / "fold_1"
        for scaler_type in ['dynamic_scaler.pkl', 'static_scaler.pkl']:
            scaler_path = fold_1_path / scaler_type
            if scaler_path.exists():
                with open(scaler_path, 'rb') as f:
                    self.scalers[scaler_type.replace('.pkl', '')] = pickle.load(f)
    
    def predict(self, features):
        prediction = self.meta_learner.predict(features)
        return {
            "prediction": float(prediction[0]) if hasattr(prediction, '__len__') else float(prediction),
            "model": "ensemble_meta_learner_v2"
        }

if __name__ == "__main__":
    engine = PCOSInferenceEngine()
    print("PCOS Inference Engine loaded successfully")
