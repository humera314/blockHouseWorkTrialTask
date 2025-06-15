from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get the database URL from the environment
DATABASE_URL = os.getenv("DATABASE_URL")

print(" Loaded DATABASE_URL:", DATABASE_URL)

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print(" Database connection successful:", result.scalar())
except Exception as e:
    print("Database connection failed:", e)
