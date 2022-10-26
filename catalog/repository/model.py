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
            new_size = model.available_sizes.pop()
            available_size = next(
                (x for x in existing_model.available_sizes if x.size == new_size.size),
                None,
            )
            if available_size is None:
                existing_model.available_sizes.append(new_size)
            else:
                available_size.quantity += new_size.quantity
            await existing_model.save()
            return existing_model.id

        await model.insert()
        return model.id


# fd6f5a30-68b3-4c00-bd93-c6829cb921ca
