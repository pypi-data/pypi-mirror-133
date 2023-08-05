

from cloudpost import depres

from . import _gcloud as gcloud
import requests
from base64 import b64decode
import yaml
import tempfile
import json


class GcpApi:
    type = 'gcp.api'

    def __init__(self, project, entity):
        self.name = f'gcp.api.{entity.name}'
        self._project = project
        self._entity = entity
        self._full_name = self._project.get_full_name(
            self._entity.name).replace('_', '-')
        depres.add_dependency(entity, self)
        entity._gcp_api = self

    async def read(self):
        self._state = await gcloud.api_gateway.apis.describe(self._full_name, _ignore_errors=True)

    async def apply(self):
        if self._state is None:
            await gcloud.api_dateway.apis.create(self._full_name)


GCP_API_CONFIG_NAME = 'api-config'


class GcpApiConfig:
    type = 'gcp.apic'

    def __init__(self, project, entity, api):
        self.name = f'gcp.apic.{entity.name}'
        self._project = project
        depres.add_dependency(self, api)
        depres.add_dependency(entity, self)
        self._api = api
        self._entity = entity
        entity._gcp_apic = self

    async def read(self):
        self._state, _ = await gcloud.api_gateway.api_configs.describe(GCP_API_CONFIG_NAME, api=self._api._full_name, _ignore_errors=True)
        if self._state:
            gcp_name = self._state.name
            token, _ = await gcloud.auth.print_access_token(_json=False)
            res = requests.get('https://apigateway.googleapis.com/v1/' + gcp_name + '?view=FULL&alt=json', headers={
                'authorization': f'Bearer {token.token}'
            })

            try:
                contents_b64 = res.json(
                )['openapiDocuments'][0]['document']['contents']
                contents = b64decode(contents_b64.encode())
                self._document = yaml.load(contents, Loader=yaml.SafeLoader)
            except Exception as ex:
                print(ex)
                self._document = None
        else:
            self._document = None

    async def apply(self):
        config = self._generate_config(self._api._full_name, self._entity)
        if self._state:
            if config == self._document:
                self._fresh = False
                return
            # need to re-deploy

            # we need to delete the gateway first
            # TODO(bebic): this would normaly require implementing full delition of resources,
            # which needs to go in the reverse order from creation. however we do not have
            # this implemented yet. so instead we just delete it here
            await self._gw.delete()
            await gcloud.api_gateway.api_configs.delete(GCP_API_CONFIG_NAME, api=self._api._full_name)

        await self._create_api_config(GCP_API_CONFIG_NAME, self._api._full_name, config)
        self._fresh = True

    async def _create_api_config(self, name, api_id, api_spec):
        with tempfile.NamedTemporaryFile('w+', suffix='.yml') as spec_file:
            yaml.dump(api_spec, spec_file)
            spec_file.flush()
            await gcloud.api_gateway.api_configs.create(name, api=api_id, openapi_spec=spec_file.name)

    def _generate_config(self, api_name, api):
        result = {
            'swagger': '2.0',
            'info': {
                'title': f'{api_name}',
                'version': '1.0.0'
            },
            'schemes': ['https'],
            'produces': ['application/json']
        }

        paths = {}

        for route in api.routes:
            cp = paths.setdefault(route.path, {})
            fn = route.function if route.function is not None else route.mount.mounted
            for method in route.methods:
                # TODO(bebic): maybe add request/response
                # format based on marshaling data/typing
                # right now it's just a smallest valid swagger doc
                cp[method.lower()] = {
                    'operationId': fn.name + '_' + method,
                    'x-google-backend': {
                        'address': fn._gcp.url
                    },
                    'responses': {
                        200: {
                            'description': 'success'
                        }
                    }
                }

        result['paths'] = paths

        return result


class GcpApiGateway:
    type = 'gcp.apigw'

    def __init__(self, project, entity, api, config):
        self.name = f'gcp.apigw.{entity.name}'
        self._project = project
        depres.add_dependency(self, api)
        depres.add_dependency(self, config)
        depres.add_dependency(entity, self)
        self._entity = entity
        entity._gcp_apigw = self
        self._full_name = self._project.get_full_name(
            self._entity.name + '-gw').replace('_', '-')
        self._api = api
        self._api_config = config
        config._gw = self

    async def delete(self):
        await gcloud.api_gateway.gateways.delete(
            self._full_name,
            location='europe-west1'
        )
        self._state = None

    async def read(self):
        self._state, _ = await gcloud.api_gateway.gateways.describe(
            self._full_name,
            location='europe-west1',
            _ignore_errors=True)

    async def apply(self):
        if self._state:
            if not self._api_config._fresh:
                return
            await gcloud.api_gateway.gateways.delete(self._full_name, location='europe-west1')
        res, _ = await gcloud.api_gateway.gateways.create(self._full_name, api=self._api._full_name, api_config=GCP_API_CONFIG_NAME, location='europe-west1')


@depres.register(provider='gcp', entity_type='api')
def _create_api_dependencies(params):
    entity = params['entity']
    proj = params['project']
    api = GcpApi(proj, entity)
    config = GcpApiConfig(proj, entity, api)
    gateway = GcpApiGateway(proj, entity, api, config)
    for path, event in entity.routes:
        if event.function:
            depres.add_dependency(api, event.function)
        elif event.mount:
            depres.add_dependency(api, event.mount.mounted)
    depres.create_entity(api)
    depres.create_entity(config)
    depres.create_entity(gateway)
