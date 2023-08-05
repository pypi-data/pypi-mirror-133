
import random 
import base64

class KvStore:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.data = {}
    
    def create(self, data):
        key = base64.b64encode(random.randbytes(10))
        self.data[str(key)] = {
            "id": str(key),
            **data
        }
        return str(key)
    
    def update(self, key, data):
        for k,v in data:
            self.data[key][k] = v

    def delete(self, key):
        del self.data[key]
    def list(self):
        return list(self.data.values())