"""Login router"""

from fastapi import APIRouter, Depends


from models.requests import LoginReq
from repository.login import LoginRepository

router = APIRouter(prefix="/login", tags=["login"])

# @router.post("/")
# async def register_user(req: LoginReq, repo: LoginRepository = Depends()):
#     try:
#         details = req.dict(exclude_unset=True)
#         if await repo.add_login(details) is True:
#             return
