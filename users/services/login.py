"""Login service"""

from uuid import UUID
from fastapi import Depends
from models.requests.login import LoginReq
from models.responses.login import LoginResponse
from repository.login import LoginRepository
from security import get_password_hash, verify_password


class LoginService:
    """Middleware between db"""

    def __init__(self, repo: LoginRepository = Depends()):
        self.repo = repo

    async def add_login(self, request: LoginReq):
        """Add new login

        Args:
            request (LoginReq): request payload

        Returns:
            LoginResponse: response model
        """
        details = request.dict(exclude_unset=True)
        details["passphrase"] = bytes(
            get_password_hash(request.password), encoding="utf-8"
        )
        del details["password"]

        login_id = await self.repo.add_login(details)
        return LoginResponse(id=login_id, username=request.username)

    async def authorize(self, request: LoginReq) -> UUID | None:
        """Check user in database and verify password

        Args:
            request (LoginReq): request

        Returns:
            UUID: user identifier if authorization successful
        """

        login = await self.repo.get_login_by_username(request.username)
        if login is not None and verify_password(request.password, login.passphrase):
            return login.id

        return None
