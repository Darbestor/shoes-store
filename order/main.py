from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from config.db import init_db

from exceptions import DBException
from rabbitmq.client import RabbitMQClientFactory

app = FastAPI()


@app.on_event("startup")
async def initialize():
    """Startup event"""

    await init_db()
    await RabbitMQClientFactory.init(queues=["orders", "cart", "order_history"])


@app.on_event("shutdown")
async def destroy():

    await RabbitMQClientFactory.shutdown()


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
