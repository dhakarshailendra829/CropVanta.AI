import streamlit as st
import requests
import numpy as np
from streamlit_folium import st_folium
import folium
from typing import Dict, List, Any
from modules.core.logger import get_logger

logger = get_logger(__name__)


class LandSuitabilityAnalyzer:

    def __init__(self):

        self.crop_requirements = {
            "Wheat": {"temp": [10, 25], "rain": 50},
            "Rice": {"temp": [20, 35], "rain": 150},
            "Maize": {"temp": [18, 30], "rain": 60},
            "Cotton": {"temp": [22, 32], "rain": 70},
            "Sugarcane": {"temp": [20, 35], "rain": 120},
            "Soybean": {"temp": [20, 30], "rain": 80},
        }

        self.headers = {
            "User-Agent": "CropVanta/1.0"
        }

    # -----------------------------
    # API 1 : OPEN METEO
    # -----------------------------

    def fetch_open_meteo(self, lat, lon):

        try:

            url = (
                "https://api.open-meteo.com/v1/forecast"
                f"?latitude={lat}"
                f"&longitude={lon}"
                "&daily=temperature_2m_max,precipitation_sum"
                "&timezone=auto"
            )

            r = requests.get(url, timeout=8, headers=self.headers)

            if r.status_code != 200:
                logger.warning("Open Meteo returned non-200 response")
                return None

            data = r.json()

            if "daily" not in data:
                logger.warning("Open Meteo missing daily data")
                return None

            temps = data["daily"].get("temperature_2m_max", [])
            rains = data["daily"].get("precipitation_sum", [])

            if not temps or not rains:
                return None

            return {
                "temp": float(np.mean(temps)),
                "rain": float(np.sum(rains)),
                "source": "Open-Meteo"
            }

        except Exception as e:
            logger.error(f"Open Meteo API failed: {e}")
            return None

    # -----------------------------
    # API 2 : NASA POWER
    # -----------------------------

    def fetch_nasa_power(self, lat, lon):

        try:

            url = (
                "https://power.larc.nasa.gov/api/temporal/daily/point"
                f"?parameters=T2M,PRECTOT"
                f"&community=AG"
                f"&longitude={lon}"
                f"&latitude={lat}"
                "&format=JSON"
            )

            r = requests.get(url, timeout=10, headers=self.headers)

            if r.status_code != 200:
                logger.warning("NASA API returned non-200 response")
                return None

            data = r.json()

            params = data.get("properties", {}).get("parameter", {})

            temps = list(params.get("T2M", {}).values())
            rains = list(params.get("PRECTOT", {}).values())

            if not temps or not rains:
                return None

            return {
                "temp": float(np.mean(temps)),
                "rain": float(np.sum(rains)),
                "source": "NASA POWER"
            }

        except Exception as e:
            logger.error(f"NASA API failed: {e}")
            return None

    # -----------------------------
    # MASTER WEATHER FETCH
    # -----------------------------

    def fetch_geo_data(self, lat, lon):

        try:

            data = self.fetch_open_meteo(lat, lon)

            if data:
                data["success"] = True
                return data

            logger.info("Fallback to NASA POWER")

            data = self.fetch_nasa_power(lat, lon)

            if data:
                data["success"] = True
                return data

            logger.error("All APIs failed. Using fallback values.")

            return {
                "temp": 25,
                "rain": 80,
                "source": "Fallback Data",
                "success": True
            }

        except Exception as e:

            logger.critical(f"Critical weather fetch error: {e}")

            return {
                "temp": 25,
                "rain": 80,
                "source": "Emergency Fallback",
                "success": True
            }

    # -----------------------------
    # SUITABILITY SCORE
    # -----------------------------

    def calculate_suitability(self, temp, rain):

        results = []

        for crop, req in self.crop_requirements.items():

            score = 0

            if req["temp"][0] <= temp <= req["temp"][1]:
                score += 40

            if rain >= req["rain"]:
                score += 60

            results.append({
                "crop": crop,
                "score": score,
                "label": "High" if score > 70 else "Medium" if score > 40 else "Low"
            })

        return sorted(results, key=lambda x: x["score"], reverse=True)


# -----------------------------
# STREAMLIT UI
# -----------------------------

def run():

    try:

        st.subheader("🌍 Land Suitability Analyzer")

        st.write("Click on map to analyze crop suitability.")

        m = folium.Map(location=[20.5937, 78.9629], zoom_start=4)

        m.add_child(folium.LatLngPopup())

        map_data = st_folium(m, width=700, height=400)

        if map_data and map_data.get("last_clicked"):

            lat = map_data["last_clicked"]["lat"]
            lon = map_data["last_clicked"]["lng"]

            st.success(f"📍 Selected Location: {lat:.4f}, {lon:.4f}")

            analyzer = LandSuitabilityAnalyzer()

            geo_info = analyzer.fetch_geo_data(lat, lon)

            temp = geo_info["temp"]
            rain = geo_info["rain"]

            st.info(
                f"🌡 Avg Temp: {temp:.1f}°C | "
                f"🌧 Rain: {rain:.1f} mm | "
                f"📡 Source: {geo_info['source']}"
            )

            rankings = analyzer.calculate_suitability(temp, rain)

            st.subheader("🌾 Crop Suitability Ranking")

            for res in rankings:

                color = (
                    "green" if res["label"] == "High"
                    else "orange" if res["label"] == "Medium"
                    else "red"
                )

                st.markdown(
                    f"**{res['crop']}** : :{color}[{res['label']} Suitability] "
                    f"({res['score']}/100)"
                )

    except Exception as e:

        logger.critical(f"UI Critical Error: {e}")

        st.error(
            "⚠️ Critical system error. Please check model files or configuration."
        )