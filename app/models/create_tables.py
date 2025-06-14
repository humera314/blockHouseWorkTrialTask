from app.core.db import Base, engine  # Make sure this points to your actual Base and engine
from app.models.job_config import PollingJobConfig
from app.models.market_data import RawMarketData
from app.models.symbol_average import SymbolAverage

print("🛠️ Creating database tables...")

try:
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully.")
except Exception as e:
    print("❌ Failed to create tables:", e)
