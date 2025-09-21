# src/settings.py
import os
from urllib.parse import quote_plus

def env(name: str, default: str | None = None) -> str | None:
    """Safe getenv with default"""
    return os.getenv(name, default)

def database_url() -> str:
    """
    Build the database URL from environment variables.
    Local: host=localhost
    Docker Compose: set host to 'db'
    """
    user = env("POSTGRES_USER", "appuser")
    password = quote_plus(env("POSTGRES_PASSWORD", "secretpassword") or "")
    host = env("POSTGRES_HOST", "localhost")  # In compose, this would be 'db'
    port = env("POSTGRES_PORT", "5432")
    dbname = env("POSTGRES_DB", "appdb")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

APP_ENV = env("APP_ENV", "dev")
APP_HOST = env("APP_HOST", "0.0.0.0")
APP_PORT = int(env("APP_PORT", "8000"))
