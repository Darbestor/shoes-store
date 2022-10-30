from fastapi import FastAPI

from config.db import init_db


app = FastAPI()


@app.on_event("startup")
async def initialize():
    """Startup event"""

    await init_db()
