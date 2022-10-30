"""Database configuration"""

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from config.settings import settings
from models.db.catalog import Model, Warehouse


async def init_db():
    """Db client initialization"""

    # Create Motor client
    client = AsyncIOMotorClient(
        f"mongodb://{settings.db_username}:{settings.db_password}@{settings.db_host}:{settings.db_port}"
    )

    # Initialize beanie with the Product document class and a database
    await init_beanie(
        database=client[settings.db_database], document_models=[Model, Warehouse]
    )
