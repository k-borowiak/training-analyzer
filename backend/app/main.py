from fastapi import FastAPI
from .api.v1.router import router as api_v1_router
from .routes.auth_strava import router as strava_auth_router
from .core.db.base import Base
from .core.db.session import engine

app = FastAPI(title="Training Analyzer")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {
        "ok": True,
        "health": "/api/v1/health",
        "me": "/api/v1/me",
        "strava_login": "/auth/strava/login",
        "strava_athlete": "/api/v1/strava/athlete",
        "strava_activities": "/api/v1/strava/activities"
    }

app.include_router(strava_auth_router)
app.include_router(api_v1_router, prefix="/api/v1")