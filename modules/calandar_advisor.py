import pandas as pd
import requests
from datetime import datetime
from typing import Dict, List, Optional
from modules.core.logger import get_logger
from modules.core.config import settings

logger = get_logger(__name__)

class CalendarAdvisor:
    def __init__(self):
        # Professional practice: Store static data in a structured format
        self.calendar_data = [
            {"Crop": "Wheat", "Region": "North India", "Sowing Start": 11, "Sowing End": 12, "Harvest Start": 3, "Harvest End": 4, "Sowing Period": "Nov - Dec", "Harvest Period": "Mar - Apr"},
            {"Crop": "Rice", "Region": "East India", "Sowing Start": 6, "Sowing End": 7, "Harvest Start": 10, "Harvest End": 11, "Sowing Period": "Jun - Jul", "Harvest Period": "Oct - Nov"},
            {"Crop": "Maize", "Region": "Pan India", "Sowing Start": 6, "Sowing End": 7, "Harvest Start": 10, "Harvest End": 11, "Sowing Period": "Jun - Jul", "Harvest Period": "Oct - Nov"},
            {"Crop": "Sugarcane", "Region": "Pan India", "Sowing Start": 2, "Sowing End": 4, "Harvest Start": 11, "Harvest End": 3, "Sowing Period": "Feb - Apr", "Harvest Period": "Nov - Mar"},
        ]

    def get_calendar_df(self) -> pd.DataFrame:
        """Returns the calendar as a DataFrame for UI display."""
        return pd.DataFrame(self.calendar_data)

    def get_current_recommendations(self) -> List[str]:
        """Returns crops that should be sown in the current month."""
        current_month = datetime.now().month
        recommended = [
            item["Crop"] for item in self.calendar_data 
            if item["Sowing Start"] <= current_month <= item["Sowing End"]
        ]
        return recommended

    def fetch_rain_forecast(self, lat: float, lon: float) -> Dict:
        """
        Fetches weather data using professional error handling.
        """
        try:
            # Using Open-Meteo (Free for non-commercial use)
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=precipitation_sum&timezone=auto"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            rain_mm = data['daily']['precipitation_sum'][0]
            
            return {
                "status": "success",
                "rain_mm": rain_mm,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
        except Exception as e:
            logger.error(f"Weather API Error: {e}")
            return {"status": "error", "message": str(e)}

    def get_actionable_advice(self, rain_mm: float) -> str:
        """Returns professional agricultural advice based on rain levels."""
        if rain_mm > 10:
            return "⚠️ Heavy rain expected. Avoid fertilizer application and ensure proper drainage."
        elif 0 < rain_mm <= 10:
            return "🌦 Light rain expected. You may skip today's irrigation cycle."
        else:
            return "☀️ Dry weather. Proceed with standard irrigation and weeding."