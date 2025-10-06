import joblib
import numpy as np
from modules.crop_mapping import get_crop_info  

def recommend_crop(model, scaled_features):
    """
    Predicts the best crop based on scaled features.
    Returns:
        crop_name (str): Name of the recommended crop
        description (str): Description of the crop
    """
    pred_label = model.predict(scaled_features)[0]
    
    crop_info = get_crop_info(pred_label)
    crop_name = crop_info["name"]
    description = crop_info["description"]
    
    return crop_name, description
