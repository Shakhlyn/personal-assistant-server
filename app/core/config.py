from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",

        # Env vars are matched case-insensitively, so DEBUG and debug both work.
        case_sensitive=False,
    )

    APP_NAME: str = "Personal Assistant Server"

    # Default is False on purpose: the value that applies when nobody sets it is the value production gets.
    DEBUG: bool = False

    # --- database ---
    # psycopg3 ("+psycopg"), not psycopg2 — psycopg2 has no async support at all
    # and create_async_engine would refuse the URL outright.
    DATABASE_URL: SecretStr
    DB_ECHO: bool = False
    # Connections held open per worker process. The real ceiling is Postgres'
    # max_connections (100 by default) divided by however many workers you run.
    DB_POOL_SIZE: int = Field(default=5, ge=1, lt=50)
    DB_MAX_OVERFLOW: int = Field(default=10, ge=0, lt=50)
    # Recycle before a typical idle-connection reaper (pgbouncer, a load
    # balancer, Postgres' own idle_session_timeout) drops it under us.
    DB_POOL_RECYCLE_SECONDS: int = Field(default=1800, ge=60)

    # --- auth ---
    SECRET_KEY: SecretStr  # no default: the app must refuse to boot without it
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=15, ge=1)  # short — a JWT cannot be revoked
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=30, ge=1)  # long — but revocable, it lives in the DB
    JWT_ISSUER: str = "book-service"
    JWT_AUDIENCE: str = "book-api"


settings = Settings()  # type: ignore[call-arg]
