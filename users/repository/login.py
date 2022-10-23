"""Repository for interaction with login table in database"""

from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import sessionmaker

from config.db import get_db_connection
from models.db import Login
from models.requests.login import LoginReq


class LoginRepository:
    """Access to data in login table"""

    def __init__(
        self, session_factory: sessionmaker = Depends(get_db_connection)
    ) -> None:
        self.session_factory: sessionmaker = session_factory

    async def add_login(self, details: dict) -> UUID | None:
        """Insert new Login entry

        Args:
            details (dict): parameters

        Returns:
            bool: transaction status. True if inserted, False on error
        """

        try:
            async with self.session_factory() as session:  # type: ignore
                async with session.begin():
                    passphrase = bytes(details["password"], encoding="utf-8")
                    login = Login(username=details["username"], passphrase=passphrase)
                    session.add(login)
            return login.id
        except Exception as ex:
            print(ex)
            return None
