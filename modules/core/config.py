import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "CropVanta AI "
    VERSION: str = "2.0.0"
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    
    # Model Paths
    MODEL_PATH: str = "models/crop_model.pkl"
    SCALER_PATH: str = "models/scaler.pkl"
    
    # App Config
    DEBUG: bool = True

settings = Settings()