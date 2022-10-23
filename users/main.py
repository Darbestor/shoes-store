"""Entry point"""

from fastapi import FastAPI

from api import login


app = FastAPI()

app.include_router(login.router)
