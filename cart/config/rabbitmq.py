from typing import Any
import aio_pika
from aio_pika.pool import Pool
from aio_pika.abc import AbstractRobustConnection
from pydantic import BaseModel


from .settings import settings


class RabbitMQClient:
    connection: AbstractRobustConnection
    channel_pool: Pool
    publish_queue: str = "orders"
    consume_queue: str = "cart"

    async def publish(self, routing_key: str, body: BaseModel):
        async with RabbitMQClient.channel_pool.acquire() as channel:
            return await channel.default_exchange.publish(
                aio_pika.Message(body=body.json(exclude_unset=True).encode("UTF-8")),
                routing_key=routing_key,
            )

    @classmethod
    async def initialize(cls):
        cls.connection = await aio_pika.connect_robust(
            host=settings.rabbitmq_host,
            port=settings.rabbitmq_port,
            login=settings.rabbimq_username,
            password=settings.rabbitmq_password,
        )
        cls.channel_pool = Pool(cls.connection.channel, max_size=5)
        async with cls.channel_pool.acquire() as channel:
            await channel.declare_queue("orders", durable=True)
            await channel.declare_queue("cart", durable=True)

    @classmethod
    async def close(cls):
        await cls.close()
