from sqlalchemy import Column, String, Integer, JSON
from app.core.db import Base
import uuid

class PollingJobConfig(Base):
    __tablename__ = "polling_jobs"

    job_id = Column(String, primary_key=True, default=lambda: f"poll_{uuid.uuid4().hex[:8]}")
    symbols = Column(JSON)
    interval = Column(Integer)
    provider = Column(String)
