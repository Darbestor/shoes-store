from types import TracebackType
from typing import Optional, Type
import aio_pika
from aio_pika.abc import AbstractQueue, AbstractConnection, AbstractChannel
from aio_pika.pool import Pool, PoolItemContextManager
from pydantic import BaseModel


from config.settings import settings


class RabbitMQClientFactory:
    initialized: bool = False
    connection: AbstractConnection
    channel_pool: Pool
    queues: list[AbstractQueue] = []

    @classmethod
    async def init(cls, queues: list[str]):
        cls.connection = await aio_pika.connect_robust(
            host=settings.rabbitmq_host,
            port=settings.rabbitmq_port,
            login=settings.rabbimq_username,
            password=settings.rabbitmq_password,
        )
        cls.channel_pool = Pool(cls.connection.channel, max_size=5)
        async with cls.channel_pool.acquire() as channel:
            for q in queues:
                cls.queues.append(await channel.declare_queue(q, durable=True))
        cls.initialized = True

    @classmethod
    def get_client(cls, queue: str):
        if not cls.initialized:
            raise RuntimeError("Initialize class with init() before using any methods")
        if cls.connection.is_closed:
            raise Exception("Connection to RabbitMQ closed")
        declared_queue = next((q for q in cls.queues if q.name == queue), None)
        if declared_queue is None:
            raise ValueError(f"RabbitMQ queue '{queue}' is not declared")
        return RabbitMQClient(cls.channel_pool.acquire(), declared_queue)

    @classmethod
    async def shutdown(cls):
        await cls.shutdown()


class RabbitMQClient:
    def __init__(
        self, channel_pool: PoolItemContextManager, queue: AbstractQueue
    ) -> None:
        self.__pool = channel_pool
        self.queue = queue
        self._channel: AbstractChannel

    async def publish(self, key: str, body: BaseModel):
        return await self._channel.default_exchange.publish(
            aio_pika.Message(
                body=body.json(exclude_unset=True).encode("UTF-8"),
                content_type="application/json",
                content_encoding="base64",
                type=key,
            ),
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
