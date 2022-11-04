from uuid import UUID
from fastapi import APIRouter, Depends
from models.requests.order_history import OrderInfoReq

from service.order import OrderHistoryService


router = APIRouter(prefix="/order", tags=["order"])


@router.post("/{order_id}")
async def confirm_order(
    request: OrderInfoReq, service: OrderHistoryService = Depends()
):
    return await service.confirm_order(request)


@router.delete("/{order_id}/change")
async def change_order(order_id: UUID, service: OrderHistoryService = Depends()):
    """Cancel order and return items to cart"""

    await service.change_order(order_id)


@router.delete("/{order_id}")
async def delete_order(order_id: UUID, service: OrderHistoryService = Depends()):
    await service.delete_order(order_id)


@router.get("/list/{user_id}")
async def get_user_orders(user_id: UUID, service: OrderHistoryService = Depends()):
    return await service.get_user_orders(user_id)


@router.get("/{order_id}")
async def get_order(order_id: UUID, service: OrderHistoryService = Depends()):
    return await service.get_order(order_id)
