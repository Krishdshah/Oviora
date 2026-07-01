import os
import pandas as pd
import numpy as np
import lightgbm as lgb
from typing import List, Dict, Any, Tuple
from nutrition_app.config import settings
from nutrition_app.data_pipeline.schemas import PatientProfile, FoodItem

# Feature Column Names
PATIENT_FEATS = [
    'age', 'weight_kg', 'height_cm', 'waist_inch', 'hip_inch',
    'exercise_hours_per_week', 'bmi', 'waist_to_hip_ratio',
    'ir_risk_code', 'hormone_sev_code', 'inflammation_risk_code', 'cv_risk_code'
]

FOOD_FEATS = [
    'Calories', 'Protein', 'Carbohydrates', 'Fat', 'Fiber', 
    'GlycemicIndex', 'GlycemicLoad', 'Sodium_mg', 'Potassium_mg', 
    'Magnesium_mg', 'Calcium_mg', 'VitaminD_mcg', 'Zinc_mg', 
    'Omega3_g', 'SaturatedFat_g', 'Sugars', 'pcos_friendliness_score',
    'InsulinResistanceSuitability', 'HormonalHealthScore',
    'AntiInflammatoryPotential', 'WeightManagementScore'
]

ALL_FEATURES = PATIENT_FEATS + FOOD_FEATS

def encode_risk(val: str) -> int:
    mapping = {"Low": 0, "Medium": 1, "High": 2}
    return mapping.get(val, 0)

def compute_suitability_score(patient: Dict[str, Any], food: Dict[str, Any]) -> float:
    """
    Calculate an expert rule-based suitability score (0.0 to 5.0) 
    representing clinician ranking decisions.
    """
    # 1. Check Allergies
    allergies = patient.get('allergies', [])
    if isinstance(allergies, str):
        import json
        try:
            allergies = json.loads(allergies.replace("'", '"'))
        except:
            allergies = []
    
    food_name_lower = str(food.get('FoodName', '')).lower()
    food_cat_lower = str(food.get('Category', '')).lower()
    
    for allergy in allergies:
        allergy_lower = allergy.lower().strip()
        if allergy_lower and (allergy_lower in food_name_lower or allergy_lower in food_cat_lower):
            return 0.0  # Strict allergy exclusion

    # 2. Check Dietary Preferences
    diet = str(patient.get('dietary_preference', 'veg')).lower()
    
    non_veg_keywords = ["chicken", "fish", "salmon", "tuna", "egg", "meat", "pork", "shrimp", "seafood", "poultry", "mutton", "beef"]
    is_non_veg = any(kw in food_name_lower or kw in food_cat_lower for kw in non_veg_keywords)
    
    dairy_keywords = ["milk", "cheese", "butter", "yogurt", "cream", "paneer"]
    is_dairy = any(kw in food_name_lower or kw in food_cat_lower for kw in dairy_keywords)
    
    if diet == "vegan" and (is_non_veg or is_dairy or "dairy" in food_cat_lower or "egg" in food_cat_lower):
        return 0.0  # Vegan exclusion
    elif diet == "veg" and is_non_veg:
        return 0.0  # Vegetarian exclusion

    # 3. Base Score on PCOS Friendliness Score
    pcos_friendliness = float(food.get('pcos_friendliness_score', 50.0))
    score = (pcos_friendliness / 100.0) * 3.5 + 0.5  # maps 0-100 to 0.5-4.0

    # 4. Clinical Condition Adjustments
    # Insulin Resistance
    ir_risk = patient.get('insulin_resistance_risk', 'Low')
    gi = float(food.get('GlycemicIndex', 50.0))
    fiber = float(food.get('Fiber', 1.0))
    protein = float(food.get('Protein', 2.0))
    
    if ir_risk == "High":
        score += -1.5 * (gi / 100.0) + 0.6 * (fiber / 5.0) + 0.3 * (protein / 10.0)
    elif ir_risk == "Medium":
        score += -0.7 * (gi / 100.0) + 0.3 * (fiber / 5.0) + 0.15 * (protein / 10.0)

    # Inflammation
    inf_risk = patient.get('inflammation_risk', 'Low')
    anti_inf_pot = float(food.get('AntiInflammatoryPotential', 50.0))
    sugars = float(food.get('Sugars', 0.0))
    
    if inf_risk == "High":
        score += 1.0 * (anti_inf_pot / 100.0) - 0.7 * (sugars / 10.0)
    elif inf_risk == "Medium":
        score += 0.5 * (anti_inf_pot / 100.0) - 0.35 * (sugars / 10.0)

    # Cardiovascular Risk / Hypertension
    cv_risk = patient.get('cardiovascular_risk', 'Low')
    sodium = float(food.get('Sodium_mg', 10.0))
    potassium = float(food.get('Potassium_mg', 100.0))
    sat_fat = float(food.get('SaturatedFat_g', 0.1))
    
    if cv_risk == "High" or patient.get('hypertension_status', False):
        score += -1.2 * (sodium / 300.0) + 0.6 * (potassium / 300.0) - 0.8 * (sat_fat / 5.0)
    elif cv_risk == "Medium":
        score += -0.6 * (sodium / 300.0) + 0.3 * (potassium / 300.0) - 0.4 * (sat_fat / 5.0)

    # Hormonal Imbalances
    hormone_sev = patient.get('hormonal_imbalance_severity', 'Low')
    hormonal_score = float(food.get('HormonalHealthScore', 50.0))
    if hormone_sev == "High":
        score += 1.2 * (hormonal_score / 100.0)
    elif hormone_sev == "Medium":
        score += 0.6 * (hormonal_score / 100.0)

    # Weight Management Goals
    goals = patient.get('goals', [])
    if isinstance(goals, str):
        import json
        try:
            goals = json.loads(goals.replace("'", '"'))
        except:
            goals = []
    
    goals_lower = [g.lower() for g in goals]
    if "weight_loss" in goals_lower or "weight loss" in goals_lower:
        weight_score = float(food.get('WeightManagementScore', 50.0))
        score += 1.0 * (weight_score / 100.0)

    # Clamp and round to integer
    score = np.clip(score, 0.0, 5.0)
    return round(score)  # Returns integer 0 to 5

