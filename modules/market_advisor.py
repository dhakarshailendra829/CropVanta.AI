import pandas as pd
from typing import Optional, Dict
from modules.core.logger import get_logger
from modules.market_sentiment import analyze_market_mood

logger = get_logger("Market_Advisor")

class MarketAdvisor:
    def process_market_data(self, df: pd.DataFrame, crop: str, state: Optional[str] = None) -> Dict:
        try:
            df['commodity'] = df['commodity'].str.lower()
            filtered_df = df[df['commodity'] == crop.lower()]
            
            if filtered_df.empty:
                return {"status": "no_data", "message": f"No data for {crop}"}

            latest_price = filtered_df.iloc[-1]['modal_price']
            
            # Fetch headlines for Sentiment (Simulation or API call)
            sample_headlines = [f"{crop} prices hitting record highs", f"High demand for {crop} in major markets"]
            sentiment = analyze_market_mood(sample_headlines)

            return {
                "status": "success",
                "insights": {
                    "current_modal": latest_price,
                    "trend_sentiment": sentiment, # Added Sentiment logic
                    "volatility": round(filtered_df['modal_price'].std(), 2)
                }
            }
        except Exception as e:
            logger.error(f"Market Logic Error: {e}")
            return {"status": "error", "message": str(e)}