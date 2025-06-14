from app.core.db import engine
from app.models.market_data import RawMarketData
from app.core.db import Base

def init():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created")

if __name__ == "__main__":
    init()