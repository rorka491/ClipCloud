from typing import Annotated
from fastapi import Request, Depends, HTTPException, Path
from src.dependency.rate_limit import get_rate_limiter
from src.services.rate_limit import RateLimiter



def rate_limiter_factory(
    endpoint: str,
    max_requests: int,
    window_seconds: int,
    test_mode: bool = False
):
    if test_mode:
        def test():
            return
        return test
    
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



