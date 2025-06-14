from app.services.kafka.producer import publish_price_event

# Example payload - make sure this matches your DB schema!
event = {
    "symbol": "AAPL",
    "price": 185.50,
    "timestamp": "2025-06-14T18:45:00Z",
    "provider": "alpha_vantage"
}

publish_price_event(event)
