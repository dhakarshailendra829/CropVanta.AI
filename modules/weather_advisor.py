import pandas as pd
import requests
import joblib
import numpy as np
from datetime import datetime
from geopy.geocoders import Nominatim

try:
    rf_temp = joblib.load('models/rf_temp.pkl')          
except Exception:
    rf_temp = None

try:
    weather_df = pd.read_csv('data/weather_data.csv')    
except Exception:
    weather_df = None

def geocode_location(location_name):
    """Convert location name to latitude & longitude using OpenStreetMap (Nominatim)."""
    try:
        geolocator = Nominatim(user_agent="crop_weather_app")
        location = geolocator.geocode(location_name)
        if location:
            return location.latitude, location.longitude
    except Exception:
        return None
    return None

def get_live_weather(location_name, date):
    """Fetch live weather using Open-Meteo free API."""
    coords = geocode_location(location_name)
    if not coords:
        return None
    lat, lon = coords
    api_url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
        f"&timezone=Asia/Kolkata"
    )
    try:
        res = requests.get(api_url, timeout=5)
        data = res.json()
        if "daily" not in data:
            return None

        daily = data["daily"]
        dates = daily["time"]
        date_str = date.strftime("%Y-%m-%d")
        if date_str in dates:
            idx = dates.index(date_str)
            forecast = {
                "Location": location_name.title(),
                "Date": date_str,
                "Max Temp (°C)": daily["temperature_2m_max"][idx],
                "Min Temp (°C)": daily["temperature_2m_min"][idx],
                "Precipitation (mm)": daily["precipitation_sum"][idx],
                "Source": "🌐",
                "Note": "This is real time Weather."
            }
            return forecast
    except Exception:
        return None
    return None

def get_model_weather(location_name, date):
    """Fallback: Predict temperature using RF model & historical weather_data.csv."""
    if rf_temp is None or weather_df is None:
        return None

    try:
        df = weather_df.copy()
        df['Date'] = pd.to_datetime(df['Date'])
        df['Month'] = df['Date'].dt.month
        month = pd.to_datetime(date).month

        if 'Location' in df.columns:
            df = pd.get_dummies(df, columns=['Location'], prefix='Location')
        X_cols = [c for c in df.columns if c not in ['Temperature', 'Date']]
        X_input = pd.DataFrame(np.zeros((1, len(X_cols))), columns=X_cols)
        X_input['Month'] = month
        loc_col = f"Location_{location_name}"
        if loc_col in X_input.columns:
            X_input[loc_col] = 1

        temp_pred = rf_temp.predict(X_input)[0]
        forecast = {
            "Location": location_name.title(),
            "Date": date.strftime("%Y-%m-%d"),
            "Predicted Temp (°C)": round(temp_pred, 2),
            "Source": "🤖 RF Model",
            "Note": "Fallback from trained model"
        }
        return forecast
    except Exception:
        return None

def get_weather_forecast(location_name, date):
    """
    Main function for app.py
    1. Try live API first
    2. If unavailable, use RF model fallback
    Returns dictionary ready for UI
    """

    forecast = get_live_weather(location_name, date)
    if forecast:
        return forecast

    model_forecast = get_model_weather(location_name, date)
    if model_forecast:
        return model_forecast

    return {
        "Location": location_name.title(),
        "Date": date.strftime("%Y-%m-%d"),
        "Source": "Not Available",
        "Note": "No forecast found for this location/date"
    }
