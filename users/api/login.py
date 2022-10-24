"""Login router"""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response


from models.requests import LoginReq
from models.responses.login import LoginResponse
from repository.login import LoginRepository

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/", status_code=201, response_model=LoginResponse)
async def register_user(req: LoginReq, repo: LoginRepository = Depends()):
    """Add new user

    Args:
        req (LoginReq): request payload
        repo (LoginRepository, optional): repository.

    Returns:
        LoginReq: Login response with user id
    """

    details = req.dict(exclude_unset=True)
    login_id = await repo.add_login(details)
    if login_id is not None:
        response = LoginResponse(id=login_id, username=req.username)
        return response
    raise HTTPException(status_code=500, detail="Fail to register user")


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
