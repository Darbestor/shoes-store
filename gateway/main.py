"""Entry point"""
import json
import logging
import aiohttp
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from config.settings import settings
from network import init_session, destroy_session, make_request
from openapi import OpenAPIGatherer

logging.basicConfig(level=logging.INFO)

app = FastAPI()
if settings.environment == "Production":
    app.root_path = "/api"

app.openapi = lambda: OpenAPIGatherer.openapi(app)


@app.get("/")
def index():
    return {"message": "Gateway service"}


@app.api_route(
    "/{full_path:path}",
    methods=["get", "post", "put", "delete"],
    include_in_schema=False,
)
async def capture_routes(request: Request, full_path: str):

    method = request.method.lower()

    path = full_path.split("/")
    base_url = settings.service_map.get(path[0])
    if base_url is None:
        raise HTTPException(status_code=404)
    url = base_url + "/".join(path[1:])
    query = str(request.query_params)
    if len(query) > 0:
        url += "?" + query

    body = None
    form = None
    try:
        body = await request.json()
    except json.decoder.JSONDecodeError:
        form_data = await request.form()
        if form_data:
            form = dict(form_data)

    try:
        resp_data, status_code_from_service = await make_request(
            url=url, method=method, data=body, form_data=form
        )
    except aiohttp.client_exceptions.ClientConnectorError as ex:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is unavailable.",
        ) from ex
    except (aiohttp.client_exceptions.ContentTypeError, Exception) as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Service error.",
        ) from ex
    return JSONResponse(content=resp_data, status_code=status_code_from_service)


@app.on_event("startup")
async def initialize():
    """Startup event"""
    init_session(settings.timeout)
    await OpenAPIGatherer.gather_openapi()


@app.on_event("shutdown")
async def destroy():
    """Shutdown event"""

    await destroy_session()
