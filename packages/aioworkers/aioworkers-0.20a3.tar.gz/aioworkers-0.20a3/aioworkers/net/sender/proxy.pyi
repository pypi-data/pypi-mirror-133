from aioworkers.core.base import AbstractWriter as AbstractWriter, LoggingEntity as LoggingEntity
from aioworkers.net.sender import AbstractSender as AbstractSender
from aioworkers.worker.base import Worker as BaseWorker
from typing import Any

class Facade(LoggingEntity, AbstractSender):
    async def init(self) -> None: ...
    async def send_message(self, msg) -> None: ...

class Worker(BaseWorker):
    async def init(self) -> None: ...
    async def run(self, value: Any | None = ...) -> None: ...
