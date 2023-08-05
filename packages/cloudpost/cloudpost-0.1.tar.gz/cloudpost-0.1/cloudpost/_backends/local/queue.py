
_QUEUES = {}
_TRIGGERS = {}


class Queue:
    def __init__(self, name: str):
        self.name = name
        _QUEUES.setdefault(name, {})

    def publish(self, message: bytes):
        if self.name in _TRIGGERS:
            for func in _TRIGGERS[self.name]:
                func(message)


def _register_trigger(name: str, func):
    q = _TRIGGERS.setdefault(name, [])
    q.append(func)


def _remove_trigger(name: str, func):
    q = _TRIGGERS.setdefault(name, [])
    if func in q:
        q.remove(func)
