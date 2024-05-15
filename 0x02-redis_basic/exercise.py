#!/usr/bin/env python3
"""exercise module"""
import uuid
from typing import Union, Callable, Any
from functools import wraps
import redis


def count_calls(method: Callable) -> Callable:
    '''Tracks the number of calls made to a method in a Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Invokes the given method after incrementing its call counter.
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    '''Tracks the call details of a method in a Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Returns the method's output after storing its inputs and output.
        '''
        in_key = f'{method.__qualname__}:inputs'
        out_key = f'{method.__qualname__}:outputs'
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return invoker


def replay(fn: Callable) -> None:
    '''Displays the call history of a Cache class' method.
    '''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = f'{fxn_name}:inputs'
    out_key = f'{fxn_name}:outputs'
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print(f'{fxn_name} was called {fxn_call_count} times:')
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print(f'{fxn_name}(*{fxn_input.decode("utf-8")}) -> {fxn_output}')


class Cache:
    """Cache class"""
    def __init__(self):
        """constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)


    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store method"""
        key = f"{uuid.uuid4()}"
        self._redis.set(key, data)
        return key


    def get(self, key: str, fn: callable = None) -> Union[str, bytes, int, float]:
        """get method"""
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data


    def get_str(self, key: str) -> str:
        """get_str method"""
        return self.get(key, lambda x: x.decode('utf-8'))


    def get_int(self, key: str) -> int:
        """get_int method"""
        return self.get(key, int)
