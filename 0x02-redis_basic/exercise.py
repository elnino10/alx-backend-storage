#!/usr/bin/env python3
"""exercise module"""
import uuid
from typing import Union
import redis



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
