from . import exceptions
from .queue import * 
from .storage import * 
import json 
from .container import *
from typing import * 
from .kvstore import * 
def triggered_function(name_or_function=None, *, event=None, events=None):
    if callable(name_or_function):
        # called as `@trigerred_function`
        # or not as a decorator at all
        return Function(name_or_function.__name__, event=event, events=events, function=name_or_function)
    else:
        # called as `@trigerred_function(...)`
        def _w(fn):
            return Function(name_or_function or fn.__name__, event=event, events=events, function=fn)
        return _w


class Api:
    def __init__(self, *args, **kwargs):
        pass
    
    def event(self, *args, **kwargs):
        pass
    
    def route(self, *args, **kwargs):
        return triggered_function(event = self.event(*args, **kwargs))
    def mount(self, *args, **kwargs):
        return ApiMount(self)



class Function:

    def __init__(self, name, *, event=None, events=None, function=None):
        self.name = name
        self.function = function

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def invoke(self, *args, **kwargs) -> Any:
        """Calls the cloud function synchronously."""
        import requests
        data = {
            'args': args,
            'kwargs': kwargs
        }

        resp = requests.post(self.url, json=data, headers={
            'x-cloudpost': '1',
            'x-cloudpost-reason': 'invoke'
        })

        if 'x-cloudpost-type' not in resp.headers:
            return resp.content

        typ = resp.headers['x-cloudpost-type']

        if typ == 'json':
            return json.loads(resp.content)
        elif typ == 'string':
            return resp.text
        elif typ == 'exception':
            raise CloudException(resp.text)
        else:
            raise TypeError('unknown cloudpost type: ' + typ)

class ApiMount:
    def __init__(self, api):
        self.api = api
        self.mounted = None
