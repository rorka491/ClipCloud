from fastapi import Path, Depends
from typing import Annotated
from src.services.message import MessageService
from src.services.s3client import S3Client
from src.core.config import ACCESS_KEY, SECRET_KEY, BUCKET_NAME, ENDPOINT_URL

from src.services.connecrions import ConnectionService
from src.services.room import RoomService
from src.repositories import MessageRepository, RoomRepository
from src.dependency.repositories import get_message_repository, get_room_repository
from src.dependency.redis import get_redis 








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
    connection_service: Annotated[ConnectionService, Depends(get_connection_service)],
    repo: Annotated[MessageRepository, Depends(get_message_repository)],
    redis = Depends(get_redis)
) -> MessageService:
    return MessageService(
        code=code, 
        s3_client=s3_client, 
        connection_service=connection_service,
        repo=repo,
        redis=redis
    )

def get_room_service(
    repo: Annotated[RoomRepository, Depends(get_room_repository)],
    redis = Depends(get_redis)
): 
    return RoomService(repo, redis)

