import sys as _sys
from .exceptions import CloudException, NotFound
from .queue import Queue
from .bucket import Bucket
from .container import * 
from .function import Function, triggered_function
from .kvstore import * 

if __name__ != 'cloudpost' and 'cloudpost' not in _sys.modules:
    _sys.modules['cloudpost'] = _sys.modules[__name__]
    
class Api:
    def __init__(self, *args, **kwargs):
        pass
    
    def event(self, *args, **kwargs):
        pass
    
    def route(self, *args, **kwargs):
        return triggered_function(event = self.event(*args, **kwargs))
    
    def mount(self, path):
        return ApiMount(self)

class ApiMount:
    def __init__(self, api):
        self.api = api
        self.mounted = None
