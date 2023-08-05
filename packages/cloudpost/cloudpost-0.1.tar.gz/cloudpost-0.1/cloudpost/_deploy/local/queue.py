import cloudpost
from ._localRunner import _register_function, _invoke_function
from ..._backends.local.queue import _register_trigger

from typing import BinaryIO, List
from cloudpost import depres
from cloudpost.cli import CloudProject
import os 


class LocalQueue:
    type = 'local.queue'

    def __init__(self, entity, project: CloudProject):
        self.name = f'local.queue.{entity.name}'
        self._entity = entity
        self._project = project
        depres.add_dependency(entity, self)

    async def read(self):
        pass

    async def apply(self):
        pass
@depres.register(provider='local', entity_type='queue')
def _local_create_queue_dependencies(params):
    entity = params['entity']
    project = params['project']
    queue = LocalQueue(entity, project)
    depres.create_entity(queue)
