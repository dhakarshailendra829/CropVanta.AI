import numpy as np
from typing import Dict, Any, Optional
from modules.core.logger import get_logger
from modules.core.schemas import CropInput
from modules.ai_researcher import perform_crop_research 

logger = get_logger("Crop_Advisor_Engine")

class CropAdvisor:
    def __init__(self, model: Any, scaler: Any):
        self.model = model
        self.scaler = scaler
        self.version = "3.1.0-Stable"
        
        self.offline_db = {
            'Rice': "Requires high humidity and heavy rainfall. Best grown in clayey soil.",
            'Maize': "Requires moderate temperatures and well-drained fertile soil.",
            'Wheat': "Thrives in cool weather and requires well-drained loamy soil.",
            'Coffee': "Needs a hot and humid climate and well-drained loamy soil.",
            'Cotton': "Requires high temperature, light rainfall, and 210 frost-free days."
        }

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
        try:
            scaled_features = self._prepare_features(input_data)
            predicted_label = self.model.predict(scaled_features)[0]
            crop_name = self.crop_map.get(predicted_label, "Unknown")

            confidence = 0.0
            if hasattr(self.model, "predict_proba"):
                probabilities = self.model.predict_proba(scaled_features)[0]
                confidence = float(np.max(probabilities))

            try:
                logger.info(f"Attempting Research for: {crop_name}")
                research_insights = perform_crop_research(crop_name)
                
                if not research_insights or "**" in research_insights:
                    research_insights = self.offline_db.get(crop_name, "Highly suitable based on soil NPK levels.")
            except Exception as res_err:
                logger.warning(f"Research failed, using offline data: {res_err}")
                research_insights = self.offline_db.get(crop_name, "Optimal growth predicted for this season.")

            return {
                "status": "success",
                "crop_name": crop_name,
                "description": research_insights, 
                "confidence_score": round(confidence * 100, 2),
                "model_version": self.version,
                "metadata": {
                    "is_reliable": confidence > 0.75,
                    "engine": "RandomForest_Integrated",
                    "label_id": int(predicted_label)
                }
            }

        except Exception as e:
            logger.error(f"Recommendation Error: {str(e)}")
            return {"status": "error", "message": str(e)}