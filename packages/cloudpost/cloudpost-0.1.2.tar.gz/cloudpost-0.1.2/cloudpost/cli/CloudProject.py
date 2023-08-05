

from pprint import pprint
from cloudpost.cli.FileAccess import FileAccess
from cloudpost import collector

import yaml
import os
import sys

import importlib
import asyncio


async def async_print(*args):
    print(*args)


class CloudProject:
    def create_project(workspace: str, name: str, fa: FileAccess = FileAccess()):
        fa.change_directory(workspace)
        fa.make_directory("src")
        fa.make_directory("resources")
        fa.make_directory("lib")
        fa.write_file("config.yml", yaml.dump({
            "name": name,
            "provider": "gcp"
        }))

    def __init__(self, path: str, fa: FileAccess = FileAccess()):
        self.fa = fa
        self.root = os.path.abspath(path)
        self.fa.change_directory(path)
        if set(["src", "lib"]) < set(self.fa.list_directory(".")):
            functions = self.fa.list_directory("src")
            libraries = ["lib"]

            self.functions = functions
            self.resources = []
            self.deployable = libraries
            self.config = yaml.load(self.fa.read_file(
                "config.yml"), yaml.SafeLoader)
            if not isinstance(self.config, dict):
                raise ValueError()
            if not (set(["name", "provider"]) <= set(self.config.keys())):
                raise ValueError(
                    "Project does not contain sufficient parameters (i.e. name and provider in config.yml)")
        else:
            self.functions = []
            self.resources = []
            self.deployable = []
            raise ValueError("Not valid project")

    def get_full_name(self, name, sep='-'):
        return sep.join([self.get_name(), self.get_stage(), name])

    def run_module(self, module_name, full_path):
        importlib.import_module(module_name)

    def collect(self):
        collector._register_into_cloudpost()
        lib_path = "lib"
        sys.path.append(lib_path)
        src_path = "src"
        sys.path.append(src_path)

        for module in self.fa.list_directory("src"):
            mod_obj = collector.Module(module)
            collector._CUR_MODULE = mod_obj
            self.run_module(module, os.path.join(src_path, module))
            collector._CUR_MODULE = None
            
            for lib_item in self.fa.list_directory(lib_path):
                for k in sys.modules:
                    if k == lib_item or k.startswith(lib_item + '.'):
                        del sys.modules[k]

        sys.path.remove(lib_path)
        sys.path.remove(src_path)

    def get_resources(self, resource_type=None):
        if resource_type is not None:
            return list(name for name, e in self.collect().items() if e.type == resource_type)
        else:
            return list(name for name, e in self.collect().items())

    def read_resource(self, resource_name):
        return yaml.safe_load(self.fa.read_file(os.path.join("resources", resource_name + ".yml")))

    def get_functions(self):
        elements = self.collect()
        return list(name for name, e in elements.items() if e.type == "function")

    def get_deployable(self):
        return self.deployable

    def get_buckets(self):
        return self.get_resources("storage")

    def get_containers(self):
        return self.get_resources("container")

    def get_kvstores(self):
        return self.get_resources("kv_store")

    def get_queues(self):
        return self.get_resources("queue")

    def get_apis(self):
        return self.get_resources("api")

    def get_name(self):
        return self.config["name"]

    def get_provider(self):
        return self.config["provider"]

    def get_stage(self):
        return self.config.get("stage", "default")

    def get_source(self, resource_name: str):
        runner_code = """
from cloudpost._internal import entry
"""
        s = {
            **self._get_sources("lib"),
            resource_name: self._get_sources(os.path.join("src", resource_name)),
            "main.py": runner_code,
            "cloudpost": self._get_sources(
                os.path.join(self.fa.get_cloudpost_path(),
                             "_backends", self.get_provider())
            ),
            "requirements.txt": self._get_requirements(
                os.path.join("src", resource_name),
                "lib",
                os.path.join(self.fa.get_cloudpost_path(),
                             "_backends", self.get_provider())
            )
        }
        return s
    
    def _get_requirements(self, *paths):
        res = ["google-cloud-datastore"]
        for path in paths:
            req_path = os.path.join(path, "requirements.txt")
            if self.fa.isfile(req_path):
                data = self.fa.read_file(req_path)
                res.extend(data.splitlines(False))
        
        return '\n'.join(res)

    def get_resource(self, resource_name):
        elements = self.collect()
        try:
            result = {
                "name": resource_name,
                "type": elements[resource_name].type,
                "module": elements[resource_name].module
            }
            if elements[resource_name].type == "function":
                result = dict(
                    **result, **self.read_function(elements[resource_name]))
            return result
        except KeyError:
            return None

    def _get_sources(self, path: str):
        if self.fa.isfile(path):
            return self.fa.read_file(path)
        elif self.fa.isdir(path):
            return {k: self._get_sources(os.path.join(path, k)) for k in self.fa.list_directory(path)}
        else:
            raise RuntimeError(
                "Symbolic links in source files for functions and containers are not supported right now: {}".format(path))

    def get_root(self):
        return self.root

    def read_function(self, element):
        return {
            "events": list(element.events)
        }

    def get_provider_location(self):
        return 'europe-west1'
