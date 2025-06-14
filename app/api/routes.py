from fastapi import APIRouter, Query, Body, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.schemas.price import PriceResponse
from app.services.providers.alpha_vantage import AlphaVantageProvider
from app.core.db import SessionLocal
from app.models.market_data import RawMarketData
from app.services.kafka.producer import publish_price_event

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/prices/latest", response_model=PriceResponse)
async def get_latest_price(symbol: str = Query(...), provider: Optional[str] = "alpha_vantage"):
    db: Session = SessionLocal()
    try:
        provider_instance = AlphaVantageProvider()
        data = provider_instance.fetch_price(symbol)

        market_data = RawMarketData(
            symbol=data["symbol"],
            price=data["price"],
            timestamp=data["timestamp"],
            provider=data["provider"],
            raw_json=data["raw_json"]
        )
        db.add(market_data)
        db.commit()
        db.refresh(market_data)

        publish_price_event({
            "symbol": data["symbol"],
            "price": data["price"],
            "timestamp": data["timestamp"].isoformat(),
            "source": data["provider"],
            "raw_response_id": market_data.id
        })

        return {
            "symbol": data["symbol"],
            "price": data["price"],
            "timestamp": data["timestamp"],
            "provider": data["provider"]
        }
    finally:
        db.close()

# ✅ Add schema for polling request and response
class PollRequest(BaseModel):
    symbols: List[str]
    interval: int
    provider: Optional[str] = "alpha_vantage"

class PollResponse(BaseModel):
    job_id: str
    status: str
    config: PollRequest

@router.post("/prices/poll", response_model=PollResponse, status_code=status.HTTP_202_ACCEPTED)
async def poll_prices(request: PollRequest):
    job_id = f"poll_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

    # Simulate async job initiation (actual background task logic can be added if needed)
    print(f"📥 Polling job accepted: {job_id} → {request.symbols} every {request.interval}s")

    return PollResponse(
        job_id=job_id,
        status="accepted",
        config=request
    )
