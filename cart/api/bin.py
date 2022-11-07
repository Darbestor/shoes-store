from uuid import UUID
from fastapi import APIRouter, Depends

from models.requests.bin import BinReq
from service.cart import BinService


router = APIRouter(tags=["cart"])


@router.post("/{user_id}")
async def submit_bin(user_id: UUID, service: BinService = Depends()):
    return await service.submit_bin(user_id)


@router.delete("/{user_id}")
async def clear_bin(user_id: UUID, service: BinService = Depends()):
    return await service.clear_bin(user_id)


@router.get("/{user_id}")
async def get_bin(user_id: UUID, service: BinService = Depends()):
    return await service.get_bin(user_id)


@router.post("/{user_id}/{item_id}")
async def add_item(req: BinReq, service: BinService = Depends()):
    return await service.add_item(req)


@router.delete("/{user_id}/{item_id}")
async def remove_item(req: BinReq, service: BinService = Depends()):
    return await service.remove_item(req)
