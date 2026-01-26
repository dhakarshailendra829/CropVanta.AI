import streamlit as st
import requests
import numpy as np
from streamlit_folium import st_folium
import folium
from typing import Dict, List, Any
from modules.core.logger import get_logger

logger = get_logger(__name__)

# --- Logic Class (Backend) ---
class LandSuitabilityAnalyzer:
    def __init__(self):
        self.crop_requirements = {
            "Wheat": {"temp": [10, 25], "rain": 50},
            "Rice": {"temp": [20, 35], "rain": 150},
            "Maize": {"temp": [18, 30], "rain": 60},
            "Cotton": {"temp": [22, 32], "rain": 70},
        }

    def fetch_geo_data(self, lat: float, lon: float) -> Dict[str, Any]:
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,precipitation_sum&timezone=auto"
            response = requests.get(url, timeout=10)
            data = response.json()
            avg_temp = np.mean(data["daily"]["temperature_2m_max"])
            total_rain = np.sum(data["daily"]["precipitation_sum"])
            return {"temp": avg_temp, "rain": total_rain, "success": True}
        except Exception as e:
            logger.error(f"GeoData Error: {e}")
            return {"success": False}

    def calculate_suitability(self, temp: float, rain: float) -> List[Dict]:
        results = []
        for crop, req in self.crop_requirements.items():
            score = 0
            if req["temp"][0] <= temp <= req["temp"][1]: score += 40
            if rain >= req["rain"]: score += 60
            results.append({
                "crop": crop, 
                "score": score, 
                "label": "High" if score > 70 else "Medium" if score > 40 else "Low"
            })
        return sorted(results, key=lambda x: x["score"], reverse=True)

# --- UI Function (Frontend) ---
# app.py isi function ko call karega
def run():
    st.subheader("🌍 Land Suitability Analyzer")
    st.write("Click on the map to analyze location-based suitability.")

    # Folium Map Logic
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=4)
    m.add_child(folium.LatLngPopup())
    map_data = st_folium(m, width=700, height=400)

    if map_data and map_data.get("last_clicked"):
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]
        
        st.success(f"📍 Selected: {lat:.4f}, {lon:.4f}")

        # Class ka instance banakar use karna (OOP approach)
        analyzer = LandSuitabilityAnalyzer()
        geo_info = analyzer.fetch_geo_data(lat, lon)

        if geo_info["success"]:
            temp, rain = geo_info["temp"], geo_info["rain"]
            st.info(f"🌡 Avg Temp: {temp:.1f}°C | 🌧 Total Rain: {rain:.1f}mm")
            
            rankings = analyzer.calculate_suitability(temp, rain)
            
            for res in rankings:
                color = "green" if res["label"] == "High" else "orange" if res["label"] == "Medium" else "red"
                st.markdown(f"**{res['crop']}**: :{color}[{res['label']} Suitability] ({res['score']}/100)")
        else:
            st.error("Failed to fetch weather data for this location.")