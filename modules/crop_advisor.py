import numpy as np
from typing import Dict, Any, Optional
from modules.core.logger import get_logger
from modules.core.schemas import CropInput

# Note: We are now handling mapping directly or via a robust dictionary
logger = get_logger(__name__)

class CropAdvisor:
    def __init__(self, model: Any, scaler: Any):
        """
        Initialize with a pre-loaded model and scaler.
        """
        self.model = model
        self.scaler = scaler
        self.version = "2.1.0-Prod"
        
        # 🌿 Industry Standard Mapping (Common for the 22-crop dataset)
        self.crop_map = {
            20: 'Rice', 11: 'Maize', 3: 'Chickpea', 9: 'Kidneybeans', 18: 'Pigeonpeas',
            13: 'Mothbeans', 14: 'Mungbean', 2: 'Blackgram', 10: 'Lentil', 19: 'Pomegranate',
            1: 'Banana', 12: 'Mango', 7: 'Grapes', 21: 'Watermelon', 15: 'Muskmelon',
            0: 'Apple', 16: 'Orange', 17: 'Papaya', 4: 'Coconut', 6: 'Cotton',
            8: 'Jute', 5: 'Coffee'
        }

    def _prepare_features(self, data: CropInput) -> np.ndarray:
        """
        Converts the Pydantic schema into a scaled NumPy array.
        """
        try:
            # feature_list must match training order: N, P, K, Temp, Hum, pH, Rain
            feature_list = [
                data.nitrogen, data.phosphorus, data.potassium, 
                data.temperature, data.humidity, data.ph, data.rainfall
            ]
            features = np.array(feature_list).reshape(1, -1)
            return self.scaler.transform(features)
        except Exception as e:
            logger.error(f"Feature transformation failed: {e}")
            raise ValueError("Invalid soil or weather data provided.")

    def recommend_crop(self, input_data: CropInput) -> Dict[str, Any]:
        """
        Predict the most suitable crop and provide rich metadata.
        """
        try:
            # 1. Transform & Scale
            scaled_features = self._prepare_features(input_data)
            
            # 2. Prediction (Numerical Label)
            predicted_label = self.model.predict(scaled_features)[0]
            
            # 3. Handle Mapping (Fixes the 'Unknown Variety' Issue)
            # Agar label dictionary mein nahi milta, toh we show the ID
            crop_name = self.crop_map.get(predicted_label, f"Unknown Crop (ID: {predicted_label})")
            
            # 4. Generate Description Dynamically
            description = self._get_crop_description(crop_name)

            # 5. Confidence Score
            confidence = 0.0
            if hasattr(self.model, "predict_proba"):
                probabilities = self.model.predict_proba(scaled_features)[0]
                confidence = float(np.max(probabilities))

            logger.info(f"Prediction: {crop_name} | Confidence: {confidence:.2f}")

            return {
                "status": "success",
                "crop_name": crop_name,
                "description": description,
                "confidence_score": round(confidence * 100, 2),
                "model_version": self.version,
                "metadata": {
                    "is_reliable": confidence > 0.75,
                    "engine": type(self.model).__name__,
                    "label_id": int(predicted_label)
                }
            }

        except Exception as e:
            logger.error(f"Recommendation Error: {str(e)}")
            return {
                "status": "error",
                "message": f"AI Engine Error: {str(e)}"
            }

    def _get_crop_description(self, crop_name: str) -> str:
        """
        Returns a professional description based on the crop.
        """
        descriptions = {
            "Coffee": "Ideal for high-altitude regions with well-drained soil and consistent rainfall.",
            "Rice": "Requires high humidity and heavy rainfall/irrigation with clayey soil.",
            "Maize": "Versatile crop requiring moderate temperatures and well-aerated soil.",
            "Coconut": "Thrives in tropical climates with sandy-loamy soil and high humidity.",
            "Blackgram": "Short-duration pulse crop ideal for low to moderate rainfall areas."
        }
        return descriptions.get(crop_name, "This crop is highly suitable based on your current soil NPK and weather conditions. Consult the 'Crop Calendar' for sowing dates.")