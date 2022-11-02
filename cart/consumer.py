import asyncio
import aio_pika

from rabbitmq.client import RabbitMQClientFactory
from config.db import init_db


def consumer(func):
    async def inner1(message: aio_pika.IncomingMessage, *args, **kwargs):

        await func(message, *args, **kwargs)

    return inner1


async def process_message(
    message: aio_pika.IncomingMessage,
) -> None:
    async with message.process():
        print(message.body)
        # await message.ack()


async def main():
    await init_db()
    await RabbitMQClientFactory.init()
    async with RabbitMQClientFactory.get_client(
        RabbitMQClientFactory.consume_queue
    ) as client:
        await client.channel.set_qos(10)

        await client.queue.consume(process_message)

        try:
            # Wait until terminate
            await asyncio.Future()
        finally:
            await RabbitMQClientFactory.close()


if __name__ == "__main__":
    asyncio.run(main())
