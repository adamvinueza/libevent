from libevent.event import Event


class PostHandler:
    def __init__(self, post_url: str): ...
    def send(self, evt: Event) -> None: ...
