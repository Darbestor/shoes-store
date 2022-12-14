from uuid import UUID
from fastapi import APIRouter, Depends

from service.order import OrderHistoryService


router = APIRouter(tags=["order history"])


@router.get("/{user_id}")
async def get_order(user_id: UUID, service: OrderHistoryService = Depends()):
    return await service.get_history(user_id)
