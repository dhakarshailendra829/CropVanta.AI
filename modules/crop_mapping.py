CROP_INFO = {
    0: {"name": "Wheat", "description": "A staple cereal crop used for flour and bread."},
    1: {"name": "Rice", "description": "A primary food crop, thrives in wet conditions."},
    2: {"name": "Maize", "description": "Corn, used for food, feed, and industrial products."},
    3: {"name": "Sugarcane", "description": "Used for sugar production and bioenergy."},
    4: {"name": "Cotton", "description": "Fiber crop for textiles, needs warm climate."},
    5: {"name": "Soybean", "description": "Rich in protein, used in oil and animal feed."},
    6: {"name": "Chili", "description": "Spicy vegetable crop, requires warm and dry climate."},
    7: {"name": "Tomato", "description": "Widely used vegetable, rich in vitamins."},
    8: {"name": "Potato", "description": "Tubular crop, grows best in cooler climates."},
    9: {"name": "Onion", "description": "Bulb vegetable, requires well-drained soil."},
    10: {"name": "Garlic", "description": "Used as spice and medicinal herb."},
    11: {"name": "Brinjal", "description": "Eggplant, grows well in warm climate."},
    12: {"name": "Carrot", "description": "Root vegetable rich in beta-carotene."},
    13: {"name": "Cabbage", "description": "Leafy vegetable, prefers cooler temperatures."},
    14: {"name": "Cauliflower", "description": "Leafy vegetable, grows best in mild climate."},
    15: {"name": "Peas", "description": "Legume crop, rich in protein and fiber."},
    16: {"name": "Bitter Gourd", "description": "Vegetable with medicinal properties."},
    17: {"name": "Pumpkin", "description": "Gourd crop, used for food and decoration."},
    18: {"name": "Okra", "description": "Also known as lady’s finger, grows in warm conditions."},
    19: {"name": "Millets", "description": "Small-grain cereals, drought resistant."}
}

def get_crop_info(label):
    """
    Returns the crop name and description based on model label.
    If label not found, returns default values.
    """
    return CROP_INFO.get(label, {"name": f"Unknown ({label})", "description": "No description available for this crop yet."})
