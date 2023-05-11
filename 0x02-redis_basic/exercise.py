#!/usr/bin/env python3
"""A cache class."""
import redis
from uuid import uuid4
from typing import Any, Callable


class Cache:
    """A class for storing key-value pairs."""

    def __init__(self):
        """Initialize the cache."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, value: Any) -> str:
        """Store a value in redis with a random key."""
        key = str(uuid4())
        self._redis.set(key, value)
        return key

    def get(self, key: str, fn: Callable):
        """Get a value from the cache."""
        if fn is None:
            return self._redis.get(key)
        return fn(self._redis.get(key))

    def get_int(self, key: str) -> int:
        """Get an integer from the cache."""
        return self.get(key, int)

    def get_str(self, key: str) -> str:
        """Get a string from the cache."""
        return self.get(key, lambda s: s.decode('utf-8'))
