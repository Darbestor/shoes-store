from uuid import UUID
from fastapi import APIRouter, Depends

from models.requests.warehouse import WarehouseReq
from service.warehouse import WarehouseService


router = APIRouter(prefix="/warehouse", tags=["warehouse"])


@router.post("/{model_id}")
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


@router.get("/{model_id}")
async def get_warehouse(model_id: UUID, service: WarehouseService = Depends()):
    return await service.get_warehouse(model_id)
