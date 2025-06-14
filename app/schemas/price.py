from datetime import datetime

from pydantic import BaseModel


class PriceResponse(BaseModel):
    symbol: str
    price: float
    timestamp: datetime
    provider: str
