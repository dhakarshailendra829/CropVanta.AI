import pandas as pd
import requests
import joblib
import numpy as np
from datetime import datetime, date
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from functools import lru_cache
from modules.core.logger import get_logger
from modules.core.schemas import WeatherData

logger = get_logger("Weather_Advisor")

try:
    rf_temp = joblib.load("models/rf_temp.pkl")
    logger.info("Temperature model loaded successfully")
except Exception as e:
    logger.error(f"Model load failed: {e}. Using API fallback.")
    rf_temp = None

geolocator = Nominatim(user_agent="cropvanta_ai", timeout=10)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

@lru_cache(maxsize=50)
def geocode_location(location_name: str):
    try:
        location = geocode(location_name)
        if location:
            return round(location.latitude, 4), round(location.longitude, 4)
        logger.warning(f"No coordinates found for {location_name}")
    except Exception as e:
        logger.warning(f"Geocoding failed for {location_name}: {e}")
    return None

def get_live_weather(location_name: str, target_date: datetime = None):
    if target_date is None:
        target_date = datetime.now()

    coords = geocode_location(location_name)
    if not coords:
        logger.error(f"Failed to geocode {location_name}")
        return None

    lat, lon = coords
    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,relative_humidity_2m_mean&timezone=Asia/Kolkata&forecast_days=7"

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        daily = data.get("daily", {})
        time_list = daily.get("time", [])

        date_str = target_date.strftime("%Y-%m-%d")
        if date_str not in time_list:
            logger.error(f"Date {date_str} not in forecast range {time_list[:3]}...")
            return None

        idx = time_list.index(date_str)

        # Extract real data [web:1][web:2]
        max_temp = daily["temperature_2m_max"][idx]
        min_temp = daily["temperature_2m_min"][idx]
        precip = daily.get("precipitation_sum", [0])[idx]
        humidity = daily.get("relative_humidity_2m_mean", [60])[idx]

        final_temp = max_temp
        confidence = 0.95
        source = "Live API (Open-Meteo)"
        if rf_temp is not None:
            try:
                features = np.array([[min_temp, precip, humidity]]).reshape(1, -1)
                ml_pred = rf_temp.predict(features)[0]
                final_temp = (max_temp + ml_pred) / 2  # Blend for improvement
                confidence = 0.98
                source += " + ML Model"
                logger.info("ML model prediction blended successfully")
            except Exception as ml_e:
                logger.warning(f"ML prediction failed: {ml_e}")

        validated_data = WeatherData(
            city=location_name,
            temp=final_temp,
            description="Forecast" if idx > 0 else "Current conditions",
            humidity=humidity
        )

        return {
            "location": validated_data.city.title(),
            "max_temp": round(validated_data.temp, 1),
            "min_temp": round(min_temp, 1),
            "precipitation": precip,
            "humidity": humidity,
            "source": source,
            "confidence": confidence
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
    except (KeyError, ValueError, IndexError) as e:
        logger.error(f"Data parsing error: {e} - Keys: {daily.keys() if 'daily' in locals() else 'no daily'}")
    except Exception as e:
        logger.error(f"Weather fetch error: {e}")
    return None