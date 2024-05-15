#!/usr/bin/env python3
"""exercise module"""
import uuid
import redis


class Cache:
    """Cache class"""
    def __init__(self):
        """constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)


    def store(self, data) -> str:
        """store method"""
        key = f"{uuid.uuid4()}"
        self._redis.set(key, data)
        return key
