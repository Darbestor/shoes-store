"""Facade between db and request for Model document"""

from uuid import UUID, uuid4
from fastapi import Depends
from models.db.catalog import Details, Model, Warehouse

from models.requests.model import CreateModelReq
from repository.model import ModelRepository


class ModelService:
    """Facade between db and request for Model document"""

    def __init__(self, repo: ModelRepository = Depends()) -> None:
        self.repo = repo

    async def create_model(self, payload: CreateModelReq) -> UUID:
        """Create new model.
        If model already exist, then update quantity for size

        Args:
            payload (CreateModelReq): request

        Returns:
            UUID: model identifier
        """
        model_id = uuid4()
        model = Model(
            id=model_id,
            name=payload.name,
            description=payload.description,
            price=0,
            storage=Warehouse(model_id=model_id, storage={}),  # type: ignore
            details=Details(
                sport_type=payload.sport_type,
                company=payload.company,
                collection=payload.collection,
                color=payload.color,
                gender=payload.gender,
            ),
        )
        return await self.repo.add_model(model)
