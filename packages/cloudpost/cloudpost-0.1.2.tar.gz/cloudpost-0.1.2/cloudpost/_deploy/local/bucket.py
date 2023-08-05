import cloudpost
from ._localRunner import _register_function, _invoke_function
from ..._backends.local.queue import _register_trigger

from typing import BinaryIO, List
from cloudpost import depres
from cloudpost.cli import CloudProject
import os 


class LocalBucket:
    type = 'local.storage'

    def __init__(self, entity, project: CloudProject):
        self.name = f'local.storage.{entity.name}'
        self._entity = entity
        self._project = project
        self.path = os.path.join(project.get_root(), ".local_buckets", project.get_name(), project.get_stage(), entity.name)
        depres.add_dependency(entity, self)

    async def read(self):
        pass

    async def apply(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

@depres.register(provider='local', entity_type='storage')
def _local_create_storage_dependencies(params):
    entity = params['entity']
    project = params['project']
    bucket = LocalBucket(entity, project)
    depres.create_entity(bucket)
