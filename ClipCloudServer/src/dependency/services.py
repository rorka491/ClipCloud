from fastapi import Path, Depends
from functools import lru_cache
from typing import Annotated, Callable
from src.services.rate_limit import RateLimiter
from src.services.message import MessageService
from src.services.s3client import S3Client
from src.core.config import ACCESS_KEY, SECRET_KEY, BUCKET_NAME, ENDPOINT_URL
from src.dependency.redis import get_redis
from src.services.connecrions import ConnectionService
from src.services.room import RoomService




def inject(getter: Callable):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            dep = getter()
            return func(self, *args, dep=dep, **kwargs)
        return wrapper
    return decorator


@lru_cache
def get_rate_limiter():
    return RateLimiter(get_redis())



def get_s3_client() -> S3Client:
    return S3Client(
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        endpoint_url=ENDPOINT_URL,
        bucket_name=BUCKET_NAME
    )




def get_connection_service():
    return ConnectionService()

async def get_message_service(
    code: Annotated[str, Path(...)],
    s3_client: Annotated[S3Client, Depends(get_s3_client)],
    connection_service: Annotated[ConnectionService, Depends(get_connection_service)]
) -> MessageService:
    return MessageService(
        code=code, 
        s3_client=s3_client, 
        connection_service=connection_service
    )

def get_room_service(): 
    return RoomService()

