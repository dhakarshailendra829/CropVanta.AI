import pandas as pd

def get_market_price(df, crop_name, state_name=None):
    """
    Returns market prices for a given crop.
    If state_name is provided, filters prices for that state only.

    Args:
        df (pd.DataFrame): Market data
        crop_name (str): Crop name to search
        state_name (str, optional): State to filter prices

    Returns:
        pd.DataFrame or None: Filtered market prices
    """
    df = df.copy()
    df['commodity_lower'] = df['commodity'].astype(str).str.lower()
    crop_lower = crop_name.lower()

    crop_data = df[df['commodity_lower'] == crop_lower]

    if state_name:
        crop_data['state_lower'] = crop_data['state'].astype(str).str.lower()
        state_lower = state_name.lower()
        crop_data = crop_data[crop_data['state_lower'] == state_lower]

    if not crop_data.empty:
        return crop_data[['date', 'state', 'district', 'market', 'min_price', 'max_price', 'modal_price']]
    else:
        return None
