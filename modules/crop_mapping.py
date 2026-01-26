from typing import Dict, Any, Optional
from modules.core.logger import get_logger

logger = get_logger(__name__)

CROP_KNOWLEDGE_BASE = {
    0: {"name": "Apple", "category": "Fruit", "description": "Needs cool climate and well-drained acidic soil.", "season": "Winter/Spring", "growth_duration": "120-150 days", "ideal_ph": [5.5, 6.5], "market_value": "Premium"},
    1: {"name": "Banana", "category": "Fruit", "description": "Thrives in tropical humid climates with rich loamy soil.", "season": "Year-round", "growth_duration": "300-365 days", "ideal_ph": [6.5, 7.5], "market_value": "Steady Demand"},
    2: {"name": "Blackgram", "category": "Pulse", "description": "Short duration pulse, improves soil nitrogen.", "season": "Kharif/Rabi", "growth_duration": "70-90 days", "ideal_ph": [6.0, 7.0], "market_value": "High"},
    3: {"name": "Chickpea", "category": "Pulse", "description": "Rabi season pulse, needs moderate weather.", "season": "Rabi", "growth_duration": "90-120 days", "ideal_ph": [6.0, 8.0], "market_value": "Very High"},
    4: {"name": "Coconut", "category": "Plantation", "description": "Coastal crop, requires high humidity and sandy soil.", "season": "Year-round", "growth_duration": "Perennial", "ideal_ph": [5.0, 8.0], "market_value": "High"},
    5: {"name": "Coffee", "category": "Plantation", "description": "Grown in hilly areas with well-distributed rainfall.", "season": "Perennial", "growth_duration": "7-9 months (harvest)", "ideal_ph": [6.0, 6.5], "market_value": "Export Quality"},
    6: {"name": "Cotton", "category": "Fiber", "description": "Cash crop requiring high temperature and moderate rain.", "season": "Kharif", "growth_duration": "160-180 days", "ideal_ph": [5.5, 8.5], "market_value": "High"},
    7: {"name": "Grapes", "category": "Fruit", "description": "Requires hot and dry climate with good irrigation.", "season": "Winter/Spring", "growth_duration": "150-180 days", "ideal_ph": [6.5, 7.5], "market_value": "Premium"},
    8: {"name": "Jute", "category": "Fiber", "description": "Golden fiber, needs high rainfall and alluvial soil.", "season": "Kharif", "growth_duration": "120-150 days", "ideal_ph": [6.0, 7.5], "market_value": "Industrial Demand"},
    9: {"name": "Kidneybeans", "category": "Pulse", "description": "Rich in protein, prefers cool climates like hills.", "season": "Kharif/Rabi", "growth_duration": "90-120 days", "ideal_ph": [6.0, 6.5], "market_value": "High"},
    10: {"name": "Lentil", "category": "Pulse", "description": "Drought tolerant pulse grown in winter.", "season": "Rabi", "growth_duration": "110-130 days", "ideal_ph": [6.0, 8.0], "market_value": "High"},
    11: {"name": "Maize", "category": "Cereal", "description": "Versatile crop used for food, fodder, and fuel.", "season": "Kharif/Summer", "growth_duration": "90-110 days", "ideal_ph": [5.5, 7.5], "market_value": "Moderate"},
    12: {"name": "Mango", "category": "Fruit", "description": "King of fruits, thrives in tropical heat.", "season": "Summer (Harvest)", "growth_duration": "Perennial", "ideal_ph": [5.5, 7.5], "market_value": "Seasonal High"},
    13: {"name": "Mothbeans", "category": "Pulse", "description": "Most drought-resistant pulse, grows in sandy soils.", "season": "Kharif", "growth_duration": "75-90 days", "ideal_ph": [6.5, 7.5], "market_value": "Moderate"},
    14: {"name": "Mungbean", "category": "Pulse", "description": "Short duration pulse, excellent for crop rotation.", "season": "Summer/Kharif", "growth_duration": "60-75 days", "ideal_ph": [6.0, 7.5], "market_value": "High"},
    15: {"name": "Muskmelon", "category": "Fruit", "description": "Summer fruit, needs dry weather and sandy soil.", "season": "Summer", "growth_duration": "80-100 days", "ideal_ph": [6.0, 7.0], "market_value": "Seasonal"},
    16: {"name": "Orange", "category": "Fruit", "description": "Citrus crop, needs well-drained soil and sun.", "season": "Winter", "growth_duration": "180-240 days", "ideal_ph": [6.0, 7.5], "market_value": "High"},
    17: {"name": "Papaya", "category": "Fruit", "description": "Fast-growing fruit, needs warmth and water.", "season": "Year-round", "growth_duration": "9-11 months", "ideal_ph": [6.0, 7.0], "market_value": "Moderate"},
    18: {"name": "Pigeonpeas", "category": "Pulse", "description": "Long-duration pulse, very hardy and deep-rooted.", "season": "Kharif", "growth_duration": "150-180 days", "ideal_ph": [6.5, 7.5], "market_value": "Very High"},
    19: {"name": "Pomegranate", "category": "Fruit", "description": "Hardy fruit, grows well in semi-arid regions.", "season": "Rabi/Kharif", "growth_duration": "150-180 days", "ideal_ph": [5.5, 7.5], "market_value": "Premium"},
    20: {"name": "Rice", "category": "Cereal", "description": "Water-intensive staple crop for humid regions.", "season": "Kharif", "growth_duration": "105-150 days", "ideal_ph": [5.5, 6.5], "market_value": "Universal Demand"},
    21: {"name": "Watermelon", "category": "Fruit", "description": "Requires high heat and sandy riverbeds.", "season": "Summer", "growth_duration": "80-100 days", "ideal_ph": [6.0, 7.0], "market_value": "Seasonal"}
}

def get_crop_info(label: int) -> Dict[str, Any]:
    try:
        label_idx = int(label)
        crop_data = CROP_KNOWLEDGE_BASE.get(label_idx)
        
        if not crop_data:
            logger.warning(f"Label {label} not mapped.")
            return {
                "name": f"New Variety (ID: {label})",
                "category": "Hybrid/Under Research",
                "description": "Our AI has identified a specialized variety. Specific cultivation guides are being optimized.",
                "season": "Experimental",
                "growth_duration": "Variable",
                "ideal_ph": [6.0, 7.0],
                "market_value": "Dynamic"
            }
        return crop_data
    except Exception as e:
        logger.error(f"Mapping Error: {e}")
        return {"name": "Mapping Error", "description": "System encountered an error during classification."}