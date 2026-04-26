from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

from app.core.db.deps import get_db

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
def health():
    logger.info("Health check called")
    return {"status": "ok"}


@router.get("/db-health")
def db_health(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).scalar()
    return {"db": "ok", "result": result}