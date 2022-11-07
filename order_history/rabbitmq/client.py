from datetime import datetime
import importlib
import logging
from types import TracebackType
from typing import Optional, Type
import aio_pika
from aio_pika.abc import AbstractQueue, AbstractConnection, AbstractChannel
from aio_pika.pool import Pool, PoolItemContextManager
from pydantic import BaseModel

from config.settings import settings
from rabbitmq.message_handlers.base import HandlerBase


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
            for queue in queues:
                cls.queues.append(await channel.declare_queue(queue, durable=True))
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
        self._channel: AbstractChannel | None = None

    async def publish(self, key: str, body: BaseModel):
        logging.info(
            "Sending message '%s' to '%s' with key '%s'", body, self.queue, key
        )
        return await self.channel.default_exchange.publish(
            aio_pika.Message(
                body=body.json(exclude_unset=True).encode("UTF-8"),
                content_type="application/json",
                type=key,
                timestamp=datetime.utcnow(),
            ),
            routing_key=self.queue.name,
        )

    async def consume_handler(self, message: aio_pika.IncomingMessage):
        async with message.process(ignore_processed=True):
            try:
                logging.info(
                    """New message:
    type: %s
    message: %s""",
                    message.type,
                    message.body,
                )
                if message.type is None:
                    raise AttributeError()
                module_name, class_name = message.type.rsplit(".", 1)
                class_name = class_name.capitalize()
                class_ = getattr(
                    importlib.import_module(f"rabbitmq.message_handlers.{module_name}"),
                    class_name,
                )
                handler: HandlerBase = class_(message)
                await handler.handle()
                logging.info("Message processed successfully")
            except (ImportError, AttributeError):
                logging.error("Wrong message type: %s", message.type)
                await message.nack()
            except Exception as ex:
                logging.error("Error in processing message: %s", ex)
                await message.reject()

    @property
    def channel(self):
        if self._channel is None:
            raise ConnectionError(
                "Channel is not opened.\nClient should be used is 'async with' context."
            )
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
