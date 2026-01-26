import pandas as pd
from typing import Optional, Dict
from modules.core.logger import get_logger

logger = get_logger(__name__)

class MarketAdvisor:
    def __init__(self, data_path: Optional[str] = None):
        self.data_path = data_path

    def process_market_data(self, df: pd.DataFrame, crop: str, state: Optional[str] = None) -> Dict:
        """
        Analyzes market data to provide price trends and filtering.
        """
        try:
            df['commodity'] = df['commodity'].str.lower()
            df['date'] = pd.to_datetime(df['date'])
            
            # Filter Data
            filtered_df = df[df['commodity'] == crop.lower()]
            if state:
                filtered_df = filtered_df[filtered_df['state'].str.lower() == state.lower()]

            if filtered_df.empty:
                return {"status": "no_data", "message": f"No market data found for {crop}"}

            # Calculate Insights
            latest_price = filtered_df.sort_values('date').iloc[-1]['modal_price']
            avg_price = filtered_df['modal_price'].mean()
            
            # Trend Analysis (Simple Version)
            trend = "Stable"
            if latest_price > avg_price * 1.05: trend = "Upward 📈"
            elif latest_price < avg_price * 0.95: trend = "Downward 📉"

            return {
                "status": "success",
                "data": filtered_df.sort_values('date', ascending=False),
                "insights": {
                    "current_modal": latest_price,
                    "avg_market_price": round(avg_price, 2),
                    "trend": trend,
                    "volatility": round(filtered_df['modal_price'].std(), 2)
                }
            }
        except Exception as e:
            logger.error(f"Market Analysis Error: {e}")
            return {"status": "error", "message": str(e)}