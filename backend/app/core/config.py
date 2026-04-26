from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralne miejsce na konfigurację aplikacji.

    - w DEV możesz używać .env
    - w Docker/Prod konfiguruj przez ENV
    """
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- Core ---
    ENV: str = "dev"

    # --- Database ---
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@db:5432/postgres"

    # --- Strava OAuth (Phase 2) ---
    STRAVA_CLIENT_ID: str | None = None
    STRAVA_CLIENT_SECRET: str | None = None
    STRAVA_REDIRECT_URI: str | None = None
    STRAVA_SCOPES: str = "read,activity:read_all"  # możesz zmienić później

    # --- App session/security ---
    SESSION_SECRET: str = "change-me"  # w prod ZAWSZE z ENV


settings = Settings()