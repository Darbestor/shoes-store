"""Repository for interaction with login table in database"""

from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select


from config.db import get_db_connection
from models.db import Login


class LoginRepository:
    """Access to data in login table"""

    def __init__(
        self, session_factory: sessionmaker = Depends(get_db_connection)
    ) -> None:
        self.session_factory: sessionmaker = session_factory

    async def add_login(self, details: dict) -> UUID:
        """Insert new Login entry

        Args:
            details (dict): parameters

        Returns:
            bool: transaction status. True if inserted, False on error
        """

        async with self.session_factory() as session:  # type: ignore
            async with session.begin():
                login = Login(**details)
                session.add(login)
        return login.id  # type: ignore

    async def get_logins(self) -> list[Login]:
        """Get all logins.
        Ordered by username

        Returns:
            list[Login]: list of logins
        """

        async with self.session_factory() as session:  # type: ignore
            result = await session.execute(select(Login).order_by(Login.username))
            return result.scalars()

    async def get_login_by_id(self, login_id: UUID) -> Login | None:
        """Get login by id."""

        async with self.session_factory() as session:  # type: ignore
            result = await session.execute(select(Login).where(Login.id == login_id))
            return result.scalars().one_or_none()

    async def get_login_by_username(self, username: str) -> Login | None:
        """Get login by username."""

        async with self.session_factory() as session:  # type: ignore
            result = await session.execute(
                select(Login).where(Login.username == username)
            )
            return result.scalars().one_or_none()
