# app/api/prices.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import SessionLocal
from app.models.market_data import RawMarketData

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/prices/latest")
def get_latest_price(symbol: str, db: Session = Depends(get_db)):
    record = (
        db.query(RawMarketData)
        .filter(RawMarketData.symbol == symbol)
        .order_by(RawMarketData.timestamp.desc())
        .first()
    )
    if record:
        return {
            "symbol": record.symbol,
            "price": record.price,
            "timestamp": record.timestamp,
            "provider": record.provider,
        }
    return {"error": "Price not found"}
