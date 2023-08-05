import asyncio

_DEPRES_CALLBACKS = []
_COMMON_PARAMS = {}

async def done_future(x): return x

def _set_common_params(**kwargs):
    _COMMON_PARAMS.update(kwargs)


def register(fn=None, **kwargs):
    if fn is not None:
        _DEPRES_CALLBACKS.append((fn, kwargs))
        return fn
    else:
        return lambda fn: register(fn, **kwargs)


def _check_params(args, params):
    for kw, val in args.items():
        if val != params.get(kw, None):
            return False
    return True


def _call_depres_callbacks(params):
    cbs = _DEPRES_CALLBACKS.copy()
    for fn, args in cbs:
        if _check_params(args, params):
            fn(params)


_ENTITIES = []
_DEPENDENCIES = {}
_ENT_NAMES = {}


def create_entity(ent):
    _ENTITIES.append(ent)
    _DEPENDENCIES.setdefault(ent, [])
    _call_depres_callbacks(
        {**_COMMON_PARAMS, 'entity_type': ent.type, 'entity': ent}
    )
    return ent

def get_named_entity(name):
    return _ENT_NAMES.get(name)

def get_or_create_named_entity(name, creator):
    if name in _ENT_NAMES:
        return _ENT_NAMES[name]
    else:
        e = create_entity(creator())
        _ENT_NAMES[name] = e
        return e


def add_dependency(dependant, depends_on):
    _DEPENDENCIES.setdefault(dependant, []).append(depends_on)

import logging

async def topological_invoke(callback):
    remaining = set(_ENTITIES.copy())
    completed = set()
    task_to_ent = {}
    cur_running = set()
    errored = set()
    while remaining:
        to_run = set()
        for x in remaining.copy():
            if all(dep in completed for dep in _DEPENDENCIES[x]):
                to_run.add(x)
                remaining.remove(x)

        if not to_run and not cur_running:
            if errored:
                raise Exception('errors ocurred')
            raise Exception('cyclic dependency found: ' + str(remaining))

        for x in to_run:
            aw = callback(x)
            if not hasattr(aw, '__await__'):
                aw = done_future(aw)
            cur_running.add(aw)
            task_to_ent[aw] = x

        done, pending = await asyncio.wait(cur_running, return_when=asyncio.FIRST_COMPLETED)
        cur_running = pending

        for d in done:
            if d.exception():
                ent = task_to_ent[d.get_coro()]
                logging.error(f'error while deploying entity {ent}', exc_info=d.exception())
                errored.add(task_to_ent[d.get_coro()])
            else:
                completed.add(task_to_ent[d.get_coro()])
