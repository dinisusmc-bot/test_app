"""
Configuration for Command & Control API.
"""

from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    """Application settings."""

    # App settings
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    APP_SECRET_KEY: str = "your-secret-key-here-change-in-production"

    # Database settings
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5433
    POSTGRES_DB: str = "geo_map_test"
    POSTGRES_USER: str = "openclaw"
    POSTGRES_PASSWORD: str = "openclaw_dev_pass"

    @property
    def DATABASE_URL(self) -> str:
        """Build database URL."""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # CORS settings - accept comma-separated string or JSON array
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        """Parse CORS origins from string."""
        try:
            return json.loads(self.CORS_ORIGINS)
        except json.JSONDecodeError:
            return [origin.strip() for origin in self.CORS_ORIGINS.split(',')]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
