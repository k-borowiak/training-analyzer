import os
from dotenv import load_dotenv

# .env może się przydać
load_dotenv()

def _get_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "yes", "y", "on")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

ENV = os.getenv("ENV", "dev")
COOKIE_SECURE = _get_bool("COOKIE_SECURE", default=False)

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID", "")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET", "")
STRAVA_REDIRECT_URI = os.getenv("STRAVA_REDIRECT_URI", "http://localhost:8000/auth/strava/callback")
STRAVA_SCOPE = os.getenv("STRAVA_SCOPE", "read,activity:read_all")

APP_REDIRECT_AFTER_LOGIN = os.getenv("APP_REDIRECT_AFTER_LOGIN", "/")
SESSION_SECRET = os.getenv("SESSION_SECRET", "change-me")
