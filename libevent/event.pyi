# event.pyi

from typing import Any, Dict, Generator, Optional
from libevent.client import Client
from contextlib import contextmanager
from libevent.fields import Fields

class Event:
    def __init__(
        self,
        data: Optional[Dict] = None,
        fields: Fields = Fields(),
        client: Optional[Client] = None) -> None: ...
    def __getitem__(self, key: str) -> Any: ...
    def __contains__(self, key: str) -> bool: ...
    def add_field(self, key: str, value: Any) -> None: ...
    def add(self, data: Dict) -> None: ...
    def fields(self) -> Dict: ...
    def send(self) -> None: ...
    def timer(self, name: str) -> Generator: ...
    def __str__(self) -> str: ...
    def to_dict(self) -> dict: ...
