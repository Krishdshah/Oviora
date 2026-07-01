import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Oviora NutriAI"
    API_V1_STR: str = "/api/v1"
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "PLACEHOLDER_KEY")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "PLACEHOLDER_KEY")
    
    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATASET_DIR: str = "/Users/lakshbaweja/Programming/Samsung innovate/model 5/Dataset"
    
    # Output stores
    DATA_OUTPUT_DIR: str = os.path.join(BASE_DIR, "data")
    PATIENT_STORE_PATH: str = os.path.join(BASE_DIR, "data", "patient_feature_store.csv")
    FOOD_STORE_PATH: str = os.path.join(BASE_DIR, "data", "food_feature_store.csv")
    MODEL_PATH: str = os.path.join(BASE_DIR, "data", "lgb_ranker.txt")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Ensure output directory exists
os.makedirs(settings.DATA_OUTPUT_DIR, exist_ok=True)
