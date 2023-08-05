from . import access_logger as access_logger
from ...core.base import AbstractNamedEntity as AbstractNamedEntity
from ...http import URL as URL
from ..server import SocketServer as SocketServer
from .exceptions import HttpException as HttpException
from .protocol import Protocol as Protocol
from typing import Any

class WebServer(SocketServer, AbstractNamedEntity):
    def __init__(self, *args, **kwargs) -> None: ...
    request_factory: Any
    parser_factory: Any
    url: Any
    async def init(self) -> None: ...
    async def start(self) -> None: ...
    async def stop(self) -> None: ...
    async def handler(self, request) -> None: ...
