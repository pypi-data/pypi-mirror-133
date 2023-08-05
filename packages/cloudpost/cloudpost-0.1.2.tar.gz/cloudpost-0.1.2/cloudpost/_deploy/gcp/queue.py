from google.cloud import pubsub_v1
from google.api_core.exceptions import NotFound
from cloudpost.collector import Queue
from cloudpost import depres

from cloudpost._deploy.gcp.bucket import * 

from ._utils import client_with_project

class GcpQueue:
    type = "gcp-queue"

    def __init__(self, entity: Queue, project):
        self.resource_name = entity.name
        self.name = entity.name
        self._location = 'europe-west1'
        self._publisher = pubsub_v1.PublisherClient()
        self._topic = None
        depres.add_dependency(entity, self)
        self.env: GcpEnvVars = depres.get_or_create_named_entity("environment_variales", GcpEnvVars)
        depres.add_dependency(self.env, self)

    async def read(self):
        self._cmp = client_with_project()
        self._topic_path = self._publisher.topic_path(self._cmp.project, self.resource_name)
        try:
            self._topic = self._publisher.get_topic(topic=self._topic_path)
        except NotFound:
            self._topic = None
    
    async def apply(self):
        if self._topic is None:
            self.create()
            self.env.add_env("CP_QUEUE_%s" % self.name, self._topic_path)
        else:
            self.update()
            self.env.add_env("CP_QUEUE_%s" % self.name, self._topic_path)


    def create(self):
        self._topic = self._publisher.create_topic(request={"name": self._topic_path})
    def update(self, **kwargs):
        self.__dict__.update(kwargs)
    def delete(self):
        self._publisher.delete_topic(topic = self._topic_path)



@depres.register(provider='gcp', entity_type='queue')
def _add_gcp_queue(params):
    project = params['project']
    entity = params['entity']
    queue = GcpQueue(entity, project)
    depres.create_entity(queue)