from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

from app.core.logging import setup_logging
from app.core.db.session import SessionLocal

# init logging 
setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(title="Training Analyzer")


# -----------------------
# DB Dependency
# -----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------
# Health check
# -----------------------
@app.get("/health")
def health():
    logger.info("Health check called")
    return {"status": "ok"}


# -----------------------
# DB test endpoint
# -----------------------
@app.get("/db-health")
def db_health(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).scalar()

    return {
        "db": "ok",
        "result": result
    }