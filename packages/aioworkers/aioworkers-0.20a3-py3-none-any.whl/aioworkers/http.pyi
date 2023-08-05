import abc
from typing import Any

class _URL(str, abc.ABC):
    def __init__(self, *args) -> None: ...
    @property
    def path(self): ...
    def __truediv__(self, other): ...

URL: Any
