import pandas as pd
import requests
import joblib
import numpy as np
from datetime import datetime
from geopy.geocoders import Nominatim
from functools import lru_cache

# ---------------- LOAD RESOURCES ---------------- #

try:
    rf_temp = joblib.load("models/rf_temp.pkl")
except Exception:
    rf_temp = None

try:
    weather_df = pd.read_csv("data/weather_data.csv")
except Exception:
    weather_df = None


# ---------------- GEO CODING ---------------- #

@lru_cache(maxsize=50)
def geocode_location(location_name: str):
    """
    Convert location name to latitude & longitude.
    Cached to avoid API rate-limit.
    """
    try:
        geolocator = Nominatim(user_agent="agri_advisor_app")
        location = geolocator.geocode(location_name, timeout=5)
        if location:
            return round(location.latitude, 4), round(location.longitude, 4)
    except Exception:
        pass
    return None


# ---------------- LIVE WEATHER ---------------- #

def get_live_weather(location_name: str, date: datetime):
    coords = geocode_location(location_name)
    if not coords:
        return None

    lat, lon = coords
    api_url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
        "&timezone=Asia/Kolkata"
    )

    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()

        daily = data.get("daily")
        if not daily:
            return None

        date_str = date.strftime("%Y-%m-%d")
        if date_str not in daily["time"]:
            return None

        idx = daily["time"].index(date_str)

        return {
            "location": location_name.title(),
            "date": date_str,
            "max_temp": daily["temperature_2m_max"][idx],
            "min_temp": daily["temperature_2m_min"][idx],
            "precipitation": daily["precipitation_sum"][idx],
            "source": "Live API",
            "confidence": 0.90,
            "note": "Real-time weather from Open-Meteo"
        }

    except Exception:
        return None


# ---------------- MODEL FALLBACK ---------------- #

def get_model_weather(location_name: str, date: datetime):
    if rf_temp is None or weather_df is None:
        return None

    try:
        df = weather_df.copy()
        df["Date"] = pd.to_datetime(df["Date"])
        df["Month"] = df["Date"].dt.month

        month = date.month

        if "Location" in df.columns:
            df = pd.get_dummies(df, columns=["Location"], prefix="Location")

        X_cols = [c for c in df.columns if c not in ["Temperature", "Date"]]
        X_input = pd.DataFrame(np.zeros((1, len(X_cols))), columns=X_cols)

        X_input["Month"] = month
        loc_col = f"Location_{location_name}"
        if loc_col in X_input.columns:
            X_input[loc_col] = 1

        temp_pred = rf_temp.predict(X_input)[0]

        return {
            "location": location_name.title(),
            "date": date.strftime("%Y-%m-%d"),
            "predicted_temp": round(float(temp_pred), 2),
            "source": "ML Model (RF)",
            "confidence": 0.65,
            "note": "Prediction based on historical data"
        }

    except Exception:
        return None


# ---------------- PUBLIC API ---------------- #

def get_weather_forecast(location_name: str, date: datetime):
    """
    Strategy:
    1. Live Weather API
    2. ML Model Fallback
    3. Graceful failure
    """

    live = get_live_weather(location_name, date)
    if live:
        return live

    model_based = get_model_weather(location_name, date)
    if model_based:
        return model_based

    return {
        "location": location_name.title(),
        "date": date.strftime("%Y-%m-%d"),
        "source": "Unavailable",
        "confidence": 0.0,
        "note": "Weather data not available for this location/date"
    }
