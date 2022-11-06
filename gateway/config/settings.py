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
    catalog_service_url: str = ""
    cart_service_url: str = ""
    orders_service_url: str = ""
    order_history_service_url: str = ""

    @property
    def service_map(self):
        return {
            "users": self.users_service_url,
            "catalog": self.catalog_service_url,
            "cart": self.cart_service_url,
            "orders": self.orders_service_url,
            "order_history": self.order_history_service_url,
        }

    class Config:
        """settings configuration"""

        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "gateway_"


settings = Settings()
