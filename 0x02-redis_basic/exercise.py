#!/usr/bin/env python3

""" Redis Module:


"""

from functools import wraps
import redis
from typing import Union, Optional, Callable
from uuid import uuid4, UUID

def count_calls(method: Callable) -> Callable:
    """ Decorator for counting """

    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper for decorator """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper

def call_history(method: Callable) -> Callable:
    """ Decorator to store the history """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper for decorator functionality """

        input = str(args)
        self._redis.rpush(method.__qualname__ + ":outputs", output)

        return output

    return wrapper

def replay(fn: Callable):
    """ Display the history of calls """

    r = redis.Redis()
    f_name = fn.__qualname__
    n_calls = r.get(f_name)
    try:
        n_calls = n_calls.decode('utf-8')
    except Exception:
        n_calls = 0
    print(f'{f_name} was called {n_calls} times:')

    ins = r.lrange(f_name + ":inputs", 0, -1)
    outs = r.lrange(f_name + ":outputs", 0, -1)

    for i, o in zip(ins, outs):
        try:
            i = i.decode('utf-8')
        except Exception:
            i = ""
        try:
            o = o.decode('utf-8')
        except Exception:
            o = ""

        print(f'{f_name}(*{i}) -> {o}')


class Cache:
    """ Cache class """

    def __init__(self):
        """ Constructor """
        self._redis = redis.Redis()

