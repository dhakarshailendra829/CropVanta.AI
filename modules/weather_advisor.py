import pandas as pd
import requests
import joblib
import numpy as np
from datetime import datetime
from geopy.geocoders import Nominatim
from functools import lru_cache
from modules.core.logger import get_logger
from modules.core.schemas import WeatherData

logger = get_logger("Weather_Advisor")

try:
    rf_temp = joblib.load("models/rf_temp.pkl")
except Exception as e:
    logger.error(f"Model Load Error: {e}")
    rf_temp = None

@lru_cache(maxsize=50)
def geocode_location(location_name: str):
    try:
        geolocator = Nominatim(user_agent="cropvanta_ai")
        location = geolocator.geocode(location_name, timeout=5)
        if location:
            return round(location.latitude, 4), round(location.longitude, 4)
    except Exception as e:
        logger.warning(f"Geocoding failed for {location_name}: {e}")
    return None

def get_live_weather(location_name: str, date: datetime):
    coords = geocode_location(location_name)
    if not coords: return None

    lat, lon = coords
    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=Asia/Kolkata"

    try:
        response = requests.get(api_url, timeout=5)
        data = response.json()
        daily = data.get("daily")
        date_str = date.strftime("%Y-%m-%d")
        
        idx = daily["time"].index(date_str)
        
        validated_data = WeatherData(
            city=location_name,
            temp=daily["temperature_2m_max"][idx],
            description="Clear Sky",
            humidity=60 
        )

        return {
            "location": validated_data.city.title(),
            "max_temp": validated_data.temp,
            "source": "Live API (Open-Meteo)",
            "confidence": 0.95
        }
    except Exception as e:
        logger.error(f"Weather API Error: {e}")
        return None