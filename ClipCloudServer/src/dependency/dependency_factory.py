from typing import Annotated
from fastapi import Request, Depends, HTTPException
from src.dependency.services import get_rate_limiter
from src.services.rate_limit import RateLimiter



def rate_limiter_factory(
    endpoint: str,
    max_requests: int,
    window_seconds: int
):
    async def dependency(
        rate_limiter: Annotated[RateLimiter, Depends(get_rate_limiter)],
        ip_address: str,
        room_code: str
    ):

        limited = await rate_limiter.is_limited(
            ip_address,
            room_code,
            endpoint,
            max_requests,
            window_seconds
        )

        if limited:
            return True

    return dependency

ws_chat_rate_limit = rate_limiter_factory('ws', 10, 5)
