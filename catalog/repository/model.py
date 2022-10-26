"""Manipulation of Model documents in database"""

from uuid import UUID, uuid4

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
            size, quantity = model.sizes.popitem()
            if size not in existing_model.sizes:
                existing_model.sizes[size] = 0
            existing_model.sizes[size] += quantity
            await existing_model.save()
            return existing_model.id

        model.id = uuid4()
        await model.insert_one()
        return model.id
