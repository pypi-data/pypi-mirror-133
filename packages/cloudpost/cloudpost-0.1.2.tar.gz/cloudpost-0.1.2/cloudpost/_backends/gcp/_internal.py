"""
Required env:
 - CP_FUNCTION_NAME : name of the executing function
"""

from importlib import import_module
import os
import json
import logging
try:
    MODULE_NAME = os.environ['CP_FUNCTION_MODULE']
    FUNCTION_NAME = os.environ['CP_FUNCTION_NAME']
    EMTRY_MODULE = import_module(MODULE_NAME)
    ENTRY_FUNCTION = getattr(EMTRY_MODULE, os.environ['CP_FUNCTION_NAME'])
except:
    logging.error('Could not load entry function', exc_info=True)
    raise

def entry(request):
    try:
        # TODO unmarshal parameters as required, right now only passes the content as a string
        res = ENTRY_FUNCTION(request.get_data(as_text=True))
        # TODO marshal response if required
        return json.dumps(res)
    except Exception as ex:
        logging.error('Error while processing request', exc_info=True)
        return str(ex), 500