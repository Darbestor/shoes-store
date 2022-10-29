"""Facade between db and request for Model document"""

from uuid import UUID, uuid4
from math import isclose
from fastapi import Depends

from exceptions import ValidationException
from models.db.catalog import Details, Model, Warehouse
from models.requests.model import CreateModelReq
from repository.model import ModelRepository


class ModelService:
    """Facade between db and request for Model document"""

    def __init__(self, repo: ModelRepository = Depends()) -> None:
        self.repo = repo

    async def create_model(self, payload: CreateModelReq) -> Model:
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

    async def set_price(self, model_id: UUID, price: float):
        """Update model's price

        Args:
            model_id (UUID): model identifier
            price (float): new price
        """
        if isclose(0, price) or price < 0:
            raise ValidationException("price cannot be less than or equal to zero")
        await self.repo.update_price(model_id, price)

    async def get_models(self, limit: int = None, offset: int = 0) -> list[Model]:
        """Get models ordered by name

        Args:
            limit (int, optional): batch size. Defaults to All models.
            offset (int, optional): skip size. Defaults to 0.

        Returns:
            list[Model]: list of models
        """
        if (limit is not None and limit < 0) or offset < 0:
            raise ValidationException("Limit or offset cannot be less than 0")
        return await self.repo.get_models(limit, offset)


# update_price update_model delete_model get_models get_model_by_id get_models_by_filter
