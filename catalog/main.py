from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from config.db import init_db
from api import model
from api import warehouse
from exceptions import DBException


app = FastAPI()
app.include_router(model.router)
app.include_router(warehouse.router)


@app.on_event("startup")
async def initialize():
    """Startup event"""

    await init_db()


@app.exception_handler(ValueError)
async def value_exception_handler(_: Request, exc: ValueError):
    return JSONResponse(
        status_code=422,
        content={exc.args[0]: exc.args[1]},
    )


@app.exception_handler(DBException)
async def db_exception_handler(_: Request, exc: DBException):
    return JSONResponse(status_code=400, content={"database": exc.args[0]})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={ex["loc"][1]: ex["msg"] for ex in exc.errors()},
    )
