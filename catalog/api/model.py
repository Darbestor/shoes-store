"""Model endpoints"""

from uuid import UUID
from fastapi import APIRouter, Depends

from models.requests.model import CreateModelReq
from service.model import ModelService


router = APIRouter(prefix="/model")


@router.post("/", response_model=UUID, status_code=201)
async def create_model(req: CreateModelReq, service: ModelService = Depends()):
    return await service.create_model(req)
