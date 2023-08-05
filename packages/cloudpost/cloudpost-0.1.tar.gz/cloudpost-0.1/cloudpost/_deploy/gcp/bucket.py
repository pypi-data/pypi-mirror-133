

from google.cloud.storage import bucket
from cloudpost import depres
from google.cloud import storage
from google.api_core.exceptions import NotFound, Forbidden
from cloudpost.collector import Bucket
from cloudpost.cli import CloudProject

class GcpEnvVars:
    type = "gcp-env-vars"

    def __init__(self):
        self.env = {}
        self.name = "GcpGlobalEnvVars"
    def add_env(self, name, val):
        self.env[name] = val 
    
    def add_envs(self, envs: dict):
        self.env = dict(**self.env, **envs)
    
    def get_env(self):
        return self.env


class GcpBucket:
    type = 'gcp.bucket'
    def __init__(self, project: CloudProject, entity: Bucket):
        self.resource_name = entity.name
        self.name = project.get_name() + "_" + entity.name
        self._location = 'europe-west1'
        self._bucket = None  
        depres.add_dependency(entity, self)
        self.env: GcpEnvVars = depres.get_or_create_named_entity("environment_variales", GcpEnvVars)
        depres.add_dependency(self.env, self)
    async def apply(self):
        if not self._bucket:
            self.create()
        else:
            self.update()
        self.add_env()
    def add_env(self):
        self.env.add_env(f'CP_BUCKET_{self.resource_name}', self.name)
    async def read(self):
        try:
            bucket = list(b for b in self.list_buckets() if b.name == self.name)[0]
        except IndexError:
            bucket = None
        self._bucket = bucket
    def create(self):
        self._bucket = self.create_bucket_class_location(self.name)
    def update(self, **kwargs):
        self.__dict__.update(kwargs)
    def delete(self):
        self.delete_bucket(self.name)

    def create_bucket_class_location(self, bucket_name):
        """Create a new bucket in specific location with storage class"""
        # bucket_name = "your-new-bucket-name"
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        bucket.storage_class = "STANDARD"
        new_bucket = storage_client.create_bucket(bucket, location=self._location)

        print(
            "Created bucket {} in {} with storage class {}".format(
                new_bucket.name, new_bucket.location, new_bucket.storage_class
            )
        )
        return new_bucket
    def list_buckets(self):
        """Lists all buckets."""
        storage_client = storage.Client()
        buckets = storage_client.list_buckets()
        return buckets
    def delete_bucket(self, bucket_name):
        """Deletes a bucket. The bucket must be empty."""
        # bucket_name = "your-bucket-name"
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        bucket.delete()
        print("Bucket {} deleted".format(bucket.name))
    
    def get_env(self):
        return {f'CP_BUCKET_{self.resource_name}':  self.name}


@depres.register(provider='gcp', entity_type='storage')
def _add_gcp_bucket(params):
    project = params['project']
    entity = params['entity']
    
    bucket = GcpBucket(project, entity)
    depres.create_entity(bucket)
