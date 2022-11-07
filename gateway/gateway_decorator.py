import functools
from typing import Any, List

from importlib import import_module
from fastapi import Request, Response, HTTPException, status
import aiohttp

from network import make_request


def route(
    request_method,
    path: str,
    response_code: int,
    payload_key: str,
    service_url: str,
    post_processing_func: str = None,
    response_model: Any = None,
    response_list: bool = False,
):
    """
    it is an advanced wrapper for FastAPI router, purpose is to make FastAPI
    acts as a gateway API in front of anything
    Args:
        request_method: is a callable like (app.get, app.post and so on.)
        path: is the path to bind (like app.post('/api/users/'))
        status_code: expected HTTP(status.HTTP_200_OK) status code
        payload_key: used to easily fetch payload data in request body
        post_processing_func: does extra things once in-network service returns
        response_model: shows return type and details on api docs
        response_list: decides whether response structure is list or not
    Returns:
        wrapped endpoint result as is
    """

    # request_method: app.post || app.get or so on
    # app_any: app.post('/api/login', status_code=200, response_model=int)
    if response_model:
        response_model = import_function(response_model)
        # if response_list:
        #     response_model = List[response_model]

    app_any = request_method(
        path, status_code=response_code, response_model=response_model
    )

    def wrapper(f):
        @app_any
        @functools.wraps(f)
        async def inner(request: Request, response: Response, **kwargs):
            service_headers: dict = {}

            scope = request.scope

            method = scope["method"].lower()
            path = scope["path"]

            payload_obj = kwargs.get(payload_key)
            payload = payload_obj.dict() if payload_obj else {}

            url = f"{service_url}{path}"

            try:
                resp_data, status_code_from_service = await make_request(
                    url=url,
                    method=method,
                    data=payload,
                    headers=service_headers,
                )
            except aiohttp.client_exceptions.ClientConnectorError:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Service is unavailable.",
                )
            except aiohttp.client_exceptions.ContentTypeError:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Service error.",
                )

            if status_code_from_service != response_code:
                raise HTTPException(
                    status_code=status_code_from_service,
                    detail=resp_data,
                )
            if post_processing_func:
                post_processing_f = import_function(post_processing_func)
                resp_data = post_processing_f(resp_data)

            response.status_code = status_code_from_service
            return resp_data

    return wrapper


def import_function(method_path):
    module, method = method_path.rsplit(".", 1)
    mod = import_module(module)
    return getattr(mod, method, lambda *args, **kwargs: None)
