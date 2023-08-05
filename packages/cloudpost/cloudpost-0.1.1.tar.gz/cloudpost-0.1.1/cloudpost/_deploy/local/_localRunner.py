import sys
import os
import importlib
from cloudpost import collector
APP = None
_REGISTRATIONS = {}
_ENV = {}


def _register_function(entity, env: dict):
    _REGISTRATIONS[entity.name] = {"entity": entity}
    _ENV[entity.name] = env


def _invoke_function(name, data):
    if name in _REGISTRATIONS:
        entity = _REGISTRATIONS[name]["entity"]
        collector._CUR_MODULE = collector.Module(entity.module.name)
        mm = _initialize_module(entity)
        result = getattr(mm, entity.name)(data)
        collector._CUR_MODULE = None
        return result


def _initialize_module(entity):
    print("Initializing function module {}".format(entity.name))
    path = 'src.{}'.format(entity.module.name)

    if path in sys.modules:
        return importlib.import_module(path)
    for k, v in _ENV.get(entity.name, {}).items():
        os.environ[k] = v
    current_cloudpost = sys.modules["cloudpost"]
    sys.modules['cloudpost'] = sys.modules['cloudpost._backends.local']
    mm = importlib.import_module(path)
    sys.modules["cloudpost"] = current_cloudpost

    for k in _ENV.get(entity.name, {}).keys():
        del os.environ[k]

    return mm


def initialize(project):
    global APP
    from flask import Flask, request
    import cloudpost._backends.local

    sys.modules['cloudpost.sdk'] = sys.modules['cloudpost._backends.local']
    sys.path.append(project.get_root())
    sys.path.append(os.path.join(project.get_root(), 'lib'))
    
    print(sys.path)

    APP = Flask(__name__)

    @APP.route('/func/<name>/event', methods=['POST'])
    def func_event(name: str):
        _invoke_function(name, request.get_json())
        return 'OK'


def start_listener():
    from werkzeug import run_simple
    run_simple('localhost', 8080, APP, use_debugger=True, use_evalex=True)
