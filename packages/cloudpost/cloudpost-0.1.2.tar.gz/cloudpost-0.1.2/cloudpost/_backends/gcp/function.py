"""
Required env:
 - CP_FUNC_{name} : url to function = https://{region}-{project}.cloudfunctions.net/{name}

"""

from typing import Any
import os
import json

from .exceptions import CloudException


class Function:

    def __init__(self, name, *, event=None, events=None, function=None):
        self.name = name
        self.function = function
        self.url = os.environ[f'CP_FUNC_{self.name}']

    def __call__(self, *args, **kwargs) -> Any:
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

def triggered_function(name_or_function = None, *, event = None, events = None):
    if callable(name_or_function):
        # called as `@trigerred_function`
        # or not as a decorator at all
        return Function(name_or_function.__name__, event=event, events=events, function=name_or_function)
    else:
        # called as `@trigerred_function(...)`
        def _w(fn):
            return Function(name_or_function or fn.__name__, event=event, events=events, function=fn)
        return _w
