from uuid import UUID
from fastapi import Depends
from config.rabbitmq import RabbitMQClient
from models.db.models import Bin
from models.requests.bin import BinReq
from repository.bin import BinRepository


class BinService:
    def __init__(
        self,
        repo: BinRepository = Depends(),
        rabbitmq_client: RabbitMQClient = Depends(),
    ) -> None:
        self.__repo = repo
        self.__rabbitmq_client = rabbitmq_client

    async def add_item(self, request: BinReq) -> Bin:
        """Add item to bin

        Args:
            request (BinReq): payload

        Returns:
            Bin: Bin instance
        """

        return await self.__repo.add_item(**request.dict())

    async def remove_item(self, request: BinReq) -> Bin:
        """Remove item from bin completly or decrease quantity

        Args:
            request (BinReq): payload

        Returns:
            Bin: Bin instance
        """

        return await self.__repo.remove_item(**request.dict())

    async def submit_bin(self, user_id: UUID):
        """Send bin items to order service and clear bin

        Args:
            user_id (UUID): user identifier
        """

        # TODO send RabbitMQ message to create order
        bin_ = await self.__repo.remove_bin(user_id)

        test = await self.__rabbitmq_client.publish(
            self.__rabbitmq_client.publish_queue, bin_
        )
        print(test)

    async def clear_bin(self, user_id: UUID):
        """Clear bin

        Args:
            user_id (UUID): user identifier
        """

        await self.__repo.remove_bin(user_id)

    async def get_bin(self, user_id: UUID) -> Bin:
        """Get bin items

        Args:
            user_id (UUID): user identifier

        Returns:
            Bin: Bin instance
        """

        return await self.__repo.get_bin(user_id)
