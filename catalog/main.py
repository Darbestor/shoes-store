from fastapi import FastAPI

from config.db import init_db
from api import model


app = FastAPI()
app.include_router(model.router)


@app.on_event("startup")
async def initialize():
    """Startup event"""

    await init_db()
