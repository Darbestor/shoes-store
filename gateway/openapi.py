import asyncio
import logging
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from config.settings import settings
from network import make_request

gathererLogger = logging.getLogger("OpenAPIGatherer")


class OpenAPIGatherer:
    """Microservices API collector"""

    _paths: dict | None = None
    _components: dict | None = None
    openapi_schema: dict | None = None

    @classmethod
    async def gather_openapi(cls):
        """Gather and merge api definitions from all confired in settings microservices"""

        tasks = []
        for name, url in settings.service_map.items():
            tasks.append(cls._get_service_api(url, name))

        openapi_list = await asyncio.gather(
            *tasks,
            return_exceptions=True,
        )
        cls._paths, cls._components = cls._merge_schemas(openapi_list)

    @classmethod
    async def _get_service_api(cls, url: str, tag=None):
        # TODO test when service unavailable
        openapi = await make_request(url + "openapi.json", "get")
        return openapi[0], tag

    @classmethod
    def _merge_schemas(cls, openapi_list):
        openapi_paths = {}
        openapi_components = {}
        for api, prefix in openapi_list:
            for method, definition in api["paths"].items():
                method = f"/{prefix}{method}"
                openapi_paths[method] = definition
            for _type, definition in api["components"]["schemas"].items():
                if _type in openapi_components:
                    gathererLogger.warning(
                        "%s is already presented in openapi components", _type
                    )
                else:
                    openapi_components[_type] = definition
        return openapi_paths, openapi_components

    @classmethod
    def openapi(cls, base_app: FastAPI):
        if cls.openapi_schema:
            return cls.openapi_schema

        gathererLogger.info("Constructing openapi schema")
        openapi_schema = get_openapi(
            title="Shoes store Gateway",
            version="1.0.0",
            description="Shoes store API for all services",
            routes=base_app.routes,
        )
        if "paths" in openapi_schema:
            openapi_schema["paths"] = openapi_schema["paths"] | cls._paths
        else:
            openapi_schema["paths"] = cls._paths

        components: dict = {"schemas": {}}
        if "components" in openapi_schema:
            components = openapi_schema["components"]
        else:
            openapi_schema["components"] = components

        components["schemas"] = components["schemas"] | cls._components

        cls.openapi_schema = openapi_schema
        return cls.openapi_schema
