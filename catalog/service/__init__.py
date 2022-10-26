"""Model service"""


from uuid import UUID


class ModelService:
    """Middleware between db and requests for Model document"""

    async def create_model(self, payload: ModelReq) -> UUID:
        pass
