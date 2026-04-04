from functools import lru_cache
from redis.asyncio import Redis


@lru_cache
def get_redis():
    return Redis(port=6379, host='localhost')