#!/usr/bin/env python3
"""A cache class."""
import redis
from uuid import uuid4
from typing import Any, Callable, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorate a function to count its calls."""
    @wraps(method)
    def new_method(self, *args, **kwargs):
        """Do the same thing as previous method but also count calls."""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return new_method


def call_history(method: Callable) -> Callable:
    """Decorate a function to keep its call history."""
    @wraps(method)
    def new_method(self, *args):
        """Do the same thing as previous method but also record history."""
        self._redis.rpush(method.__qualname__ + ":inputs", str(args))
        res = method(self, *args)
        self._redis.rpush(method.__qualname__ + ":outputs", res)
        return res
    return new_method


class Cache:
    """A class for storing key-value pairs."""

    def __init__(self):
        """Initialize the cache."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Any) -> str:
        """Store a value in redis with a random key."""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Union[Callable, None] = None)\
            -> Union[int, float, str, bytes]:
        """Get a value from the cache."""
        if fn is None:
            return self._redis.get(key)
        return fn(self._redis.get(key))

    def get_int(self, key: str) -> int:
        """Get an integer from the cache."""
        return int(self._redis.get(key))

    def get_str(self, key: str) -> str:
        """Get a string from the cache."""
        data = self._redis.get(key)
        return data.decode("utf-8")


def replay(func: Callable) -> None:
    """Print the replay of a function."""
    name = func.__qualname__
    cache = redis.Redis()
    count = cache.get(name)
    if count is None:
        count = b'0'
    print("{} was called {} times:".format(
        name,
        count.decode("utf-8")
    ))
    for inp, outp in zip(
            cache.lrange(name + ":inputs", 0, -1),
            cache.lrange(name + ":outputs", 0, -1)
    ):
        print("{}(*{}) -> {}".format(
            name,
            inp.decode("utf-8"),
            outp.decode("utf-8")
        ))
