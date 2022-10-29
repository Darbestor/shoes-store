"""Facade between db and request for Model document"""

from uuid import UUID, uuid4
from math import isclose
from fastapi import Depends
from varname import nameof

from exceptions import ValidationException
from models.db.catalog import Details, Model, Warehouse
from models.requests.model import ModelReq
from repository.model import ModelRepository


class ModelService:
    """Facade between db and request for Model document"""

    def __init__(self, repo: ModelRepository = Depends()) -> None:
        self.__repo = repo

    async def create_model(self, payload: ModelReq) -> Model:
        """Create new model.
        If model already exist, then update quantity for size

        Args:
            payload (ModelReq): request

        Returns:
            UUID: model identifier
        """
        model_id = uuid4()
        model = Model(
            id=model_id,
            name=payload.name,
            description=payload.description,
            price=0,
            storage=Warehouse(model_id=model_id, storage=[]),  # type: ignore
            details=Details(
                sport_type=payload.sport_type,
                company=payload.company,
                collection=payload.collection,
                color=payload.color,
                gender=payload.gender,
            ),
        )
        return await self.__repo.add_model(model)

    async def update_model(self, model_id: UUID, payload: ModelReq) -> Model:
        """Update model information

        Args:
            model_id (UUID): model identifier
            payload (ModelReq): new details

        Returns:
            Model: Updated model
        """
        details = payload.dict(exclude_unset=True)
        name = details.pop(nameof(payload.name))
        description = details.pop(nameof(payload.description))
        return await self.__repo.update_model(
            model_id, name=name, desciption=description, details=details
        )

    async def set_price(self, model_id: UUID, price: float):
        """Update model's price

        Args:
            model_id (UUID): model identifier
            price (float): new price
        """
        if isclose(0, price) or price < 0:
            raise ValidationException("price cannot be less than or equal to zero")
        await self.__repo.update_price(model_id, price)

    async def delete_model(self, model_id: UUID):
        """Delete model by id

        Args:
            model_id (UUID): model identifier
        """
        await self.__repo.delete_model(model_id)

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
        return await self.__repo.get_models(limit, offset)

    async def get_model_by_id(self, model_id: UUID) -> Model | None:
        """Get model by id

        Args:
            model_id (UUID): model identifier

        Returns:
            Model | None: Model if found or None
        """
        return await self.__repo.get_model_by_id(model_id)


# TODO get_models_by_filter
