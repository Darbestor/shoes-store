"""Users service api gateway"""

from fastapi import APIRouter, Request, status
from fastapi.responses import Response

from gateway_decorator import route
from config.settings import settings
from models.requests.login import LoginReq

# TODO Think about custom Router
# and generic decorators with neccessary gateway logic

router = APIRouter()


@route(
    request_method=router.post,
    path="/login",
    response_code=status.HTTP_201_CREATED,
    payload_key="login",
    service_url=settings.users_service_url,
    response_model="models.responses.login.LoginResponse",
)
async def login_gateway(login: LoginReq, request: Request, response: Response):
    pass
