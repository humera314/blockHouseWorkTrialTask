from typing import List

from pydantic import BaseModel, Field


class PollRequest(BaseModel):
    symbols: List[str] = Field(..., example=["AAPL", "MSFT"])
    interval: int = Field(..., example=60)
    provider: str = Field(..., example="alpha_vantage")


class PollResponse(BaseModel):
    job_id: str = Field(..., example="poll_123")
    status: str = Field(..., example="accepted")
    config: PollRequest
