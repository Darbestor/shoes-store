from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from config.db import init_db
from exceptions import DBException


app = FastAPI()


@app.on_event("startup")
async def initialize():
    """Startup event"""

    await init_db()


@app.exception_handler(DBException)
async def db_exception_handler(_: Request, exc: DBException):
    return JSONResponse(status_code=400, content={"database": exc.args[0]})
