import os
import pandas as pd
import numpy as np
import shap
from typing import Dict, List, Any
from nutrition_app.config import settings
from nutrition_app.data_pipeline.schemas import PatientProfile
from nutrition_app.recommendation.ranker import get_ranker_service, ALL_FEATURES, PATIENT_FEATS, FOOD_FEATS, encode_risk

class SHAPExplainerService:
    def __init__(self):
        self.explainer = None
        self.ranker_service = get_ranker_service()
        self.initialize_explainer()

    def initialize_explainer(self):
        # We need the model loaded to initialize TreeExplainer
        if self.ranker_service.model is not None:
            try:
                self.explainer = shap.TreeExplainer(self.ranker_service.model)
                print("SHAP TreeExplainer initialized successfully.")
            except Exception as e:
                print(f"Failed to initialize SHAP TreeExplainer: {e}")
        else:
            print("SHAP Explainer delayed: LGBM model not loaded yet.")

    def explain_recommendation(self, profile: PatientProfile, food_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Computes SHAP value explanations for a specific patient-food interaction.
        """
        # Re-initialize if model was loaded after initialization
        if self.explainer is None:
            self.initialize_explainer()
            
        if self.explainer is None:
            return {"error": "SHAP explainer not initialized (model missing)."}

        # 1. Prepare candidate feature vector
        p_dict = profile.model_dump()
        p_dict['ir_risk_code'] = encode_risk(p_dict['insulin_resistance_risk'])
        p_dict['hormone_sev_code'] = encode_risk(p_dict['hormonal_imbalance_severity'])
        p_dict['inflammation_risk_code'] = encode_risk(p_dict['inflammation_risk'])
        p_dict['cv_risk_code'] = encode_risk(p_dict['cardiovascular_risk'])
        
        # Merge Patient and Food features
        feat_dict = {}
        for f in PATIENT_FEATS:
            feat_dict[f] = p_dict.get(f, 0.0)
            
        # Extract food features mapping naming conventions in CSV
        # Map FoodItem schema field name to the raw CSV fields
        food_csv_mapper = {
            'Calories': food_dict.get('calories'),
            'Protein': food_dict.get('protein'),
            'Carbohydrates': food_dict.get('carbs'),
            'Fat': food_dict.get('fat'),
            'Fiber': food_dict.get('fiber'),
            'GlycemicIndex': food_dict.get('glycemic_index'),
            'pcos_friendliness_score': food_dict.get('pcos_friendliness_score')
        }
        
        # Load from actual food store if raw parameters are missing
        if os.path.exists(settings.FOOD_STORE_PATH):
            df_foods = pd.read_csv(settings.FOOD_STORE_PATH)
            match = df_foods[df_foods['FoodID'] == food_dict.get('food_id')]
            if not match.empty:
                full_food_dict = match.iloc[0].to_dict()
                for f in FOOD_FEATS:
                    feat_dict[f] = full_food_dict.get(f, 0.0)
            else:
                for f in FOOD_FEATS:
                    feat_dict[f] = food_csv_mapper.get(f, 0.0)
        else:
            for f in FOOD_FEATS:
                feat_dict[f] = food_csv_mapper.get(f, 0.0)
                
        # Build dataframe row
        df_row = pd.DataFrame([feat_dict])[ALL_FEATURES]
        
        # 2. Calculate SHAP values
        shap_values = self.explainer.shap_values(df_row)
        
        # For ranker, shap_values might be a list or single array.
        # Generally booster shap_values returns an array of shape (num_samples, num_features)
        if isinstance(shap_values, list):
            # For multi-class it's a list. For LambdaRank it's typically a single array.
            shap_array = shap_values[0][0]
        else:
            shap_array = shap_values[0] if len(shap_values.shape) > 1 else shap_values

        # 3. Pair and sort feature importances
        feature_shap = list(zip(ALL_FEATURES, shap_array))
        
        # Split into positive and negative drivers
        positive_drivers = [item for item in feature_shap if item[1] > 0]
        negative_drivers = [item for item in feature_shap if item[1] < 0]
        
        # Sort
        positive_drivers = sorted(positive_drivers, key=lambda x: x[1], reverse=True)
        negative_drivers = sorted(negative_drivers, key=lambda x: x[1]) # Most negative first
        
        # 4. Generate user-friendly explanations
        explanations = []
        for feat, val in positive_drivers[:3]:
            desc = self._get_feature_explanation_desc(feat, val, is_positive=True, profile=profile)
            explanations.append(desc)
            
        for feat, val in negative_drivers[:3]:
            desc = self._get_feature_explanation_desc(feat, val, is_positive=False, profile=profile)
            explanations.append(desc)
            
        return {
            "food_name": food_dict.get('food_name'),
            "base_value": float(self.explainer.expected_value) if hasattr(self.explainer, 'expected_value') else 0.0,
            "shap_score": float(np.sum(shap_array)),
            "top_features": [
                {"feature": feat, "shap_value": float(val), "interpretation": self._get_feature_explanation_desc(feat, val, val > 0, profile)}
                for feat, val in (positive_drivers[:3] + negative_drivers[:3])
            ],
            "narrative_explanation": " ".join(explanations)
        }

    def _get_feature_explanation_desc(self, feat: str, val: float, is_positive: bool, profile: PatientProfile) -> str:
        """
        Translates a technical SHAP feature value into clinician explanation.
        """
        # Map feature names to simple names
        names = {
            'Calories': 'Caloric density',
            'Protein': 'Protein content',
            'Carbohydrates': 'Carbohydrate content',
            'Fat': 'Healthy fats',
            'Fiber': 'Dietary fiber',
            'GlycemicIndex': 'Glycemic Index',
            'GlycemicLoad': 'Glycemic Load',
            'Sodium_mg': 'Sodium content',
            'Potassium_mg': 'Potassium content',
            'Magnesium_mg': 'Magnesium richness',
            'Calcium_mg': 'Calcium content',
            'VitaminD_mcg': 'Vitamin D richness',
            'Zinc_mg': 'Zinc levels',
            'Omega3_g': 'Omega-3 fatty acids',
            'SaturatedFat_g': 'Saturated fat content',
            'Sugars': 'Sugar levels',
            'pcos_friendliness_score': 'PCOS Friendliness Index',
            'InsulinResistanceSuitability': 'Insulin Resistance suitability',
            'HormonalHealthScore': 'Hormonal balancing properties',
            'AntiInflammatoryPotential': 'Anti-inflammatory properties',
            'WeightManagementScore': 'Weight management compatibility'
        }
        
        feat_name = names.get(feat, feat)
        sign_str = "+" if is_positive else ""
        
        if is_positive:
            if feat in ['Fiber', 'InsulinResistanceSuitability'] and profile.insulin_resistance_risk in ['High', 'Medium']:
                return f"{feat_name} ({sign_str}{val:.2f}) was recommended to help stabilize your insulin levels."
            elif feat in ['Omega3_g', 'AntiInflammatoryPotential'] and profile.inflammation_risk in ['High', 'Medium']:
                return f"{feat_name} ({sign_str}{val:.2f}) was boosted to help lower chronic systemic inflammation."
            elif feat in ['Zinc_mg', 'Magnesium_mg', 'HormonalHealthScore'] and profile.hormonal_imbalance_severity in ['High', 'Medium']:
                return f"{feat_name} ({sign_str}{val:.2f}) supports regulatory ovulation and hormone synthesis."
            elif feat in ['WeightManagementScore', 'Protein'] and "weight_loss" in [g.lower() for g in profile.goals]:
                return f"{feat_name} ({sign_str}{val:.2f}) was prioritized to support healthy weight management and satiety."
            else:
                return f"High {feat_name} ({sign_str}{val:.2f}) fits your nutritional requirement profiles."
        else:
            if feat in ['GlycemicIndex', 'GlycemicLoad', 'Sugars'] and profile.insulin_resistance_risk in ['High', 'Medium']:
                return f"High {feat_name} ({val:.2f}) was avoided because it triggers elevated blood glucose spikes."
            elif feat in ['Sodium_mg', 'SaturatedFat_g'] and (profile.cardiovascular_risk in ['High', 'Medium'] or profile.hypertension_status):
                return f"{feat_name} ({val:.2f}) was penalized to reduce cardiovascular and blood pressure risks."
            elif feat in ['Sugars', 'SaturatedFat_g'] and profile.inflammation_risk in ['High', 'Medium']:
                return f"Elevated {feat_name} ({val:.2f}) was reduced to avoid exacerbating inflammatory symptoms."
            else:
                return f"Higher {feat_name} ({val:.2f}) negatively impacts suitability for your metabolic profile."

# Singleton instance
shap_explainer = None

def get_shap_explainer() -> SHAPExplainerService:
    global shap_explainer
    if shap_explainer is None:
        shap_explainer = SHAPExplainerService()
    return shap_explainer
