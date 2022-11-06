from uuid import UUID
from fastapi import Depends
from models.db.models import OrderHistory
from models.requests.order_history import OrderReq
from repository.order_history import OrderHistoryRepository


class OrderHistoryService:
    def __init__(
        self,
        repo: OrderHistoryRepository = Depends(),
    ) -> None:
        self.__repo = repo

    async def add_order(self, payload: OrderReq) -> OrderHistory:
        """Add  user order to history

        Args:
            payload (OrderReq): payload

        Returns:
            OrderHistory: User's order history
        """

        return await self.__repo.add_order(payload.user_id, payload.order)

    async def get_history(self, user_id: UUID) -> OrderHistory:
        return await self.__repo.get_history(user_id)
