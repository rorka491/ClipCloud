from functools import lru_cache
from redis.asyncio import Redis
from src.services.rate_limit import RateLimiter

@lru_cache
def get_redis():
    return Redis(port=6379, host='redis')

@lru_cache
def get_rate_limiter():
    return RateLimiter(get_redis())