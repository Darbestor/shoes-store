"""External requests methods"""

import aiohttp


SESSION: aiohttp.ClientSession


def init_session(timeout):
    global SESSION
    timeout_client = aiohttp.ClientTimeout(timeout)
    SESSION = aiohttp.ClientSession(timeout=timeout_client)


async def destroy_session():
    if SESSION is not None:
        await SESSION.close()


async def make_request(
    url: str, method: str, data: dict | None = None, headers: dict | None = None
):
    """
    Args:
        url: is the url for one of the in-network services
        method: is the lower version of one of the HTTP methods: GET, POST, PUT, DELETE # noqa
        data: is the payload
        headers: is the header to put additional headers into request
    Returns:
        service result coming / non-blocking http request (coroutine)
    """
    if data is None:
        data = {}

    request = getattr(SESSION, method)
    async with request(url=url, json=data, headers=headers) as response:
        data = await response.json()
        return (data, response.status)
