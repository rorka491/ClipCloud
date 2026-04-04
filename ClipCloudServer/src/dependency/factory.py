from typing import Annotated
from fastapi import Request, Depends, HTTPException, Path
from src.dependency.services import get_rate_limiter
from src.services.rate_limit import RateLimiter
from typing import Optional

def rate_limiter_factory(
    endpoint: str,
    max_requests: int,
    window_seconds: int
):
    async def dependency(
        request: Request,
        rate_limiter: Annotated[RateLimiter, Depends(get_rate_limiter)],
    ):

        limited = await rate_limiter.is_limited(
            ip_address=request.client.host,
            endpoint=endpoint,
            max_requests=max_requests,
            window_seconds=window_seconds
        )

        if limited:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded for {endpoint}. Max {max_requests} requests per {window_seconds} seconds"
            )
    return dependency



create_room_rate_limit = rate_limiter_factory('create_room', 10, 5)
get_room_rate_limit = rate_limiter_factory('get_room', 10, 5)
get_history_rate_limit = rate_limiter_factory('hisotry', 10, 5)
default_rate_limit = rate_limiter_factory('default', 10, 5)



