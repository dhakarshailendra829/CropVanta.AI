import numpy as np
from typing import Dict, Any, Optional
from modules.core.logger import get_logger
from modules.core.schemas import CropInput
# --- NEW: Autonomous Research Import ---
from modules.ai_researcher import perform_crop_research 

logger = get_logger("Crop_Advisor_Engine")

class CropAdvisor:
    def __init__(self, model: Any, scaler: Any):
        self.model = model
        self.scaler = scaler
        self.version = "3.0.0-Autonomous" # Upgraded Version
        
        self.crop_map = {
            20: 'Rice', 11: 'Maize', 3: 'Chickpea', 9: 'Kidneybeans', 18: 'Pigeonpeas',
            13: 'Mothbeans', 14: 'Mungbean', 2: 'Blackgram', 10: 'Lentil', 19: 'Pomegranate',
            1: 'Banana', 12: 'Mango', 7: 'Grapes', 21: 'Watermelon', 15: 'Muskmelon',
            0: 'Apple', 16: 'Orange', 17: 'Papaya', 4: 'Coconut', 6: 'Cotton',
            8: 'Jute', 5: 'Coffee'
        }

    def _prepare_features(self, data: CropInput) -> np.ndarray:
        try:
            feature_list = [
                data.nitrogen, data.phosphorus, data.potassium, 
                data.temperature, data.humidity, data.ph, data.rainfall
            ]
            features = np.array(feature_list).reshape(1, -1)
            return self.scaler.transform(features)
        except Exception as e:
            logger.error(f"Transformation Error: {e}")
            raise ValueError("Invalid Input Data")

    def recommend_crop(self, input_data: CropInput) -> Dict[str, Any]:
        """
        Predicts crop AND performs autonomous web research.
        """
        try:
            scaled_features = self._prepare_features(input_data)
            predicted_label = self.model.predict(scaled_features)[0]
            crop_name = self.crop_map.get(predicted_label, "Unknown")

            # --- STEP 1: Calculate Confidence ---
            confidence = 0.0
            if hasattr(self.model, "predict_proba"):
                probabilities = self.model.predict_proba(scaled_features)[0]
                confidence = float(np.max(probabilities))

            # --- STEP 2: AUTONOMOUS RESEARCH (The Upgrade) ---
            # Yeh line DuckDuckGo se live data fetch karegi
            logger.info(f"Triggering Autonomous Research for: {crop_name}")
            research_insights = perform_crop_research(crop_name)

            return {
                "status": "success",
                "crop_name": crop_name,
                "description": research_insights, # Ab yahan LIVE data aayega
                "confidence_score": round(confidence * 100, 2),
                "model_version": self.version,
                "metadata": {
                    "is_reliable": confidence > 0.75,
                    "engine": "RandomForest_Integrated",
                    "label_id": int(predicted_label),
                    "research_status": "Complete"
                }
            }

        except Exception as e:
            logger.error(f"Recommendation Error: {str(e)}")
            return {"status": "error", "message": f"AI Engine Error: {str(e)}"}