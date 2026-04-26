import os

DATABASE_URL = os.getenv("DATABASE_URL")

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")