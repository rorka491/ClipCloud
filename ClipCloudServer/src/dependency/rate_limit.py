from functools import lru_cache
from src.services.rate_limit import RateLimiter


@lru_cache
def get_rate_limiter():
    return RateLimiter()
