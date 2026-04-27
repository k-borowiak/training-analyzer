from fastapi import FastAPI, Depends
from .auth_strava import router as strava_router
from .deps import get_current_user
from .models import User

app = FastAPI(title="Strava OAuth App (Phase 2)")

@app.on_event("startup")
def on_startup():
    print("STARTUP: zaczynam tworzyć tabele...")
    from .db import engine
    from .models import Base
    Base.metadata.create_all(bind=engine)
    print("STARTUP: tabele gotowe ✅")

app.include_router(strava_router)

@app.get("/")
def home():
    return {"ok": True, "how_to_login": "/auth/strava/login", "me": "/api/me"}

@app.get("/api/me")
def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "stravaAthleteId": user.strava_athlete_id}