from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# -----------------------
# Engine (połączenie z DB)
# -----------------------
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,   # sprawdza czy connection żyje
    pool_recycle=3600     # resetuje stare połączenia
)

# -----------------------
# Session factory
# -----------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)