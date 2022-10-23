"""Database configuration"""

from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker, registry
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from .settings import settings

url = make_url(
    f"postgres+asyncpg://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@"
    + f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}",
)

engine = create_async_engine(url, echo=True)

async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

orm_mapper = registry()


def get_db_connection():
    """Get sessionmaker"""

    return async_session
