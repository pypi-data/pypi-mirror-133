
import subprocess
from sys import stdout
from google.cloud import datastore
import os 

def create_client(project_id):
    return datastore.Client(project_id)

class KvStore:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self._project_id = os.environ["CP_PROJECT_ID"]
        self.client = create_client(self._project_id)
    
    def create(self, data):
        key = self.client.key(self.name)
        entity = datastore.Entity(key)

        # Apply new field values and save the Task entity to Datastore
        entity.update(data)
        self.client.put(entity)
        return entity.key
    
    def update(self, key, data):
        with self.client.transaction():
            key = self.client.key(self.name, key)
            # Use that key to load the entity
            entity = self.client.get(key)
            if not entity:
                raise ValueError(f"Task {key} does not exist.")
            for k,v in data.items():
                entity[k] = v
            # Persist the change back to Datastore
            self.client.put(entity)

    def delete(self, key):
        key = self.client.key(self.name, key)
        self.client.delete(key)
    
    def list(self):
        return list(self.client.query(kind=self.name).fetch())