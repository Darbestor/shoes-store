"""Login router"""

from fastapi import APIRouter, Depends, HTTPException


from models.requests import LoginReq
from repository.login import LoginRepository

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/", status_code=201)
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
        req.id = login_id
        return req
    raise HTTPException(status_code=500, detail="Fail to register user")
