from fastapi import FastAPI

from config.db import init_db
from api import model
from api import warehouse


app = FastAPI()
app.include_router(model.router)
app.include_router(warehouse.router)


@app.on_event("startup")
async def initialize():
    """Startup event"""

    await init_db()
