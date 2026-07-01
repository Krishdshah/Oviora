import os
import pandas as pd
import numpy as np
from typing import List, Optional
from nutrition_app.config import settings
from nutrition_app.data_pipeline.schemas import PatientAdvancedInput, PatientProfile, FoodItem

def preprocess_patient_data(input_data: PatientAdvancedInput) -> PatientProfile:
    # 1. Physical metrics calculations
    bmi = input_data.weight_kg / ((input_data.height_cm / 100) ** 2)
    
    # Waist to Hip ratio
    waist_to_hip_ratio = (input_data.waist_inch * 2.54) / (input_data.hip_inch * 2.54) if input_data.hip_inch > 0 else 0
    
    # 2. Lab metrics and ratios
    homa_ir = None
    if input_data.fasting_glucose is not None and input_data.fasting_insulin is not None:
        homa_ir = (input_data.fasting_glucose * input_data.fasting_insulin) / 405
        
    lh_fsh_ratio = None
    if input_data.lh is not None and input_data.fsh is not None and input_data.fsh > 0:
        lh_fsh_ratio = input_data.lh / input_data.fsh

    # 3. Categorize Obesity
    if bmi < 18.5:
        obesity_status = "Underweight"
    elif bmi < 25.0:
        obesity_status = "Normal"
    elif bmi < 30.0:
        obesity_status = "Overweight"
    else:
        obesity_status = "Obese"
        
    # 4. Insulin Resistance Risk (with Fallbacks)
    if homa_ir is not None:
        if homa_ir > 2.0:
            insulin_resistance_risk = "High"
        elif homa_ir > 1.4:
            insulin_resistance_risk = "Medium"
        else:
            insulin_resistance_risk = "Low"
    else:
        # Fallback estimation using physical markers & symptoms
        symptoms_lower = [s.lower() for s in input_data.symptoms]
        has_weight_gain = "weight_gain" in symptoms_lower or "weight gain" in symptoms_lower
        has_fatigue = "fatigue" in symptoms_lower
        if bmi >= 28.0 or (has_weight_gain and waist_to_hip_ratio > 0.85):
            insulin_resistance_risk = "High"
        elif bmi >= 25.0 or has_weight_gain or has_fatigue:
            insulin_resistance_risk = "Medium"
        else:
            insulin_resistance_risk = "Low"

    # 5. Hormonal Imbalance Severity (with Fallbacks)
    if lh_fsh_ratio is not None or input_data.amh is not None:
        lh_ratio_val = lh_fsh_ratio if lh_fsh_ratio is not None else 1.0
        amh_val = input_data.amh if input_data.amh is not None else 2.0
        if lh_ratio_val > 2.0 or amh_val > 6.0:
            hormonal_imbalance_severity = "High"
        elif lh_ratio_val > 1.5 or amh_val > 4.0:
            hormonal_imbalance_severity = "Medium"
        else:
            hormonal_imbalance_severity = "Low"
    else:
        # Fallback estimation using cycle regularity & symptoms
        symptoms_lower = [s.lower() for s in input_data.symptoms]
        cycle_irregular = input_data.cycle_regularity.lower() == "irregular"
        has_hirsutism = "hirsutism" in symptoms_lower or "excess hair" in symptoms_lower or "hair growth" in symptoms_lower
        has_acne = "acne" in symptoms_lower or "pimples" in symptoms_lower
        if cycle_irregular and (has_hirsutism or has_acne):
            hormonal_imbalance_severity = "High"
        elif cycle_irregular or has_hirsutism or has_acne:
            hormonal_imbalance_severity = "Medium"
        else:
            hormonal_imbalance_severity = "Low"

    # 6. Inflammation Risk (with Fallbacks)
    symptoms_lower = [s.lower() for s in input_data.symptoms]
    has_fatigue = "fatigue" in symptoms_lower
    if bmi >= 30.0 or (has_fatigue and input_data.exercise_hours_per_week < 2.0):
        inflammation_risk = "High"
    elif bmi >= 25.0 or has_fatigue or input_data.exercise_hours_per_week < 3.0:
        inflammation_risk = "Medium"
    else:
        inflammation_risk = "Low"

    # 7. Cardiovascular Risk (with Fallbacks)
    if input_data.hypertension_status or (bmi >= 30.0 and waist_to_hip_ratio > 0.88):
        cardiovascular_risk = "High"
    elif bmi >= 27.0 or waist_to_hip_ratio > 0.82:
        cardiovascular_risk = "Medium"
    else:
        cardiovascular_risk = "Low"

    # 8. Exercise Habits
    if input_data.exercise_hours_per_week < 1.5:
        exercise_habits = "Sedentary"
    elif input_data.exercise_hours_per_week <= 4.0:
        exercise_habits = "Moderate"
    else:
        exercise_habits = "Active"

    # 9. Caloric Requirement (Mifflin-St Jeor for women)
    bmr = 10 * input_data.weight_kg + 6.25 * input_data.height_cm - 5 * input_data.age - 161
    activity_multiplier = 1.2
    if exercise_habits == "Moderate":
        activity_multiplier = 1.375
    elif exercise_habits == "Active":
        activity_multiplier = 1.55
    caloric_requirement = bmr * activity_multiplier

    # 10. Protein Requirement
    if exercise_habits == "Active":
        protein_requirement_g = 1.2 * input_data.weight_kg
    elif exercise_habits == "Moderate":
        protein_requirement_g = 1.0 * input_data.weight_kg
    else:
        protein_requirement_g = 0.8 * input_data.weight_kg

    return PatientProfile(
        age=input_data.age,
        weight_kg=input_data.weight_kg,
        height_cm=input_data.height_cm,
        waist_inch=input_data.waist_inch,
        hip_inch=input_data.hip_inch,
        cycle_regularity=input_data.cycle_regularity,
        dietary_preference=input_data.dietary_preference,
        allergies=input_data.allergies,
        symptoms=input_data.symptoms,
        goals=input_data.goals,
        exercise_hours_per_week=input_data.exercise_hours_per_week,
        fasting_glucose=input_data.fasting_glucose,
        fasting_insulin=input_data.fasting_insulin,
        lh=input_data.lh,
        fsh=input_data.fsh,
        amh=input_data.amh,
        tsh=input_data.tsh,
        prolactin=input_data.prolactin,
        progesterone=input_data.progesterone,
        vit_d=input_data.vit_d,
        follicle_num_l=input_data.follicle_num_l,
        follicle_num_r=input_data.follicle_num_r,
        follicle_size_l=input_data.follicle_size_l,
        follicle_size_r=input_data.follicle_size_r,
        diabetes_status=input_data.diabetes_status,
        hypertension_status=input_data.hypertension_status,
        bmi=round(bmi, 2),
        waist_to_hip_ratio=round(waist_to_hip_ratio, 2),
        homa_ir=round(homa_ir, 2) if homa_ir is not None else None,
        lh_fsh_ratio=round(lh_fsh_ratio, 2) if lh_fsh_ratio is not None else None,
        obesity_status=obesity_status,
        insulin_resistance_risk=insulin_resistance_risk,
        hormonal_imbalance_severity=hormonal_imbalance_severity,
        inflammation_risk=inflammation_risk,
        cardiovascular_risk=cardiovascular_risk,
        exercise_habits=exercise_habits,
        caloric_requirement=round(caloric_requirement, 1),
        protein_requirement_g=round(protein_requirement_g, 1)
    )

