import json
from groq import Groq
from typing import Dict, List, Any
from nutrition_app.config import settings
from nutrition_app.data_pipeline.schemas import PatientProfile
from nutrition_app.knowledge_graph.graph_manager import get_graph_manager

class GroqMealPlannerService:
    def __init__(self):
        self.api_configured = False
        self.client = None
        self.setup_groq()

    def setup_groq(self):
        api_key = settings.GROQ_API_KEY
        if api_key and api_key != "PLACEHOLDER_KEY":
            try:
                self.client = Groq(api_key=api_key)
                self.api_configured = True
                print("Groq Client initialized successfully.")
            except Exception as e:
                print(f"Failed to configure Groq Client: {e}")
        else:
            print("Groq API Key is placeholder. Live queries will fail.")

    def generate_meal_plan(
        self, 
        profile: PatientProfile, 
        ranked_foods: List[Dict[str, Any]], 
        cuisine: str, 
        duration_days: int, 
        budget: str,
        model_name: str = "llama-3.3-70b-versatile"
    ) -> Dict[str, Any]:
        """
        Uses Groq to generate a personalized meal plan and nutritional justification.
        """
        if not self.api_configured or self.client is None:
            raise ValueError("Groq API key is not configured or is set to placeholder in .env. Please set a valid key.")

        # Get semantic connections for top foods from Knowledge Graph
        kg = get_graph_manager()
        
        top_foods_info = []
        for food in ranked_foods:
            name = food['food_name']
            kg_context = kg.get_food_context(name)
            relations = []
            if "semantic_connections" in kg_context:
                relations = [f"{c['relation']} {c['target']}" for c in kg_context['semantic_connections']]
            
            top_foods_info.append(
                f"- {name} (Category: {food['category']}, Rank Score: {food['ranking_score']:.2f}): "
                f"Calories: {food['calories']}kcal, Protein: {food['protein']}g, Carbs: {food['carbs']}g. "
                f"Semantic Connections: {', '.join(relations)}. "
                f"SHAP explanation: {food.get('explanation', '')}"
            )
            
        avoid_foods_info = []
        for food in [f for f in ranked_foods if f['is_avoided']][:5]:
            avoid_foods_info.append(
                f"- {food['food_name']} (Category: {food['category']}): Avoid due to allergies or dietary preferences."
            )

        prompt = f"""
You are a highly qualified Clinical PCOS Dietitian and AI Nutrition Assistant.
Your task is to generate a personalized, hormone-balancing meal plan for a patient with PCOS (Polycystic Ovary Syndrome).

### Patient Profile:
- Age: {profile.age} years old
- BMI: {profile.bmi} ({profile.obesity_status})
- Waist-to-Hip Ratio: {profile.waist_to_hip_ratio}
- Insulin Resistance Risk: {profile.insulin_resistance_risk} (HOMA-IR: {profile.homa_ir if profile.homa_ir else 'Not tested'})
- Hormonal Imbalance Severity: {profile.hormonal_imbalance_severity} (LH/FSH: {profile.lh_fsh_ratio if profile.lh_fsh_ratio else 'Not tested'})
- Inflammation Risk: {profile.inflammation_risk}
- Cardiovascular Risk: {profile.cardiovascular_risk}
- Dietary Preference: {profile.dietary_preference}
- Allergies: {', '.join(profile.allergies) if profile.allergies else 'None'}
- PCOS Symptoms: {', '.join(profile.symptoms) if profile.symptoms else 'None'}
- Exercise Habits: {profile.exercise_habits} ({profile.exercise_hours_per_week} hrs/week)
- Target Calorie Requirement: {profile.caloric_requirement} kcal/day
- Target Protein Requirement: {profile.protein_requirement_g} g/day

### User Preferences:
- Cuisine Style: {cuisine}
- Duration: {duration_days} Day(s)
- Budget Constraint: {budget}

### Machine Learning LTR Model Recommendation Guidance:
Here are the top 10 recommended foods for this patient (as determined by a LightGBM LambdaMART ranker based on clinical suitability):
{chr(10).join(top_foods_info)}

And here are the foods that MUST be strictly avoided (allergies or preference exclusions):
{chr(10).join(avoid_foods_info)}

---

    ### Output Requirements:
    Generate a complete meal plan and return the output ONLY in raw, structured JSON format with no markdown blocks or backticks. Follow this exact structure:

    {{
      "meal_plan": [
        {{
          "day": 1,
          "meals": {{
            "breakfast": {{
              "name": "Meal name",
              "ingredients": ["Ingredient 1 with portion size", "Ingredient 2"],
              "instructions": "Brief preparation tip",
              "macronutrients": {{"calories": 450, "protein": 25, "carbs": 35, "fat": 15}}
            }},
            "lunch": {{
              "name": "Meal name",
              "ingredients": ["Ingredient 1 with portion size", "Ingredient 2"],
              "instructions": "Brief preparation tip",
              "macronutrients": {{"calories": 550, "protein": 30, "carbs": 50, "fat": 18}}
            }},
            "dinner": {{
              "name": "Meal name",
              "ingredients": ["Ingredient 1 with portion size", "Ingredient 2"],
              "instructions": "Brief preparation tip",
              "macronutrients": {{"calories": 500, "protein": 35, "carbs": 40, "fat": 16}}
            }},
            "snack": {{
              "name": "Meal name",
              "ingredients": ["Ingredient 1 with portion size", "Ingredient 2"],
              "instructions": "Brief preparation tip",
              "macronutrients": {{"calories": 200, "protein": 10, "carbs": 20, "fat": 8}}
            }}
          }}
        }}
      ],
      "grocery_list": {{
        "produce": ["Spinach", "Avocado"],
        "proteins": ["Eggs", "Wild Salmon"],
        "grains_seeds": ["Chia Seeds", "Oats"],
        "other": []
      }},
      "clinical_reasoning": "A clinical explanation of why this plan stabilizes insulin, balances hormones (LH/FSH), lowers inflammation, and supports weight loss based on the LTR recommendations, SHAP drivers, and knowledge graph paths.",
      "healthy_substitutions": [
        {{"original": "Dairy Milk", "substitute": "Unsweetened Almond Milk", "reason": "Reduces inflammatory response and glycemic index."}}
      ],
      "adherence_tips": [
        "Tip 1 on cycle regularity and stress management",
        "Tip 2 on seed cycling or hydration"
      ]
    }}

    Ensure that:
    1. Every meal is appetizing and suitable for the {cuisine} cuisine.
    2. The foods included in the meal plan are strictly drawn from or heavily compatible with the LTR recommended items.
    3. Absolutely NO ingredients are used that violate the patient's allergies or dietary preference (e.g. no meats if veg, no dairy if allergic).
    4. The daily total macronutrients are aligned with the target caloric intake (+/- 10%) and protein target.
    5. You MUST ensure HIGH variety across days. Every single day (Day 1, Day 2, Day 3, etc.) must have different recipe names and different primary ingredients for breakfast, lunch, dinner, and snacks. Do not repeat the exact same meal name or same main ingredients on consecutive days. Rotate grain sources (e.g., swap between oats, quinoa, barley, brown rice) and protein sources (e.g., swap between salmon, chicken, eggs, lentils, tofu/paneer) dynamically.
    """

        try:
            # We call Groq chat completion API with JSON response format
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional clinical dietitian. You must respond strictly with a valid JSON object. Ensure all fields are fully populated, do not use ellipses or placeholder strings like '{ ... }', and double check that all JSON syntax is correct (separate key-values with colons, close all braces)."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=model_name,
                response_format={"type": "json_object"}
            )
            content = chat_completion.choices[0].message.content
            plan_json = json.loads(content)
            return plan_json
        except Exception as e:
            print(f"Groq API generation failed: {e}")
            raise RuntimeError(f"Groq API Error: {str(e)}")

# Singleton instance
groq_service = None

def get_groq_service() -> GroqMealPlannerService:
    global groq_service
    if groq_service is None:
        groq_service = GroqMealPlannerService()
    return groq_service
