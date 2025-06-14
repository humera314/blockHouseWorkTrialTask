import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, String

from app.core.db import Base


class RawMarketData(Base):
    __tablename__ = "raw_market_data"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    symbol = Column(String, index=True)
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    provider = Column(String)
    raw_json = Column(String)