def calculate_derived_food_metrics(food_df: pd.DataFrame) -> pd.DataFrame:
    df = food_df.copy()
    
    # Ensure all required numeric columns are present and clean
    numeric_cols = [
        'Calories', 'Protein', 'Carbohydrates', 'Fat', 'Fiber', 
        'GlycemicIndex', 'Sodium_mg', 'Potassium_mg', 'Magnesium_mg', 
        'Calcium_mg', 'VitaminD_mcg', 'Zinc_mg', 'Omega3_g', 'SaturatedFat_g', 'Sugars'
    ]
    for col in numeric_cols:
        if col not in df.columns:
            df[col] = 0.0
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

    # 1. Nutrient Density: (Protein, Fiber, Micronutrients) relative to Calories
    # Normalize components for scaling
    p_norm = df['Protein'] / 50.0
    fib_norm = df['Fiber'] / 30.0
    mg_norm = df['Magnesium_mg'] / 400.0
    ca_norm = df['Calcium_mg'] / 1000.0
    zn_norm = df['Zinc_mg'] / 15.0
    vitd_norm = df['VitaminD_mcg'] / 20.0
    omega3_norm = df['Omega3_g'] / 2.0
    
    df['NutrientDensity'] = ((p_norm + fib_norm + mg_norm + ca_norm + zn_norm + vitd_norm + omega3_norm) * 100) / (df['Calories'] + 50)
    
    # 2. Glycemic Load: (Carbohydrates * Glycemic Index) / 100
    df['GlycemicLoad'] = (df['Carbohydrates'] * df['GlycemicIndex']) / 100

    # 3. Heart Health Indicator (low sodium/sat fat, high fiber/potassium)
    df['HeartHealthIndicator'] = 50 + 20 * (df['Fiber'] / 5.0) + 20 * (df['Potassium_mg'] / 300.0) - 20 * (df['Sodium_mg'] / 200.0) - 20 * (df['SaturatedFat_g'] / 5.0)
    df['HeartHealthIndicator'] = df['HeartHealthIndicator'].clip(0, 100)

    # 4. Anti-Inflammatory Potential (high fiber/omega3/magnesium, low sugars/sat fat)
    df['AntiInflammatoryPotential'] = 50 + 25 * df['Omega3_g'] + 15 * (df['Fiber'] / 5.0) + 10 * (df['Magnesium_mg'] / 100.0) - 25 * (df['Sugars'] / 10.0) - 15 * (df['SaturatedFat_g'] / 5.0)
    df['AntiInflammatoryPotential'] = df['AntiInflammatoryPotential'].clip(0, 100)

    # 5. Insulin Resistance Suitability (low GI, high fiber/protein)
    df['InsulinResistanceSuitability'] = (100 - df['GlycemicIndex']) * 0.6 + (df['Fiber'] / 5.0 * 20.0) + (df['Protein'] / 10.0 * 20.0)
    df['InsulinResistanceSuitability'] = df['InsulinResistanceSuitability'].clip(0, 100)

    # 6. Hormonal Health Score (essential zinc, magnesium, vit d, omega3)
    df['HormonalHealthScore'] = 20 * (df['Zinc_mg'] / 5.0) + 30 * (df['Magnesium_mg'] / 100.0) + 25 * (df['VitaminD_mcg'] / 5.0) + 25 * df['Omega3_g']
    df['HormonalHealthScore'] = df['HormonalHealthScore'].clip(0, 100)

    # 7. Weight Management Score (high protein/fiber, low GI/calories)
    df['WeightManagementScore'] = 50 - (df['Calories'] - 150) / 10.0 + (df['Protein'] / 10.0 * 20.0) + (df['Fiber'] / 5.0 * 20.0) - (df['GlycemicIndex'] / 10.0 * 5.0)
    df['WeightManagementScore'] = df['WeightManagementScore'].clip(0, 100)

    # 8. Overall PCOS Friendliness Score (weighted combo of targeted metrics)
    df['pcos_friendliness_score'] = (
        0.30 * df['InsulinResistanceSuitability'] + 
        0.25 * df['HormonalHealthScore'] + 
        0.25 * df['AntiInflammatoryPotential'] + 
        0.20 * df['WeightManagementScore']
    )
    df['pcos_friendliness_score'] = df['pcos_friendliness_score'].clip(0, 100)

    return df

