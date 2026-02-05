import pandas as pd
from typing import Optional, Dict
from modules.core.logger import get_logger
from modules.market_sentiment import analyze_market_mood

logger = get_logger("Market_Advisor")

class MarketAdvisor:
    def process_market_data(self, df: pd.DataFrame, crop: str, state: Optional[str] = None) -> Dict:
        try:
            if df.empty:
                return {"status": "error", "message": "Database is empty"}

            # Clean data for better matching
            df['commodity'] = df['commodity'].str.lower().str.strip()
            df['state'] = df['state'].str.lower().str.strip()
            
            search_crop = crop.lower().strip()
            search_state = state.lower().strip() if state else None

            # Smart Filter: State and Crop both
            if search_state:
                filtered_df = df[(df['commodity'].str.contains(search_crop)) & (df['state'] == search_state)]
            else:
                filtered_df = df[df['commodity'].str.contains(search_crop)]

            # Fallback: Agar state mein nahi mila, toh pure India ka data dikhao
            if filtered_df.empty:
                filtered_df = df[df['commodity'].str.contains(search_crop)]
                logger.warning(f"No data for {crop} in {state}, showing national average.")

            if filtered_df.empty:
                return {"status": "no_data", "message": f"No data found for {crop}."}

            # Insights Calculation
            latest_price = filtered_df.iloc[-1]['modal_price']
            avg_price = filtered_df['modal_price'].mean()
            
            sample_headlines = [f"{crop} market trend stable", f"Demand for {crop} remains steady in {state}"]
            sentiment = analyze_market_mood(sample_headlines)

            return {
                "status": "success",
                "data": filtered_df.tail(10), # Return last 10 records for the graph
                "insights": {
                    "current_modal": latest_price,
                    "avg_price": round(avg_price, 2),
                    "trend_sentiment": sentiment, 
                    "volatility": round(filtered_df['modal_price'].std(), 2) if len(filtered_df) > 1 else 0
                }
            }
        except Exception as e:
            logger.error(f"Market Logic Error: {e}")
            return {"status": "error", "message": "Market analysis failed. Please check CSV format."}