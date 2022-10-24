"""Entry point"""

from sqlalchemy.exc import IntegrityError
from asyncpg import UniqueViolationError
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from api import login


app = FastAPI()

app.include_router(login.router)


@app.exception_handler(IntegrityError)
async def integrity_db_exception_helper(_: Request, exc: IntegrityError):
    """Unique constraint in db exception handler"""

    internal_error = exc.orig.__cause__
    if isinstance(internal_error, UniqueViolationError):
        details = internal_error.detail
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=details)
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=exc.detail)


@app.exception_handler(Exception)
async def general_exception_helper(_: Request, exc: Exception):
    """General exception parser"""

    print(exc)
    return JSONResponse(status_code=500, content="Error encountered")
