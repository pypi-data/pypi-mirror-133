from cloudpost import depres
_ELEMENTS = {}

_CUR_MODULE = None


class Element:
    type: str
    name: str

    def __new__(cls, name=None, *args, **kwargs):
        if name and name in _ELEMENTS:
            obj = _ELEMENTS[name]
            obj._add_to_module()
        else:
            obj = object.__new__(cls)
            obj.__init__(name=name, *args, **kwargs)
            obj._register()
            obj._add_to_module()
            depres.create_entity(obj)

        return obj
    
    def _add_to_module(self):
        if _CUR_MODULE is not None:
            _CUR_MODULE.add_element(self)
        elif type(self) is not Module:
            raise Exception('no module defined atm')

    def _register(self):
        if self.name not in _ELEMENTS:
            _ELEMENTS[self.name] = self
        else:
            raise ValueError(f'"{self.name}" is already registered')

    def __str__(self):
        return f'<{self.__class__.__name__} {self.name}>'

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'


class Event:
    def _bind_to_function(self, fn):
        pass


class Module(Element):
    type = 'module'
    def __init__(self, name):
        self.name = name
        self.functions = []
        self.dependant_elements = []

    def add_element(self, elem):
        print(' ++ adding', elem, 'to', self)
        if type(elem) is Function:
            self.functions.append(elem)
            elem.module = self
            depres.add_dependency(elem, self)
        else:
            self.dependant_elements.append(elem)
            depres.add_dependency(self, elem)


class ApiRoute(Event):
    def __init__(self, api, path, methods, marshal):
        self.api = api
        self.methods = methods
        self.marshal = marshal
        self.path = path
        self.function = None
        self.mount = None

    def _bind_to_function(self, fn):
        if self.function is not None and self.function is not fn:
            raise ValueError('ApiRoute already bound to function')
        self.function = fn


class Queue(Element, Event):
    type = 'queue'

    def __init__(self, name):
        self.name = name
        self.subscribers = []

    def _bind_to_function(self, fn):
        self.subscribers.append(fn)


class Bucket(Element):
    type = 'storage'

    def __init__(self, name, *, location=None):
        self.name = name
        self.location = location


class KvStore(Element):
    type = 'kv_store'

    def __init__(self, name, location):
        self.name = name
        self.location = location


class Container(Element):
    type = 'container'

    def __init__(self, name, *, path=None, mount=None):
        self.name = name
        self.path = path
        self.mount = mount
        if mount:
            mount.mounted = self


class Function(Element):
    type = 'function'

    def __init__(self, name, *, event=None, events=None, function=None):
        self.name = name
        if event:
            if events:
                raise ValueError(
                    f'{self.name}: cannot specify both "event" and "events".')
            self.events = (event, )
        elif events:
            self.events = events
        else:
            self.events = ()

        for e in self.events:
            e._bind_to_function(self)

        self.function = function

    def __call__(self, *args, **kwargs):
        self.function(*args, **kwargs)


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


class ApiMount:
    def __init__(self, api):
        self.api = api
        self.mounted = None



class Api(Element):
    type = 'api'

    def __init__(self, name):
        self.name = name
        self.routes = []

    def event(self, path, *, methods=('GET', 'POST'), marshal=None):
        route = ApiRoute(self, path, list(methods), marshal=marshal)
        self.routes.append(route)
        return route

    def mount(self, *args, **kwargs):
        route = self.event(*args, **kwargs)
        route.mount = ApiMount(self)
        return route.mount


    def route(self, *args, **kwargs):
        return triggered_function(event=self.event(*args, **kwargs))


_EXPORTS = (
    Queue, KvStore, Container, Function, triggered_function, Api, Bucket
)


def _register_into_cloudpost():
    import cloudpost
    for item in _EXPORTS:
        setattr(cloudpost, item.__name__, item)
