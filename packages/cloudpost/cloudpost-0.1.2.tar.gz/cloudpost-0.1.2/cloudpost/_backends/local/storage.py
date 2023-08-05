
from cloudpost._backends.local.exceptions import CloudException


_BUCKETS = {}


class Bucket:
    name: str

    def __init__(self, name: str, location: str):
        self.name = name
        _BUCKETS.setdefault(name, {})

    def object(self, key: str):
        return Object(self.name, key)


class Object:
    def __init__(self, bucket: str, key: str):
        self._bucket = bucket
        self._key = key

    def download(self):
        if not self.exists():
            raise CloudException('Requested object does not exist')
        return _BUCKETS[self._bucket][self._key]

    def upload(self, data):
        if hasattr(data, 'read') and callable(data.read):
            data = data.read()
        if isinstance(data, str):
            data = data.encode()
        _BUCKETS[self._bucket][self._key] = data

    def exists(self):
        return self._key in _BUCKETS[self._bucket]

    def delete(self):
        del _BUCKETS[self._bucket][self._key]
