"""Login router"""

from uuid import UUID
from fastapi import APIRouter, Depends, status
from fastapi.responses import Response, JSONResponse


from models.requests import LoginReq
from models.responses.login import LoginResponse
from repository.login import LoginRepository
from services.login import LoginService

router = APIRouter(tags=["login"])


@router.post("/authorize", response_model=UUID)
async def authorize_user(req: LoginReq, service: LoginService = Depends()):
    """Authorize user

    Args:
        req (LoginReq): request payload

    Returns:
        UUID: user id if authorization successful
    """

    login_id = await service.authorize(req)
    if login_id is not None:
        return login_id
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": "Wrong username or password"},
    )


@router.post("/", status_code=201, response_model=LoginResponse)
async def register_user(req: LoginReq, service: LoginService = Depends()):
    """Add new user

    Args:
        req (LoginReq): request payload
        repo (LoginRepository, optional): repository.

    Returns:
        LoginReq: Login response with user id
    """

    return await service.add_login(req)


@router.get("/", response_model=list[LoginResponse])
async def get_users(repo: LoginRepository = Depends()):
    """Retrieve all logins

    Args:
        req (LoginReq): request payload
        repo (LoginRepository, optional): repository.
    """

    logins = await repo.get_logins()
    response = [LoginResponse(id=l.id, username=l.username) for l in logins]
    return response


@router.get("/{login_id}", response_model=LoginResponse)
async def get_user_by_id(login_id: UUID, repo: LoginRepository = Depends()):
    """Get login info by id

    Args:
        login_id (UUID): user identifier
        repo (LoginRepository, optional): repository
    """

    login = await repo.get_login_by_id(login_id)
    if login is not None:
        return LoginResponse(id=login.id, username=login.username)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
