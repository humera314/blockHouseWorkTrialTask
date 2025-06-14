from sqlalchemy import Column, String, Float, DateTime
from app.core.db import Base
from datetime import datetime, timezone

class SymbolAverage(Base):
    __tablename__ = "symbol_averages"

    symbol = Column(String, primary_key=True)
    moving_avg = Column(Float)
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc))
