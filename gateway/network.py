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
    url: str,
    method: str,
    data: dict | None = None,
    form_data: dict | None = None,
    headers: dict | None = None,
):
    """
    Args:
        url: is the url for one of the in-network services
        method: is the lower version of one of the HTTP methods: GET, POST, PUT, DELETE # noqa
        data: json payload. Data and form_data cannot be used at the same time
        form_data: url encoded form data. Data and form_data cannot be used at the same time
        headers: is the header to put additional headers into request
    Returns:
        service result coming / non-blocking http request (coroutine)
    """
    request = getattr(SESSION, method)
    async with request(url=url, json=data, data=form_data, headers=headers) as response:
        data = await response.json()
        return (data, response.status)
