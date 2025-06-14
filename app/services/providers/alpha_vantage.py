import requests
import os
from datetime import datetime
from app.services.providers.base import BaseMarketProvider

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

class AlphaVantageProvider(BaseMarketProvider):
    def fetch_price(self, symbol: str) -> dict:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": API_KEY
        }
        r = requests.get(url, params=params)
        data = r.json()
        quote = data.get("Global Quote", {})
        price = float(quote.get("05. price", 0.0))
        timestamp = datetime.utcnow()
        return {
            "symbol": symbol.upper(),
            "price": price,
            "timestamp": timestamp,
            "provider": "alpha_vantage",
            "raw_json": str(data)
        }