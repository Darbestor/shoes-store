"""Entry point"""

import aiohttp
from fastapi import FastAPI, Request

from settings import settings

app = FastAPI()


@app.middleware("http")
async def gateway(request: Request, call_next):
    """Gateway"""
    response = await call_next(request)


SESSION: aiohttp.ClientSession | None = None


@app.on_event("startup")
def initialize():
    """Startup event"""

    global SESSION
    timeout = aiohttp.ClientTimeout(settings.GATEWAY_TIMEOUT)
    SESSION = aiohttp.ClientSession(timeout=timeout)


@app.on_event("shutdown")
async def destroy():
    """Shutdown event"""

    if SESSION is not None:
        await SESSION.close()
