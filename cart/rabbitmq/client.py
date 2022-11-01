from types import TracebackType
from typing import Optional, Type
import aio_pika
from aio_pika.pool import Pool, PoolItemContextManager
from aio_pika.abc import AbstractRobustConnection, AbstractChannel, AbstractQueue
from pydantic import BaseModel


from config.settings import settings


class RabbitMQClientFactory:
    connection: AbstractRobustConnection
    channel_pool: Pool
    publish_queue: AbstractQueue
    consume_queue: AbstractQueue

    @classmethod
    async def init(cls):
        cls.connection = await aio_pika.connect_robust(
            host=settings.rabbitmq_host,
            port=settings.rabbitmq_port,
            login=settings.rabbimq_username,
            password=settings.rabbitmq_password,
        )
        cls.channel_pool = Pool(cls.connection.channel, max_size=5)
        async with cls.channel_pool.acquire() as channel:
            cls.publish_queue = await channel.declare_queue("orders", durable=True)
            cls.consume_queue = await channel.declare_queue("cart", durable=True)

    @classmethod
    def get_client(cls, queue):
        if cls.connection.is_closed:
            raise Exception("Connection to RabbitMQ closed")
        return RabbitMQClient(cls.channel_pool.acquire(), queue)

    @classmethod
    async def close(cls):
        await cls.close()


class RabbitMQClient:
    def __init__(
        self, channel_pool: PoolItemContextManager, queue: AbstractQueue
    ) -> None:
        self.__pool = channel_pool
        self.queue = queue
        self._channel: AbstractChannel

    async def publish(self, body: BaseModel):
        return await self._channel.default_exchange.publish(
            aio_pika.Message(body=body.json(exclude_unset=True).encode("UTF-8")),
            routing_key=self.queue.name,
        )

    @property
    def channel(self):
        return self._channel

    async def __aenter__(self):
        self._channel = await self.__pool.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if self.__pool is not None:
            await self.__pool.__aexit__(exc_type, exc_val, exc_tb)
