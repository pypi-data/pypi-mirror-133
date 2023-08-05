from ...core.formatter import registry as registry
from .exceptions import HttpException as HttpException
from typing import Any

class Request:
    url: Any
    method: Any
    headers: Any
    transport: Any
    context: Any
    content_length: Any
    def __init__(self, url, method, *, body_future: Any | None = ..., headers=..., transport: Any | None = ..., context: Any | None = ...) -> None: ...
    def read(self): ...
    def response(self, data: Any | None = ..., status: int = ..., reason: str = ..., format: Any | None = ..., headers=...): ...
