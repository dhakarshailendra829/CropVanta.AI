from textblob import TextBlob
from modules.core.logger import get_logger

logger= get_logger("Sentiment_Engine")

def analyze_market_mood(news_headlines):
    """Analyzes news text and returns a sentiment score (Free)."""
    if not news_headlines:
        return "Neutral"
    
    polarity = sum([TextBlob(h).sentiment.polarity for h in news_headlines]) / len(news_headlines)
    
    if polarity > 0.1: return "Bullish 📈"
    elif polarity < -0.1: return "Bearish 📉"
    else: return "Stable ⚖️"