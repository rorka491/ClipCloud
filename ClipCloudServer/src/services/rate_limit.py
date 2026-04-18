from collections import defaultdict, deque
from threading import Lock
from time import time




class RateLimiter:
    def __init__(self) -> None:
        self._buckets: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()
        self.is_active = True

    async def is_limited(
        self,
        ip_address: str,
        endpoint: str,
        max_requests: int,
        window_seconds: int
    ) -> bool:
        if not self.is_active:
            return False
        
        key = f"rate_limiter:{endpoint}:{ip_address}"
        now = time()
        window_start = now - window_seconds

        with self._lock:
            bucket = self._buckets[key]
            while bucket and bucket[0] < window_start:
                bucket.popleft()

            if len(bucket) >= max_requests:
                return True

            bucket.append(now)
            return False
