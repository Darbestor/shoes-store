"""Manipulation of Model documents in database"""

from typing import Any, Mapping
from uuid import UUID

from beanie import WriteRules

from exceptions import DBException
from models.db.catalog import Model


class ModelRepository:
    """Repository"""

    async def add_model(self, model: Model) -> UUID:
        """Create new model

        Args:
            details (dict): payload

        Returns:
            UUID: id of new model or existed one
        """

        existing_model = await Model.find_one(
            Model.name == model.name,
            Model.details.company == model.details.company,
            Model.details.color == model.details.color,
            Model.details.gender == model.details.gender,
        )
        if existing_model is not None:
            raise DBException("Model with given parameters already exists")
        await model.insert(link_rule=WriteRules.WRITE)
        return model.id

    async def update_price(self, model_id: UUID, new_price: float):
        """Set new price for model

        Args:
            model_id (UUID): model identifier
            new_price (float): new price
        """
        model = await self.get_model_by_id(model_id)
        if model is None:
            raise DBException(f"Model {model_id} not found")
        model.price = new_price
        await model.save()

    async def update_model(
        self,
        model_id: UUID,
        name: str | None = None,
        desciption: str | None = None,
        details: dict | None = None,
    ):
        """update model fields

        Args:
            model_id (UUID): model identifier
            name(str): new name. Defaults to None
            description(str): new description. Defaults to None
            details (dict): new details
        """
        model = await self.get_model_by_id(model_id)
        if model is None:
            raise DBException(f"Model {model_id} not found")
        if details is not None:
            for key, value in details.items():
                setattr(model, key, value)

        if name is not None:
            if (
                await Model.find(
                    Model.name == name,
                    Model.details.company == model.details.company,
                    Model.details.color == model.details.color,
                    Model.details.gender == model.details.gender,
                ).count()
                > 0
            ):
                raise DBException(f"Model {name} already exists")
            model.name = name

        if desciption is not None:
            model.description = desciption

        await model.save()

    async def delete_model(self, model_id: UUID):
        """delete model

        Args:
            model_id (UUID): model identifier
        """
        model = await self.get_model_by_id(model_id)
        if model is None:
            raise DBException(f"Model {model_id} not found")
        await model.delete()

    async def get_models(self, limit: int | None = None, offset: int = 0):
        """Retrive all models using batches if needed

        Args:
            limit (int, optional): batch size. Defaults to None.
            offset (int, optional): skip quantity. Defaults to 0.
        """

        return await Model.all(
            skip=offset,
            limit=limit,
            sort="+name",
        ).to_list()

    async def get_model_by_id(self, model_id: UUID) -> Model | None:
        """Get model by id

        Args:
            model_id (UUID): model identifier

        Returns:
            Model | None: Model if found or None
        """
        return await Model.find(Model.id == model_id).first_or_none()

    async def get_models_by_filter(self, *args: Mapping[str, Any]):
        """Get models that fit search criteria

        Args:
            filter (ModelFilter): filters
        """

        return await Model.find(*args).sort("+name").to_list()
