import uuid

from sqlalchemy import JSON, Column, Integer, String

from app.core.db import Base


class PollingJobConfig(Base):
    __tablename__ = "polling_jobs"

    job_id = Column(
        String, primary_key=True, default=lambda: f"poll_{uuid.uuid4().hex[:8]}"
    )
    symbols = Column(JSON)
    interval = Column(Integer)
    provider = Column(String)
