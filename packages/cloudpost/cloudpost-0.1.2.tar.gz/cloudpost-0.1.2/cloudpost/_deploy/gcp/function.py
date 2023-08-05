import asyncio
import os
from zipfile import ZipFile
import google.api_core.exceptions
from google.api_core.retry import Retry, if_exception_type
from google.iam.v1.iam_policy_pb2 import SetIamPolicyRequest

from cloudpost import depres
from io import BytesIO

from ._utils import client_with_project

from google.cloud.functions_v1.services.cloud_functions_service.async_client import CloudFunctionsServiceAsyncClient
from google.cloud.functions_v1.types import CloudFunction
from google.api_core.exceptions import NotFound
from google.cloud.functions_v1.types.functions import EventTrigger, GenerateUploadUrlRequest, HttpsTrigger

from cloudpost._deploy.gcp.bucket import GcpEnvVars

import requests

import hashlib
import subprocess

def _get_zip_from_source(source: dict):
    io = BytesIO()
    zip = ZipFile(io, "w")
    _write_zip_from_source(source, "", zip)
    zip.close()
    io.seek(0)
    x = io.read()
    return x


def _write_zip_from_source(source: dict, path: str, zip: ZipFile):
    for f in source.keys():
        if isinstance(source[f], dict):
            _write_zip_from_source(source[f], os.path.join(path, f), zip)
        else:
            zip.writestr(os.path.join(path, f), source[f])


class GcpFunction:
    type = 'gcp.function'

    def __init__(self, entity, project, module_source):
        self.name = f'gcp.function.{entity.name}'
        self._entity = entity
        self._project = project
        self._module = entity.module
        self._msb = module_source
        self._project_id, _ = subprocess.Popen(["gcloud", "config", "get-value", "project"], stdout=subprocess.PIPE).communicate()
        self.global_env = depres.get_or_create_named_entity("environment_variales", GcpEnvVars)
        self._env = {
            'CP_FUNCTION_MODULE': entity.module.name,
            'CP_FUNCTION_NAME': entity.name,
            'CP_PROJECT_ID': self._project_id
        }
        entity._gcp = self
        depres.add_dependency(self, module_source)
        depres.add_dependency(self, self.global_env)
        depres.add_dependency(entity, self)

    async def read(self):
        self._client = CloudFunctionsServiceAsyncClient()
        self._cwp = client_with_project()
        self._location = 'projects/{}/locations/{}'.format(
            self._cwp.project,
            self._project.get_provider_location(),
        )
        self._full_name = '{}/functions/{}'.format(
            self._location,
            self._project.get_full_name(self._entity.name))
        self.url = 'https://{}-{}.cloudfunctions.net/{}'.format(
            self._project.get_provider_location(),
            self._cwp.project,
            self._project.get_full_name(self._entity.name)
        )
        
        try:
            self._cf = await self._client.get_function(name=self._full_name)
        except NotFound:
            self._cf = None
        self.global_env.add_env("CP_FUNC_%s" % self._entity.name, self.url)

    def _create_function(self):
        return CloudFunction(
            name=self._full_name,
            # source_archive_url=self._msb._url,
            source_upload_url=self._msb._url,
            entry_point='entry',
            environment_variables=dict(**self._env, **self.global_env.get_env()),
            runtime='python38',
            https_trigger=HttpsTrigger()
        )

    async def apply(self):
        if self._cf is None:
            # create new
            self._cf = self._create_function()
            oper = await self._client.create_function(
                location=self._location, function=self._cf,
                retry=Retry(deadline=100000000))
            self._cf = await oper.result(timeout=100000000)
        else:
            self._fresh = (
                self._msb._fresh
                or self._env != self._cf.environment_variables
            )

            if self._fresh:
                cf = self._create_function()
                oper = await self._client.update_function(function=cf, retry=Retry(deadline=100000000))
                self._cf = await oper.result(timeout=100000000)

        # TODO(bebic): add options for non-public functions
        # possibly automatically deduced
        # e.g. all API functions are public, others private by default
        # TODO(bebic): make this IAM policy into a separate entity so it
        # can be versionied / deployed along like everything else
        await self._client.set_iam_policy(request=dict(
            resource=self._full_name,
            policy=dict(
                bindings=[dict(
                    role='roles/cloudfunctions.invoker',
                    members=['allUsers']
                )]
            )
        ))


class GcpModuleSource:
    type = 'gcp.module_source'

    def __init__(self, module, project):
        self.name = f'gcp.module_source.{module.name}'
        self._module = module
        self._project = project
        self._cwp = client_with_project()
        # self._bucket = bucket
        self._location = project.get_provider_location()
        # depres.add_dependency(self, bucket)

    async def read(self):
        self._client = CloudFunctionsServiceAsyncClient()
        source = self._project.get_source(self._module.name)
        self._data = _get_zip_from_source(source)
        self._hash = hashlib.sha256(self._data).hexdigest()

    async def _upload_code(self, location):
        uu = await self._client.generate_upload_url(GenerateUploadUrlRequest(
            parent=location
        ))
        data = self._data
        if isinstance(data, str):
            data = data.encode()
        if isinstance(data, bytes):
            data = BytesIO(data)
        res = requests.put(uu.upload_url, data=data, headers={
            'content-type': 'application/zip',
            'x-goog-content-length-range': '0,104857600'
        })
        res.raise_for_status()
        return uu

    async def apply(self):
        location = 'projects/{}/locations/{}'.format(
            self._cwp.project,
            self._location
        )
        uu = await self._upload_code(location)
        self._url = uu.upload_url
        self._fresh = True


@depres.register(provider='gcp', entity_type='function')
def _create_function_dependencies(params):
    entity = params['entity']
    project = params['project']

    module = entity.module

    # module_source_bucket = depres.get_or_create_named_entity(
    #     'gcp.module_source_bucket', lambda: GcpModuleSourcesBucket(project)
    # )
    module_source = depres.get_or_create_named_entity(
        f'gcp.module_source.{module}',
        lambda: GcpModuleSource(module, project))

    func = GcpFunction(entity, project, module_source)
    depres.create_entity(func)
