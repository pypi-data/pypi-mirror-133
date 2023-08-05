from google.api_core.exceptions import NotFound
from ._utils import client_with_project

import subprocess
import json 
from cloudpost import depres
from cloudpost.collector import Container


class GcpContainer:
    type = "gcp-container"

    def __init__(self, entity: Container, project):
        self.resource_name = entity.name
        self.name = entity.name
        self._cmp = client_with_project()
        self._location = 'europe-west1'
        self.path = entity.path
        self.url = None
        depres.add_dependency(entity, self)
    async def read(self):
        services = self._list_services()
        try:
            me = list((name, location, url) for name, location, url in services if name == self.resource_name)[0]
        except IndexError:
            self.url = None
        else:
            name, location, url = me 
            self.url = url
    def create(self):
        self._build_image(self.path, self.resource_name, self._cmp.project)
        self._create_service(self.resource_name, self._location, self._cmp.project, self.resource_name)
        services = self._list_services()
        for name, location, url in services:
            if name == self.resource_name:
                self.url = url
    def update(self, **kwargs):
        self.delete()
        self.create()

    def delete(self):
        self._delete_service(self.resource_name, self._location)
    def _list_services(self):
        process = subprocess.Popen(
            "gcloud run services list --platform=managed --format=json".split(" "),
            stdout = subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        info = json.loads(stdout)
        res = [] 
        for service in info:
            name = service["metadata"]["name"]
            url = service["status"].get("url", "")
            location = service["metadata"]["labels"]["cloud.googleapis.com/location"]
            res.append((name, location, url))
        return res 


    def _build_image(self, path, name, project):
        process = subprocess.Popen(
            ("gcloud builds submit --tag gcr.io/%s/%s" % (project, name)).split(),
            stdout = subprocess.PIPE,
            cwd=path
        )
        process.communicate()

    def _create_service(self, name, location, project, image):
        process = subprocess.Popen(
            [
                "gcloud",
                "run", 
                "deploy", 
                name, 
                "--platform=managed",
                "--port=8080", 
                "--allow-unauthenticated", 
                "--region=%s" % location,  
                "--image=gcr.io/%s/%s" % (project, image)
            ]
        )
        process.communicate()

    def _delete_service(self, name, location):
        process = subprocess.Popen([
            "gcloud", 
            "run", 
            "services",
            "delete", 
            "--quiet", 
            "--platform=managed", 
            "--region=%s" % location, 
            name
        ])
        return process.wait(timeout=3000)
    
    async def apply(self):
        if self.url is None:
            self.create()
        else:
            self.update()


@depres.register(provider='gcp', entity_type='container')
def _add_gcp_container(params):
    project = params['project']
    entity = params['entity']
    container = GcpContainer(entity, project)
    entity._gcp = container
    depres.create_entity(container)