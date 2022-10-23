"""Service settings"""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Service settings"""

    db_username: str = ""
    db_password: str = ""
    db_database: str = ""
    db_host: str = ""
    db_port: int = 5432

    class Config:
        """settings configuration"""

        env_file = ".env_local"
        env_file_encoding = "utf-8"


settings = Settings()
