import numpy as np
from typing import Dict, Any, Optional
from modules.core.logger import get_logger
from modules.core.schemas import CropInput
from modules.crop_mapping import get_crop_info

logger = get_logger(__name__)

class CropAdvisor:
    def __init__(self, model: Any, scaler: Any):
        """
        Initialize with a pre-loaded model and scaler.
        In industry, we inject dependencies rather than loading files inside classes.
        """
        self.model = model
        self.scaler = scaler
        self.version = "2.0.0"

    def _prepare_features(self, data: CropInput) -> np.ndarray:
        """
        Converts the Pydantic schema into a scaled NumPy array for the model.
        """
        try:
            # Convert schema to list in the exact order the model expects
            feature_list = [
                data.nitrogen, 
                data.phosphorus, 
                data.potassium, 
                data.temperature, 
                data.humidity, 
                data.ph, 
                data.rainfall
            ]
            
            # Reshape for a single prediction (1, -1)
            features = np.array(feature_list).reshape(1, -1)
            
            # Apply scaling
            return self.scaler.transform(features)
        except Exception as e:
            logger.error(f"Feature transformation failed: {e}")
            raise ValueError("Error processing soil data for the model.")

    def recommend_crop(self, input_data: CropInput) -> Dict[str, Any]:
        """
        Predict the most suitable crop and provide metadata.
        """
        try:
            # 1. Transform & Validate
            scaled_features = self._prepare_features(input_data)
            
            # 2. Prediction
            predicted_label = self.model.predict(scaled_features)[0]
            crop_info = get_crop_info(predicted_label)

            # 3. Confidence Score (Probability)
            confidence = None
            if hasattr(self.model, "predict_proba"):
                probabilities = self.model.predict_proba(scaled_features)[0]
                confidence = float(np.max(probabilities))

            logger.info(f"Prediction successful: {crop_info.get('name')} with {confidence} confidence")

            # 4. Structured Response
            return {
                "status": "success",
                "crop_name": crop_info.get("name", "Unknown"),
                "description": crop_info.get("description", "No description available."),
                "confidence_score": round(confidence * 100, 2) if confidence else "N/A",
                "model_version": self.version,
                "metadata": {
                    "is_reliable": confidence > 0.7 if confidence else False,
                    "engine": type(self.model).__name__
                }
            }

        except Exception as e:
            logger.error(f"Recommendation Error: {str(e)}")
            return {
                "status": "error",
                "message": "Model failed to generate a recommendation."
            }