from uuid import UUID
from fastapi import APIRouter, Depends

from models.requests.warehouse import WarehouseReq
from service.warehouse import WarehouseService


router = APIRouter(prefix="/warehouse", tags=["warehouse"])


@router.put("/{model_id}")
async def update_storage(
    model_id: UUID, payload: WarehouseReq, service: WarehouseService = Depends()
):
    return await service.update_storage(model_id, payload)
