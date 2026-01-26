from typing import Dict, Any, Optional
from modules.core.logger import get_logger

logger = get_logger(__name__)

# Expanded Knowledge Base
# Added optimal ranges to allow the AI to explain 'Why' it recommended a crop
CROP_KNOWLEDGE_BASE = {
    0: {
        "name": "Wheat",
        "category": "Cereal",
        "description": "A staple cereal crop used for flour and bread.",
        "season": "Rabi (Winter)",
        "growth_duration": "120-150 days",
        "ideal_ph": [6.0, 7.5],
        "market_value": "High"
    },
    1: {
        "name": "Rice",
        "category": "Cereal",
        "description": "A primary food crop, thrives in wet conditions.",
        "season": "Kharif (Monsoon)",
        "growth_duration": "105-150 days",
        "ideal_ph": [5.5, 6.5],
        "market_value": "Very High"
    },
    # ... (Keep existing crops but follow this new structure)
    19: {
        "name": "Millets",
        "category": "Cereal/Superfood",
        "description": "Small-grain cereals, highly drought resistant and nutritious.",
        "season": "Kharif/Summer",
        "growth_duration": "70-100 days",
        "ideal_ph": [5.0, 8.0],
        "market_value": "Rising Demand"
    }
}

def get_crop_info(label: int) -> Dict[str, Any]:
    """
    Retrieves rich metadata for a given crop label.
    Uses professional error handling and type hinting.
    """
    try:
        # Ensure label is integer (sometimes models return numpy.int64)
        label_idx = int(label)
        
        crop_data = CROP_KNOWLEDGE_BASE.get(label_idx)
        
        if not crop_data:
            logger.warning(f"Label {label} not found in knowledge base.")
            return {
                "name": f"Unknown Variety ({label})",
                "category": "N/A",
                "description": "Detailed data for this specific variety is currently being updated.",
                "season": "N/A",
                "growth_duration": "N/A",
                "ideal_ph": [0, 0],
                "market_value": "N/A"
            }
            
        return crop_data

    except Exception as e:
        logger.error(f"Error retrieving crop info for label {label}: {e}")
        return {"name": "System Error", "description": "Failed to fetch crop metadata."}

def get_all_crops_by_category(category: str) -> list:
    """Useful for the Admin or Search functionality"""
    return [info["name"] for info in CROP_KNOWLEDGE_BASE.values() if info["category"] == category]