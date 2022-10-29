"""Model endpoints"""

from fastapi import APIRouter, Depends
from models.db.catalog import Model

from models.requests.model import CreateModelReq
from service.model import ModelService


router = APIRouter(prefix="/model")


@router.post("/", response_model=Model, status_code=201)
async def create_model(req: CreateModelReq, service: ModelService = Depends()):
    return await service.create_model(req)


@router.get("/", response_model=list[Model])
async def get_models(
    limit: int | None = None, offset: int = 0, service: ModelService = Depends()
):
    return await service.get_models(limit, offset)
