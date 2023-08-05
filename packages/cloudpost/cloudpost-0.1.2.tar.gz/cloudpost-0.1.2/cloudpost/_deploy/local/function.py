from ._localRunner import _register_function, _invoke_function
from ..._backends.local.queue import _register_trigger

from typing import BinaryIO, List
from cloudpost import collector, depres



class LocalFunction:
    type = 'local.function'

    def __init__(self, entity, project):
        self.name = f'local.function.{entity.name}'
        self._entity = entity
        self._project = project
        self.env = {}
        depres.add_dependency(entity, self)

    async def read(self):
        pass

    async def apply(self):
        _register_function(self._entity, self.env)
        for trig in self._entity.events:
            if type(trig) == collector.Queue:
                _register_trigger(trig.name, self._entity.function)


@depres.register(provider='local', entity_type='function')
def _local_create_function_dependencies(params):
    entity = params['entity']
    project = params['project']
    func = LocalFunction(entity, project)
    depres.create_entity(func)
