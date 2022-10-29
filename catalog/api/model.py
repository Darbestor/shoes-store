"""Model endpoints"""

from uuid import UUID
from fastapi import APIRouter, Depends
from models.db.catalog import Model

from models.requests.model import ModelReq
from service.model import ModelService


router = APIRouter(prefix="/model", tags=["model"])


@router.post("/", response_model=Model, status_code=201)
async def create_model(
    req: ModelReq = Depends(ModelReq.as_form), service: ModelService = Depends()
):
    return await service.create_model(req)


@router.put("/{model_id}")
async def update_model(
    model_id: UUID, details: ModelReq, service: ModelService = Depends()
):
    return await service.update_model(model_id, details)


@router.put("/{model_id}/price")
async def update_price(model_id: UUID, price: float, service: ModelService = Depends()):
    await service.set_price(model_id, price)


@router.delete("/{model_id}")
async def delete_model(model_id: UUID, service: ModelService = Depends()):
    await service.delete_model(model_id)


@router.get("/", response_model=list[Model])
async def get_models(
    limit: int | None = None, offset: int = 0, service: ModelService = Depends()
):
    return await service.get_models(limit, offset)


@router.get("/{model_id}", response_model=Model)
async def get_model_by_id(model_id: UUID, service: ModelService = Depends()):
    return await service.get_model_by_id(model_id)
