from time import time
from random import randint
from redis.asyncio import Redis




class RateLimiter:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis
        self.is_active = True

    async def is_limited(
        self,
        ip_address: str,
        room_code: str,
        endpoint: str,
        max_requests: int,
        window_seconds: int
    ) -> bool:
        if not self.is_active:
            return False
        
        key = f"rate_limiter:{endpoint}:{ip_address}:{room_code}"

        current_ms = time() * 1000
        window_start_ms = current_ms - window_seconds * 1000

        current_request = f"{current_ms}-{randint(1, 100_000)}"

        async with self._redis.pipeline(transaction=True) as pipe:
            await pipe.zremrangebyscore(key, 0, window_start_ms)

            await pipe.zcard(key)
            await pipe.zadd(key, {current_request: current_ms})

            await pipe.expire(key, window_seconds)


            res = await pipe.execute()
        
        _, current_count, _, _ = res
        if current_count >= max_requests:
            return True
        
        return False

