import os
from dotenv import load_dotenv

load_dotenv()

def _get_bool(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "y", "on")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/strava_app")

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID", "")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET", "")
STRAVA_REDIRECT_URI = os.getenv("STRAVA_REDIRECT_URI", "http://localhost:8000/auth/strava/callback")

APP_REDIRECT_AFTER_LOGIN = os.getenv("APP_REDIRECT_AFTER_LOGIN", "/")

COOKIE_SECURE = _get_bool("COOKIE_SECURE", default=False)

# Scope zmienić później
STRAVA_SCOPE = os.getenv("STRAVA_SCOPE", "read,activity:read_all")

print("CONFIG DATABASE_URL =", DATABASE_URL)