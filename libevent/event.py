import datetime
from typing import Any, Dict, Generator, Optional
from libevent.handler import Handler
import libevent.state as state
from contextlib import contextmanager
from libevent.fields import Fields
"""
ADAPTED FROM Event CLASS AT https://github.com/honeycombio/libhoney-py
"""


class Event(object):
    """A collection of fields to be sent via a client."""

    ELAPSED_MS_KEY: str = 'elapsedMs'

    def __init__(self,
                 data: Optional[Dict] = None,
                 fields: Fields = Fields(),
                 client: Optional[Handler] = None):
        """Constructor. Should be called only by libevent.new_event()."""
        self.client = client
        self._fields = Fields()
        if self.client:
            self._fields += self.client.fields
        if data is None:
            data = {}
        self._fields.add(data)
        self._fields += fields

    def __getitem__(self, key: str) -> Any:
        return self.fields()[key]

    def __delitem__(self, key: str) -> None:
        del(self.fields()[key])

    def __contains__(self, key: str) -> bool:
        return key in self._fields

    def add_field(self, key: str, value: Any) -> None:
        self.add({key: value})

    def add(self, data: Dict) -> None:
        self._fields.add(data)

    def fields(self) -> Dict:
        return self._fields.get_data()

    def send(self) -> None:
        if self.client is None:
            state.warn_uninitialized()
            return
        self.client.send(self)

    @contextmanager
    def timer(self, name: str = ELAPSED_MS_KEY) -> Generator:
        """timer is a context for timing (in milliseconds) a function call.
         Example:
             ev = Event()
             with ev.timer("database_dur_ms"):
                 do_database_work()
            will add a field (name, duration) indicating running time
            do_database_work()"""
        start = datetime.datetime.utcnow()
        yield
        duration = datetime.datetime.utcnow() - start
        self.add_field(name, round(duration.total_seconds() * 1000, 4))

    def __str__(self) -> str:
        return str(self._fields)

    def to_dict(self) -> dict:
        return self._fields.get_data()
