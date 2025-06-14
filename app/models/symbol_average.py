from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, String

from app.core.db import Base


class SymbolAverage(Base):
    __tablename__ = "symbol_averages"

    symbol = Column(String, primary_key=True)
    moving_avg = Column(Float)
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc))
