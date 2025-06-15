from confluent_kafka import Consumer, KafkaError
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.market_data import RawMarketData
from app.models.symbol_average import SymbolAverage
import json
from datetime import datetime

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'ma-consumer-group-v2',
    'auto.offset.reset': 'earliest'
}

print(" Initializing Kafka Consumer...")
consumer = Consumer(conf)
consumer.subscribe(['price-events'])
print(" Subscribed to topic: price-events")

def calculate_moving_average(prices):
    print(f" Calculating moving average for prices: {prices}")
    result = round(sum(prices[-5:]) / min(5, len(prices)), 2)
    print(f" Computed moving average: {result}")
    return result

def main():
    print(" Consumer started. Listening for price events...\n")
    while True:
       
        msg = consumer.poll(1.0)

        if msg is None:
            
            continue
        if msg.error():
            if msg.error().code() != KafkaError._PARTITION_EOF:
                print(f" Consumer error: {msg.error()}")
            continue

        try:
            print(" Message received, parsing payload...")
            data = json.loads(msg.value())
            print(f" Parsed data: {data}")

            symbol = data["symbol"]
            db: Session = SessionLocal()

            print(f" Fetching last 5 prices for: {symbol}")
            prices = (
                db.query(RawMarketData)
                .filter(RawMarketData.symbol == symbol)
                .order_by(RawMarketData.timestamp.desc())
                .limit(5)
                .all()
            )
            last_5_prices = [p.price for p in reversed(prices)]
            print(f" Prices: {last_5_prices}")

            if len(last_5_prices) > 0:
                ma = calculate_moving_average(last_5_prices)

                existing = db.query(SymbolAverage).filter_by(symbol=symbol).first()
                if existing:
                    print(f" Updating existing average for {symbol}")
                    existing.moving_avg = ma
                    existing.last_updated = datetime.utcnow()
                else:
                    print(f" Creating new average record for {symbol}")
                    new_avg = SymbolAverage(symbol=symbol, moving_avg=ma)
                    db.add(new_avg)

                db.commit()
                print(f" MA updated in DB: {symbol} → {ma}")
            else:
                print("⚠️ No prices in DB for this symbol.")

            db.close()

        except Exception as e:
            print(f" Failed to process message: {e}")

if __name__ == "__main__":
    main()
