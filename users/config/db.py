"""Database configuration"""

from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from .settings import settings

url = make_url(
    f"postgres+asyncpg://{settings.db_username}:{settings.db_password}@"
    + f"{settings.db_host}:{settings.db_port}/{settings.db_database}",
)

engine = create_async_engine(url, echo=True)

async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


Base = declarative_base()


def get_db_connection():
    """Get sessionmaker"""

    return async_session
