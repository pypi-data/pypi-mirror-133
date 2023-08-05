from ..core.base import ExecutorEntity as ExecutorEntity
from ..core.formatter import FormattedEntity as FormattedEntity
from .base import AbstractQueue as AbstractQueue

class ProxyQueue(ExecutorEntity, AbstractQueue):
    def __init__(self, *args, **kwargs) -> None: ...
    async def init(self) -> None: ...
    def set_queue(self, queue) -> None: ...
    async def get(self): ...
    async def put(self, value): ...

class PipeLineQueue(FormattedEntity, ExecutorEntity, AbstractQueue):
    def __init__(self, *args, **kwargs) -> None: ...
    def set_reader(self, reader) -> None: ...
    def set_writer(self, writer) -> None: ...
    async def get(self): ...
    async def put(self, value): ...
