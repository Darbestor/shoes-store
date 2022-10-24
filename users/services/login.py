"""Login service"""

from asyncpg import UniqueViolationError
from fastapi import Depends, HTTPException
from models.requests.login import LoginReq
from models.responses.login import LoginResponse
from repository.login import LoginRepository


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
        login_id = await self.repo.add_login(details)
        return LoginResponse(id=login_id, username=request.username)
