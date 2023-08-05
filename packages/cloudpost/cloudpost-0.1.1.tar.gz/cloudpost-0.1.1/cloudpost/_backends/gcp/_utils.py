from functools import update_wrapper
from .exceptions import CloudException

def exception_wrap(message: str = 'An exception occurred'):
    def _make_wrapper(func):
        def _wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as err:
                raise CloudException(message) from err
        return update_wrapper(_wrapper, func)
    return _make_wrapper