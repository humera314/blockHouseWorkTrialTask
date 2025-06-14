from sqlalchemy import Column, String, Float, DateTime
from app.core.db import Base
import uuid
from datetime import datetime

class RawMarketData(Base):
    __tablename__ = "raw_market_data"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    symbol = Column(String, index=True)
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    provider = Column(String)
    raw_json = Column(String)