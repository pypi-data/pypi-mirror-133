import subprocess
import json
from typing import Tuple
import asyncio


class _result:
    def __init__(self, data):
        self.__dict__.update({k: _result(data[k]) if type(
            data[k]) is dict else data[k] for k in data})

    def __str__(self):
        return '<Result ' + ' '.join(f'{k}={v}' for k, v in self.__dict__.items()) + '>'


def _map_option(k, v):
    k = k.replace('_', '-')
    if v is True:
        return f'--{k}'
    else:
        return f'--{k}={v}'


class _command:
    def __init__(self, args):
        self.args = args

    async def __call__(self, *args, **kwargs) -> Tuple[_result, bool]:

        ignore_error = kwargs.pop('_ignore_error', False)
        ignore_errors = kwargs.pop('_ignore_errors', False)
        ignore_error = ignore_error or ignore_errors

        kwargs.setdefault('quiet', True)
        kwargs.setdefault('format', 'json')
        kws = [_map_option(k, v) for k, v in kwargs.items() if k[0] != '_']
        aa = self.args + list(args) + kws

        proc = await asyncio.create_subprocess_exec(
            'gcloud', *aa, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        stdout, stderr = await proc.communicate()

        if proc.returncode != 0 and not ignore_error:
            raise Exception(
                'Command finished with non-zero exit code: ' + stderr.decode())

        result = _result(json.loads(stdout)) if stdout else None

        return result, proc.returncode == 0

    def __getattr__(self, k):
        return _command(self.args + [k.replace('_', '-')])


def __getattr__(k):
    return _command([k.replace('_', '-')])
