from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- Core ---
    ENV: str = "dev"

    # --- Database ---
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@db:5432/postgres"

    # --- Strava OAuth (Phase 2) ---
    STRAVA_CLIENT_ID: str | None = None
    STRAVA_CLIENT_SECRET: str | None = None
    STRAVA_REDIRECT_URI: str | None = None
    STRAVA_SCOPES: str = "read,activity:read_all"  

    # --- App session/security ---
    SESSION_SECRET: str = "change-me"  


settings = Settings()