class LGBMRankerService:
    def __init__(self):
        self.model = None
        self.load_model()
        
    def load_model(self):
        if os.path.exists(settings.MODEL_PATH):
            try:
                self.model = lgb.Booster(model_file=settings.MODEL_PATH)
                print(f"Loaded LightGBM Ranker model from {settings.MODEL_PATH}")
            except Exception as e:
                print(f"Failed to load LightGBM Ranker: {e}")
        else:
            print("No model found. Call pipeline/train to fit the LGBMRanker.")

    def train(self) -> Dict[str, Any]:
        """
        Synthetically pairs patients and foods, calculates suitability labels,
        and trains the LightGBM LambdaMART ranker.
        """
        if not os.path.exists(settings.PATIENT_STORE_PATH) or not os.path.exists(settings.FOOD_STORE_PATH):
            raise FileNotFoundError("Feature stores are missing. Run preprocessor first.")
            
        patients_df = pd.read_csv(settings.PATIENT_STORE_PATH)
        foods_df = pd.read_csv(settings.FOOD_STORE_PATH)
        
        print(f"Generating training interaction matrix for {len(patients_df)} patients & {len(foods_df)} foods...")
        
        records = []
        groups = []
        
        # Enumerate and compute pairs
        for p_idx, p_row in patients_df.iterrows():
            p_dict = p_row.to_dict()
            p_dict['ir_risk_code'] = encode_risk(p_dict['insulin_resistance_risk'])
            p_dict['hormone_sev_code'] = encode_risk(p_dict['hormonal_imbalance_severity'])
            p_dict['inflammation_risk_code'] = encode_risk(p_dict['inflammation_risk'])
            p_dict['cv_risk_code'] = encode_risk(p_dict['cardiovascular_risk'])
            
            p_feat_values = {f: p_dict.get(f, 0.0) for f in PATIENT_FEATS}
            
            p_food_count = 0
            for f_idx, f_row in foods_df.iterrows():
                f_dict = f_row.to_dict()
                suitability = compute_suitability_score(p_dict, f_dict)
                
                # Combine features
                combined_row = p_feat_values.copy()
                for col in FOOD_FEATS:
                    combined_row[col] = f_dict.get(col, 0.0)
                    
                combined_row['relevance'] = suitability
                combined_row['PatientID'] = p_idx
                combined_row['FoodID'] = f_dict.get('FoodID')
                combined_row['FoodName'] = f_dict.get('FoodName')
                
                records.append(combined_row)
                p_food_count += 1
                
            groups.append(p_food_count)
            
        train_df = pd.DataFrame(records)
        
        # Train-val split by patients to avoid data leakage
        num_patients = len(patients_df)
        train_pat_count = int(0.8 * num_patients)
        
        train_groups = groups[:train_pat_count]
        val_groups = groups[train_pat_count:]
        
        split_idx = sum(train_groups)
        
        X_train = train_df.iloc[:split_idx][ALL_FEATURES]
        y_train = train_df.iloc[:split_idx]['relevance']
        
        X_val = train_df.iloc[split_idx:][ALL_FEATURES]
        y_val = train_df.iloc[split_idx:]['relevance']
        
        print(f"Training LambdaMART ranker. Train samples: {len(X_train)}, Val samples: {len(X_val)}")
        
        # Prepare datasets
        train_dataset = lgb.Dataset(X_train, label=y_train, group=train_groups)
        val_dataset = lgb.Dataset(X_val, label=y_val, group=val_groups, reference=train_dataset)
        
        # Set parameters
        params = {
            'objective': 'lambdarank',
            'metric': 'ndcg',
            'ndcg_eval_at': [5, 10],
            'learning_rate': 0.08,
            'max_depth': 6,
            'num_leaves': 31,
            'min_data_in_leaf': 20,
            'verbose': -1,
            'seed': 42
        }
        
        # Train
        evals = {}
        booster = lgb.train(
            params,
            train_dataset,
            num_boost_round=80,
            valid_sets=[val_dataset],
            callbacks=[lgb.record_evaluation(evals)]
        )
        
        # Save model
        os.makedirs(os.path.dirname(settings.MODEL_PATH), exist_ok=True)
        booster.save_model(settings.MODEL_PATH)
        self.model = booster
        
        # Compute validation NDCG metrics
        best_iter = 80
        best_ndcg_val = evals['valid_0']['ndcg@10'][-1]
        
        print(f"Model saved to {settings.MODEL_PATH}. Iterations: {best_iter}, final NDCG@10: {best_ndcg_val:.4f}")
        return {
            "status": "success",
            "best_iteration": best_iter,
            "ndcg_10": best_ndcg_val,
            "train_samples": len(X_train),
            "val_samples": len(X_val)
        }

    def rank_foods_for_patient(self, profile: PatientProfile) -> List[Dict[str, Any]]:
        """
        Rank all foods in the database for a specific patient profile.
        """
        if self.model is None:
            raise RuntimeError("LGBMRanker model is not trained/loaded. Run training first.")
            
        if not os.path.exists(settings.FOOD_STORE_PATH):
            raise FileNotFoundError("Food store not found.")
            
        foods_df = pd.read_csv(settings.FOOD_STORE_PATH)
        
        # Prepare patient values
        p_dict = profile.model_dump()
        p_dict['ir_risk_code'] = encode_risk(p_dict['insulin_resistance_risk'])
        p_dict['hormone_sev_code'] = encode_risk(p_dict['hormonal_imbalance_severity'])
        p_dict['inflammation_risk_code'] = encode_risk(p_dict['inflammation_risk'])
        p_dict['cv_risk_code'] = encode_risk(p_dict['cardiovascular_risk'])
        
        p_feat_values = {f: p_dict.get(f, 0.0) for f in PATIENT_FEATS}
        
        # Pair with all foods
        records = []
        for idx, row in foods_df.iterrows():
            f_dict = row.to_dict()
            
            # Combine features
            combined_row = p_feat_values.copy()
            for col in FOOD_FEATS:
                combined_row[col] = f_dict.get(col, 0.0)
            records.append(combined_row)
            
        candidate_df = pd.DataFrame(records)
        
        # Predict ranking scores
        scores = self.model.predict(candidate_df[ALL_FEATURES])
        
        # Compile results
        results = []
        for idx, score in enumerate(scores):
            food_row = foods_df.iloc[idx].to_dict()
            
            # Verify suitability rules (hard constraints check)
            relevance_label = compute_suitability_score(p_dict, food_row)
            
            # If relevance is 0, we push it to strict avoidance or filter it
            is_avoided = (relevance_label == 0.0)
            
            results.append({
                "food_id": int(food_row['FoodID']),
                "food_name": food_row['FoodName'],
                "category": food_row['Category'],
                "calories": float(food_row['Calories']),
                "protein": float(food_row['Protein']),
                "carbs": float(food_row['Carbohydrates']),
                "fat": float(food_row['Fat']),
                "fiber": float(food_row['Fiber']),
                "glycemic_index": float(food_row['GlycemicIndex']),
                "pcos_friendliness_score": float(food_row['pcos_friendliness_score']),
                "ranking_score": float(score),
                "is_avoided": is_avoided
            })
            
        # Sort foods:
        # Non-avoided foods sorted by descending ranking_score, followed by avoided foods (ranking_score set to -999)
        for r in results:
            if r['is_avoided']:
                r['ranking_score'] = -999.0
                
        results = sorted(results, key=lambda x: x['ranking_score'], reverse=True)
        
        # Deduplicate by food name (case-insensitive) to prevent repetitive items in top recommendations
        seen_names = set()
        deduplicated_results = []
        for r in results:
            name_lower = r['food_name'].lower().strip()
            if name_lower not in seen_names:
                seen_names.add(name_lower)
                deduplicated_results.append(r)
                
        return deduplicated_results

