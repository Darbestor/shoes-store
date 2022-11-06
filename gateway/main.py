"""Entry point"""
import logging
import aiohttp
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi

from config.settings import settings
from network import init_session, destroy_session, make_request
from openapi import OpenAPIGatherer
from router import GatewayRoute

logging.basicConfig(level=logging.INFO)

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Shoes store Gateway",
        version="1.0.0",
        description="Shoes store API for all services",
        routes=app.routes,
    )

    openapi_schema["paths"] = openapi_schema["paths"] | OpenAPIGatherer.paths
    openapi_schema["components"]["schemas"] = (
        openapi_schema["components"]["schemas"] | OpenAPIGatherer.components
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
app.router.route_class = GatewayRoute


@app.api_route("/{full_path:path}", methods=["get", "post", "put", "delete"])
async def capture_routes(request: Request, full_path: str):
    # TODO stopped here
    scope = request.scope

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
