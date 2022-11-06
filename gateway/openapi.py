import asyncio
import logging

from config.settings import settings
from network import make_request

gathererLogger = logging.getLogger("OpenAPIGatherer")


class OpenAPIGatherer:
    """Microservices API collector"""

    paths: dict | None = None
    components: dict | None = None

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
        cls.paths, cls.components = cls._merge_schemas(openapi_list)

    @classmethod
    async def _get_service_api(cls, url: str, tag=None):
        openapi = await make_request(f"{url}/openapi.json", "get")
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
