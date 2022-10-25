"""Service settings"""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Service settings"""

    db_username: str = ""
    db_password: str = ""
    db_database: str = ""
    db_host: str = ""
    db_port: int = 5432
    timeout: float = 59.0
    users_service_url: str = ""

    class Config:
        """settings configuration"""

        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "gateway_"


settings = Settings()
