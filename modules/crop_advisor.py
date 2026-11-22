import numpy as np
from typing import Dict, Any

from modules.core.logger import get_logger
from modules.core.schemas import CropInput
from modules.ai_researcher import perform_crop_research
from modules.core.cache import (
    build_cache_key,
    get_cached_json,
    set_cached_json,
)

logger = get_logger("Crop_Advisor_Engine")


class CropAdvisor:
    def __init__(self, model: Any, scaler: Any, label_encoder: Any):
        self.model = model
        self.scaler = scaler
        self.label_encoder = label_encoder

        self.version = "3.2.0-Ensemble"

        # Verify that model output IDs match LabelEncoder IDs.
        expected_classes = np.arange(len(self.label_encoder.classes_))

        if not np.array_equal(
            np.asarray(self.model.classes_),
            expected_classes,
        ):
            raise ValueError(
                "Model classes do not match LabelEncoder classes."
            )

        if self.model.n_features_in_ != 7:
            raise ValueError("Model must accept exactly 7 features.")

        if self.scaler.n_features_in_ != 7:
            raise ValueError("Scaler must accept exactly 7 features.")

        self.offline_db = {
            "Rice": "Requires high humidity and heavy rainfall. Best grown in clayey soil.",
            "Maize": "Requires moderate temperatures and well-drained fertile soil.",
            "Wheat": "Thrives in cool weather and requires well-drained loamy soil.",
            "Coffee": "Needs a hot and humid climate and well-drained loamy soil.",
            "Cotton": "Requires high temperature, light rainfall, and 210 frost-free days.",
        }

        logger.info(
            "Ensemble model initialized successfully with "
            f"{len(self.label_encoder.classes_)} crop classes."
        )

    
    def _prepare_features(self, data: CropInput) -> np.ndarray:
        try:
            import pandas as pd

            feature_data = pd.DataFrame(
                [[
                    data.nitrogen,
                    data.phosphorus,
                    data.potassium,
                    data.temperature,
                    data.humidity,
                    data.ph,
                    data.rainfall,
                ]],
                columns=[
                    "N",
                    "P",
                    "K",
                    "temperature",
                    "humidity",
                    "ph",
                    "rainfall",
                ],
            )

            return self.scaler.transform(feature_data)

        except Exception as e:
            logger.error(f"Transformation Error: {e}")
            raise ValueError("Invalid Input Data") from e


    def recommend_crop(self, input_data: CropInput) -> Dict[str, Any]:
        try:
            raw_features = [
                input_data.nitrogen,
                input_data.phosphorus,
                input_data.potassium,
                input_data.temperature,
                input_data.humidity,
                input_data.ph,
                input_data.rainfall,
            ]

            cache_key = build_cache_key(
                "crop-recommendation",
                {
                    "model_version": self.version,
                    "features": raw_features,
                },
            )

            cached_result = get_cached_json(cache_key)

            if cached_result is not None:
                logger.info("Crop recommendation served from Redis cache")
                return cached_result

            scaled_features = self._prepare_features(input_data)

            predicted_label = int(
                self.model.predict(scaled_features)[0]
            )

            # Decode the predicted integer using the correct LabelEncoder.
            crop_name = str(
                self.label_encoder.inverse_transform(
                    [predicted_label]
                )[0]
            ).title()

            probabilities = self.model.predict_proba(
                scaled_features
            )[0]

            confidence = float(np.max(probabilities))

            try:
                logger.info(f"Attempting research for: {crop_name}")

                research_insights = perform_crop_research(crop_name)

                if not research_insights or "**" in research_insights:
                    research_insights = self.offline_db.get(
                        crop_name,
                        "Highly suitable based on soil NPK levels.",
                    )

            except Exception as res_err:
                logger.warning(
                    f"Research failed, using offline data: {res_err}"
                )

                research_insights = self.offline_db.get(
                    crop_name,
                    "Optimal growth predicted for this season.",
                )

            result = {
                "status": "success",
                "crop_name": crop_name,
                "description": research_insights,
                "confidence_score": round(confidence * 100, 2),
                "model_version": self.version,
                "metadata": {
                    "is_reliable": confidence > 0.75,
                    "engine": "RandomForest_GradientBoosting_SoftVoting",
                    "label_id": predicted_label,
                },
            }

            set_cached_json(
                cache_key,
                result,
                ttl_seconds=3600,
            )

            return result

        except Exception as e:
            logger.error(f"Recommendation Error: {str(e)}")

            return {
                "status": "error",
                "message": str(e),
            }