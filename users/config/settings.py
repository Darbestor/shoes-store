"""Service settings"""

import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Service settings"""

    DB_USERNAME: str | None = os.environ.get("DB_USERNAME")
    DB_PASSWORD: str | None = os.environ.get("DB_PASSWORD")
    DB_DATABASE: str | None = os.environ.get("DB_DATABASE")
    DB_HOST: str | None = os.environ.get("DB_HOST", "localhost")
    DB_PORT: int | None = int(os.environ.get("DB_PORT", 5432))


settings = Settings()
