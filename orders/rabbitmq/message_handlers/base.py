from abc import ABC, abstractmethod

from aio_pika import IncomingMessage


class HandlerError(Exception):
    pass


class HandlerBase(ABC):
    def __init__(self, message: IncomingMessage):
        self._message = message

    @abstractmethod
    async def handle(self):
        if self._message.content_type != "application/json":
            raise HandlerError(
                f"Invalid content type: \
                    Expected 'accplication/json', \
                    Actual {self._message.content_type}"
            )
        if self._message.content_encoding is not None:
            raise HandlerError("Encoded message is not supported")
