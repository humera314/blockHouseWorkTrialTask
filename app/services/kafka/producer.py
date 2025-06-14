from confluent_kafka import Producer
import json
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.market_data import RawMarketData
from datetime import datetime
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Fetch database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/market_data")
print("📄 Loaded DATABASE_URL:", DATABASE_URL)

# ✅ Setup DB session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# ✅ Kafka Producer Configuration
producer_config = {
    'bootstrap.servers': 'localhost:9092'
}
producer = Producer(producer_config)

def publish_price_event(data: dict):
    # ✅ Publish to Kafka
    payload = json.dumps(data)
    producer.produce("price-events", value=payload.encode("utf-8"))
    producer.flush()
    print(f"✅ Published event: {data}")

    # ✅ Store to PostgreSQL
    try:
        db: Session = SessionLocal()
        raw_data = RawMarketData(
            symbol=data["symbol"],
            price=data["price"],
            timestamp=datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%SZ"),
            provider=data["provider"],
            raw_json=json.dumps(data)
        )
        db.add(raw_data)
        db.commit()
        db.close()
        print("📝 Stored event in DB.")
    except Exception as e:
        print("❌ Failed to save to DB:", e)

if __name__ == "__main__":
    sample_event = {
        "symbol": "AAPL",
        "price": 185.5,
        "timestamp": "2025-06-14T18:45:00Z",
        "provider": "alpha_vantage"
    }
    publish_price_event(sample_event)
