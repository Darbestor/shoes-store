from uuid import UUID
from fastapi import APIRouter, Depends
from models.db.catalog import Warehouse

from models.requests.warehouse import WarehouseReq
from service.warehouse import WarehouseService


router = APIRouter(prefix="/warehouse", tags=["warehouse"])


@router.post("/{model_id}", response_model=Warehouse, status_code=201)
async def set_storage(
    model_id: UUID,
    payload: WarehouseReq = Depends(WarehouseReq.as_form),
    service: WarehouseService = Depends(),
):
    """Set size's quantity for model. Should be used only to fill database"""
    return await service.set_storage(model_id, payload)


@router.put("/{model_id}")
async def update_storage(
    model_id: UUID, payload: WarehouseReq, service: WarehouseService = Depends()
):
    await service.change_storage(model_id, payload)


@router.get("/{model_id}", response_model=Warehouse)
async def get_warehouse(model_id: UUID, service: WarehouseService = Depends()):
    return await service.get_warehouse(model_id)
