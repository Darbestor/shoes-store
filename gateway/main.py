"""Entry point"""

from fastapi import FastAPI

from config.settings import settings
from api import users
from network import init_session, destroy_session

app = FastAPI()
app.include_router(users.router)


@app.on_event("startup")
def initialize():
    """Startup event"""

    init_session(settings.timeout)


@app.on_event("shutdown")
async def destroy():
    """Shutdown event"""

    await destroy_session()
