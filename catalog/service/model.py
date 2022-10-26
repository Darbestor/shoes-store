"""Facade between db and request for Model document"""

from uuid import UUID, uuid4
from fastapi import Depends
from models.db.catalog import Details, Model

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

        model = Model(
            id=uuid4(),
            name=payload.name,
            description=payload.description,
            price=0,
            sizes={payload.size, payload.quantity},
            details=Details(
                sport_type=payload.sport_type,
                company=payload.company,
                collection=payload.collection,
                color=payload.collection,
                gender=payload.gender,
            ),
        )
        return await self.repo.add_model(model)
