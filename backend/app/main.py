from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from sqlalchemy import text

app = FastAPI(title="Training Analyzer")

@app.get("/db-health")
def db_health(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).scalar()
    return {"db": "ok", "result": result}