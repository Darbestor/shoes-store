import asyncio

from rabbitmq.client import RabbitMQClientFactory
from rabbitmq.types import QueueName
from config.db import init_db


async def main():
    await init_db()
    await RabbitMQClientFactory.init(queues=[e.value for e in QueueName])
    async with RabbitMQClientFactory.get_client(QueueName.ORDERS) as client:
        await client.channel.set_qos(10)

        await client.queue.consume(client.consume_handler)

        try:
            # Wait until terminate
            await asyncio.Future()
        finally:
            await RabbitMQClientFactory.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
