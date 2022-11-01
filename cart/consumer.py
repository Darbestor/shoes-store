import asyncio
import aio_pika

from rabbitmq.client import RabbitMQClientFactory


async def process_message(
    message: aio_pika.abc.AbstractIncomingMessage,
) -> None:
    async with message.process():
        print(message.body)
        await asyncio.sleep(1)


async def main():
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
