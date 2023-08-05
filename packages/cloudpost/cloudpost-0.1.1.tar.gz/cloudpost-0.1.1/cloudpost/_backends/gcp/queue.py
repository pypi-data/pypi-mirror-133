"""Queue module for GCP.

Requires env:
 - CP_QUEUE_{name}: queue topic

"""

import logging
import os
import json

from ._utils import exception_wrap

try:
    from google.cloud.pubsub import PublisherClient
except:
    pass

class Queue:
    _pub_client : 'PublisherClient' = None
    
    @staticmethod
    def _init_client():
        from google.cloud.pubsub import PublisherClient
        if not Queue._pub_client:
            Queue._pub_client = PublisherClient()
    
    def __init__(self, name):
        Queue._init_client()
        self._queue_name = os.environ[f'CP_QUEUE_{name}']
    
    @exception_wrap('Could not publish message')
    def publish(self, event, data):
        Queue._pub_client.publish(
            self._queue_name,
            json.dumps(data).encode(),
            event=event
        ).result()