def build_feature_stores():
    print("Building patient and food feature stores...")
    os.makedirs(settings.DATA_OUTPUT_DIR, exist_ok=True)
    
    # ------------------ PATIENT STORE ------------------
    xlsx_path = os.path.join(settings.DATASET_DIR, "archive (9)", "PCOS_data_without_infertility.xlsx")
    csv_path = os.path.join(settings.DATASET_DIR, "archive (9)", "PCOS_infertility.csv")
    
    if os.path.exists(xlsx_path) and os.path.exists(csv_path):
        df_without = pd.read_excel(xlsx_path, sheet_name='Full_new')
        df_inf = pd.read_csv(csv_path)
        
        # Clean column spaces
        df_without.columns = df_without.columns.str.strip()
        df_inf.columns = df_inf.columns.str.strip()
        
        # Merge on patient file no.
        # df_inf file no is 10001, 10002... whereas df_without is 1, 2...
        df_without['Patient File No.'] = df_without['Patient File No.'].astype(int)
        df_inf['Patient File No.'] = df_inf['Patient File No.'].astype(int) - 10000
        
        # Merge
        merged_patient = pd.merge(df_without, df_inf, on='Patient File No.', suffixes=('', '_inf'))
        
        # We will parse this data into a standardized patient store.
        # Since it's clinical data of women with PCOS (PCOS (Y/N) == 1), let's keep it.
        # Derived fields:
        patient_profiles = []
        for idx, row in merged_patient.iterrows():
            # Extract raw parameters
            age = row.get('Age (yrs)', 28.0)
            weight = row.get('Weight (Kg)', 60.0)
            height = row.get('Height(Cm)', 160.0) # Check raw name in log: 'Height(Cm) ' (with space)
            if 'Height(Cm)' not in merged_patient.columns and 'Height(Cm) ' in merged_patient.columns:
                height = row.get('Height(Cm) ', 160.0)
            
            waist = row.get('Waist(inch)', 32.0)
            hip = row.get('Hip(inch)', 36.0)
            
            # Fasting glucose (RBS is available, let's use it as glucose)
            glucose = row.get('RBS(mg/dl)', 90.0)
            # Fasting insulin
            insulin = row.get('Fasting Insulin (uIU/mL)', 8.0)
            if 'Fasting Insulin (uIU/mL)' not in merged_patient.columns and 'Fasting insulin (uIU/mL)' in merged_patient.columns:
                insulin = row.get('Fasting insulin (uIU/mL)', 8.0)
            
            lh = row.get('LH(mIU/mL)', 4.0)
            fsh = row.get('FSH(mIU/mL)', 5.0)
            
            # AMH
            amh = row.get('AMH(ng/mL)', 3.0)
            if amh is None or pd.isna(amh):
                amh = row.get('AMH(ng/mL)_inf', 3.0)
            
            tsh = row.get('TSH (mIU/L)', 2.0)
            prolactin = row.get('PRL(ng/mL)', 15.0)
            progesterone = row.get('PRG(ng/mL)', 1.0)
            vitd = row.get('Vit D3 (ng/mL)', 20.0)
            
            # Follicles
            fol_l = row.get('Follicle No. (L)', 4)
            fol_r = row.get('Follicle No. (R)', 4)
            fol_size_l = row.get('Avg. F size (L) (mm)', 10.0)
            fol_size_r = row.get('Avg. F size (R) (mm)', 10.0)
            
            cycle_regularity = "irregular" if row.get('Cycle(R/I)', 2) == 4 or row.get('Cycle(R/I)', 2) == 3 else "regular"
            # In Kaggle dataset: Cycle(R/I) is 2 for Regular, 4 for Irregular
            if row.get('Cycle(R/I)', 2) == 4:
                cycle_regularity = "irregular"
            else:
                cycle_regularity = "regular"
                
            # Symptoms
            symptoms = []
            if row.get('Weight gain(Y/N)', 0) == 1: symptoms.append("weight_gain")
            if row.get('hair growth(Y/N)', 0) == 1: symptoms.append("hirsutism")
            if row.get('Skin darkening (Y/N)', 0) == 1: symptoms.append("skin_darkening")
            if row.get('Hair loss(Y/N)', 0) == 1: symptoms.append("hair_loss")
            if row.get('Pimples(Y/N)', 0) == 1: symptoms.append("acne")
            
            # Exercise
            reg_exercise = row.get('Reg.Exercise(Y/N)', 0)
            exercise_hours = 4.0 if reg_exercise == 1 else 0.5
            
            # Food habits from fast food
            fast_food = row.get('Fast food (Y/N)', 0)
            diet_pref = "non-veg" if fast_food == 1 else "veg"
            
            # Create input schema
            inp = PatientAdvancedInput(
                age=float(age),
                weight_kg=float(weight),
                height_cm=float(height),
                waist_inch=float(waist),
                hip_inch=float(hip),
                cycle_regularity=cycle_regularity,
                dietary_preference=diet_pref,
                allergies=[],
                symptoms=symptoms,
                goals=["regular_cycles", "weight_loss"] if cycle_regularity == "irregular" else ["energy"],
                exercise_hours_per_week=float(exercise_hours),
                fasting_glucose=float(glucose) if not pd.isna(glucose) else None,
                fasting_insulin=float(insulin) if not pd.isna(insulin) else None,
                lh=float(lh) if not pd.isna(lh) else None,
                fsh=float(fsh) if not pd.isna(fsh) else None,
                amh=float(amh) if not pd.isna(amh) and isinstance(amh, (int, float)) else None, # Clean non-numeric AMH if any
                tsh=float(tsh) if not pd.isna(tsh) else None,
                prolactin=float(prolactin) if not pd.isna(prolactin) else None,
                progesterone=float(progesterone) if not pd.isna(progesterone) else None,
                vit_d=float(vitd) if not pd.isna(vitd) else None,
                follicle_num_l=int(fol_l) if not pd.isna(fol_l) else None,
                follicle_num_r=int(fol_r) if not pd.isna(fol_r) else None,
                follicle_size_l=float(fol_size_l) if not pd.isna(fol_size_l) else None,
                follicle_size_r=float(fol_size_r) if not pd.isna(fol_size_r) else None,
                diabetes_status=False,
                hypertension_status=False
            )
            profile = preprocess_patient_data(inp)
            patient_profiles.append(profile.model_dump())
            
        patient_store_df = pd.DataFrame(patient_profiles)
        patient_store_df.to_csv(settings.PATIENT_STORE_PATH, index=False)
        print(f"Saved {len(patient_store_df)} processed patient profiles to {settings.PATIENT_STORE_PATH}")
    else:
        print("Clinical datasets not found in settings.DATASET_DIR. Please check paths.")

    # ------------------ FOOD STORE ------------------
    food_csv_1 = os.path.join(settings.DATASET_DIR, "daily_food_nutrition_dataset.csv")
    food_csv_2 = os.path.join(settings.DATASET_DIR, "pred_food.csv")
    
    if os.path.exists(food_csv_1) and os.path.exists(food_csv_2):
        df_daily = pd.read_csv(food_csv_1, on_bad_lines='skip')
        df_pred = pd.read_csv(food_csv_2, on_bad_lines='skip')
        
        # Clean column names
        df_daily.columns = df_daily.columns.str.strip()
        df_pred.columns = df_pred.columns.str.strip()
        
        # We will build a merged food feature store
        # Normalize food names to match
        df_daily['norm_name'] = df_daily['Food_Item'].str.lower().str.strip()
        df_pred['norm_name'] = df_pred['Food Name'].str.lower().str.strip()
        
        merged_foods = []
        
        # Match foods in df_pred first, and augment with df_daily
        for idx, row in df_pred.iterrows():
            name = row['Food Name']
            norm = row['norm_name']
            
            # Find matching items in df_daily
            match = df_daily[df_daily['norm_name'] == norm]
            
            # Set values
            category = "General"
            meal_type = "Any"
            sugars = 0.0
            cholesterol = 0.0
            
            if not match.empty:
                category = match.iloc[0]['Category']
                meal_type = match.iloc[0]['Meal_Type']
                sugars = match.iloc[0].get('Sugars (g)', 0.0)
                cholesterol = match.iloc[0].get('Cholesterol (mg)', 0.0)
            
            # Extract basic macronutrients
            cal = row.get('Calories', 100.0)
            carbs = row.get('Carbohydrates', 10.0)
            prot = row.get('Protein', 2.0)
            fat = row.get('Fat', 1.0)
            gi = row.get('Glycemic Index', 50.0)
            fiber = row.get('Fiber Content', 1.0)
            sodium = row.get('Sodium Content', 10.0)
            potassium = row.get('Potassium Content', 100.0)
            magnesium = row.get('Magnesium Content', 20.0)
            calcium = row.get('Calcium Content', 30.0)
            
            # Standardize Vitamin D and Zinc and Omega3 based on names
            vit_d = 0.0
            zinc = 0.0
            omega3 = 0.0
            sat_fat = 0.1 * fat
            
            # Heuristics based on categories or names
            name_lower = name.lower()
            if "egg" in name_lower or "salmon" in name_lower or "sardine" in name_lower or "tuna" in name_lower:
                vit_d = 5.0 # mcg
                zinc = 1.0 # mg
                if "salmon" in name_lower or "tuna" in name_lower or "sardine" in name_lower:
                    omega3 = 1.5 # g
            elif "chia" in name_lower or "flax" in name_lower or "walnut" in name_lower:
                omega3 = 2.0
                zinc = 2.0
                magnesium = 150.0
            elif "spinach" in name_lower or "kale" in name_lower or "broccoli" in name_lower:
                magnesium = 80.0
                calcium = 100.0
                zinc = 0.5
            elif "pumpkin seeds" in name_lower or "sunflower seeds" in name_lower:
                zinc = 5.0
                magnesium = 250.0
            elif "avocado" in name_lower:
                omega3 = 0.1
                potassium = 480.0
            elif "yogurt" in name_lower or "milk" in name_lower or "cheese" in name_lower:
                calcium = 120.0
                vit_d = 1.2
                sat_fat = 0.6 * fat
                
            merged_foods.append({
                'FoodID': idx + 1,
                'FoodName': name,
                'Category': category,
                'Calories': cal,
                'Protein': prot,
                'Carbohydrates': carbs,
                'Fat': fat,
                'Fiber': fiber,
                'GlycemicIndex': gi,
                'Sodium_mg': sodium,
                'Potassium_mg': potassium,
                'Magnesium_mg': magnesium,
                'Calcium_mg': calcium,
                'VitaminD_mcg': vit_d,
                'Zinc_mg': zinc,
                'Omega3_g': omega3,
                'SaturatedFat_g': sat_fat,
                'Sugars': sugars,
                'Cholesterol_mg': cholesterol,
                'Meal_Type': meal_type
            })
            
        food_df = pd.DataFrame(merged_foods)
        # Apply enrichments
        enriched_food_df = calculate_derived_food_metrics(food_df)
        enriched_food_df.to_csv(settings.FOOD_STORE_PATH, index=False)
        print(f"Saved {len(enriched_food_df)} enriched food items to {settings.FOOD_STORE_PATH}")
    else:
        print("Food datasets not found in settings.DATASET_DIR. Please check paths.")

if __name__ == "__main__":
    build_feature_stores()