# Singleton ranker instance
ranker_service = None

def get_ranker_service() -> LGBMRankerService:
    global ranker_service
    if ranker_service is None:
        ranker_service = LGBMRankerService()
    return ranker_service

def get_diverse_recommendations(
    results: List[Dict[str, Any]], 
    profile: PatientProfile, 
    cuisine: str = None, 
    limit: int = 15
) -> List[Dict[str, Any]]:
    """
    Selects a categorically balanced subset of foods (Proteins, Vegetables, Grains, Legumes, Nuts/Seeds)
    and filters/prioritizes based on the requested cuisine style to ensure compatibility.
    """
    # 1. Filter out cuisine mismatches if a cuisine is specified
    filtered_results = []
    
    if cuisine:
        cuisine_lower = cuisine.lower().strip()
        
        indian_keywords = [
            "dal", "chilla", "idli", "sambhar", "paneer", "roti", "khichdi", "raita", 
            "biryani", "curry", "tikka", "masala", "chana", "lobia", "rajma", "masoor", 
            "soya", "sabzi", "ragi", "korma", "kadhai", "naan", "tandoori", "chawal",
            "kabsa", "halwa", "kheer", "lassi", "upma", "poha", "paratha", "dosa"
        ]
        
        mediterranean_keywords = [
            "hummus", "tahini", "greek", "feta", "caprese", "olive", "falafel", "mediterranean",
            "tabbouleh", "tzatziki", "baba ganoush", "shawarma", "gyros"
        ]
        
        for r in results:
            food_name_lower = r['food_name'].lower()
            
            is_indian_specific = any(kw in food_name_lower for kw in indian_keywords)
            is_med_specific = any(kw in food_name_lower for kw in mediterranean_keywords)
            
            if cuisine_lower in ["indian", "south asian"]:
                # Exclude Mediterranean specific items from Indian plans
                if is_med_specific and not is_indian_specific:
                    continue
            elif cuisine_lower in ["mediterranean", "greek", "middle eastern"]:
                # Exclude Indian specific items from Mediterranean plans
                if is_indian_specific and not is_med_specific:
                    continue
            elif cuisine_lower in ["western", "american", "european"]:
                # Exclude highly specific prepared Indian/Med items from general Western plans
                if (is_indian_specific or is_med_specific) and not any(kw in food_name_lower for kw in ["chicken", "salmon", "salad", "spinach", "broccoli"]):
                    continue
                    
            filtered_results.append(r)
    else:
        filtered_results = results

    # 2. Categorize remaining foods
    categories = {
        "protein": [],
        "vegetable": [],
        "grain": [],
        "legume": [],
        "nut_seed": [],
        "other": []
    }
    
    non_veg_keywords = ["chicken", "fish", "salmon", "tuna", "egg", "meat", "pork", "shrimp", "seafood", "poultry", "mutton", "beef", "turkey", "cod", "tilapia"]
    veg_protein_keywords = ["tofu", "paneer", "tempeh", "soya"]
    veg_keywords = ["spinach", "broccoli", "asparagus", "zucchini", "cucumber", "cabbage", "carrot", "tomato", "salad", "greens", "okra", "cauliflower", "mushroom", "kale", "brussels sprouts"]
    grain_keywords = ["quinoa", "oats", "rice", "barley", "roti", "bread", "sourdough", "ragi", "idli", "chilla", "khichdi"]
    legume_keywords = ["lentils", "dal", "chickpeas", "beans", "chana", "lobia", "kidney beans"]
    nut_seed_keywords = ["almonds", "chia", "flax", "walnuts", "seeds", "cashews", "peanuts", "butter"]
    
    for r in filtered_results:
        if r['is_avoided']:
            categories["other"].append(r)
            continue
            
        name_lower = r['food_name'].lower()
        cat_lower = r['category'].lower()
        
        # Check Protein
        if any(kw in name_lower or kw in cat_lower for kw in non_veg_keywords):
            categories["protein"].append(r)
        elif any(kw in name_lower or kw in cat_lower for kw in veg_protein_keywords):
            categories["protein"].append(r)
        # Check Legume
        elif any(kw in name_lower or kw in cat_lower for kw in legume_keywords):
            categories["legume"].append(r)
        # Check Nut/Seed
        elif any(kw in name_lower or kw in cat_lower for kw in nut_seed_keywords):
            categories["nut_seed"].append(r)
        # Check Grain
        elif any(kw in name_lower or kw in cat_lower for kw in grain_keywords):
            categories["grain"].append(r)
        # Check Vegetable
        elif any(kw in name_lower or kw in cat_lower for kw in veg_keywords) or "vegetable" in cat_lower or "salad" in name_lower:
            categories["vegetable"].append(r)
        else:
            categories["other"].append(r)
            
    # Select top items from each group
    diverse_list = []
    groups_to_take = ["protein", "vegetable", "grain", "legume", "nut_seed"]
    
    # Take top 3 from each main group to hit up to 15 foods
    for g in groups_to_take:
        diverse_list.extend(categories[g][:3])
        
    # If we have less than limit, fill from the rest
    if len(diverse_list) < limit:
        remaining = []
        for g in groups_to_take:
            remaining.extend(categories[g][3:])
        remaining.extend(categories["other"])
        remaining = sorted(remaining, key=lambda x: x['ranking_score'], reverse=True)
        diverse_list.extend(remaining[:limit - len(diverse_list)])
        
    diverse_list = sorted(diverse_list, key=lambda x: x['ranking_score'], reverse=True)
    return diverse_list[:limit]
