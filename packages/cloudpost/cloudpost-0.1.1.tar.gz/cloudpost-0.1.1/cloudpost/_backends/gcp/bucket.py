"""

Requires env:
 - CP_BUCKET_{name}: namespaced bucket name
"""

import os
from typing import Iterable, List, Union

from ._utils import exception_wrap
from . import exceptions

try:
    from google.cloud.storage import Client
    from google.cloud.exceptions import NotFound
except:
    pass


class Bucket:

    _client: "Client" = None

    @staticmethod
    def _init_client():
        from google.cloud.storage import Client
        Bucket._client = Client()

    def __init__(self, name, **kwargs):
        self._init_client()
        self._name = os.environ[f'CP_BUCKET_{name}']
        self._bucket = Bucket._client.bucket(self._name)

    @exception_wrap('Error while putting blob content')
    def put(self, file_name: str, file_content: Union[str, bytes]) -> None:
        blob = self._bucket.blob(file_name)
        blob.upload_from_string(file_content)

    @exception_wrap('Error while getting blob content')
    def get(self, file_name: str) -> bytes:
        blob = self._bucket.blob(file_name)
        return blob.download_as_bytes()

    @exception_wrap('Error while getting blob content')
    def get_text(self, file_name: str) -> str:
        blob = self._bucket.blob(file_name)
        try:
            return blob.download_as_text()
        except NotFound as nf:
            raise exceptions.NotFound(file_name) from nf

    @exception_wrap('Error while deleting blob content')
    def delete(self, file_name: str) -> None:
        blob = self._bucket.blob(file_name)
        blob.delete()

    @exception_wrap('Error while checking blob existance')
    def exists(self, file_name: str) -> None:
        blob = self._bucket.blob(file_name)
        return blob.exists()

    @exception_wrap('Error while listing bucket contents')
    def list_folder(self, prefix: str = '') -> Iterable[str]:
        prefix = prefix.strip('/') + '/'
        return (x.name for x in self._bucket.list_blobs(prefix=prefix))
