from datetime import timedelta, datetime, UTC
from uuid import uuid4
import json
from fastapi import HTTPException
from tortoise.exceptions import IntegrityError
from src.core.config import TTL
from src.services.s3client import S3Client
from src.utils import is_expired
from src.repositories import RoomRepository



class RoomService:
    
    def __init__(self, repo, redis):
        self.redis = redis
        self.TTL = TTL
        self.repo: RoomRepository = repo

    async def create_room(self) -> tuple[str, int]:
        try:
            room_code, room_id = await self.repo.create()
        except IntegrityError as e:
            raise HTTPException(
                status_code=500,
                detail='Failed to create room'
            )
        return room_code, room_id

    async def get(self, code: str):
        room = await self.repo.get(code)
        if room is None:
            raise HTTPException(
                status_code=404,
                detail='Failed to found room'
            )
        return room
    
    async def delete_expired_rooms(self, codes):
        return await self.repo.batch_delete(codes)
    
    async def get_expired_rooms(self) -> list[str]:
        return await self.repo.get_expired_rooms()

    async def exists(self, code: str) -> bool:
        return await self.repo.exists(code=code)
    
    
    async def _refresh_ttl(self, code: str):
        return await self.repo.refresh_expires_at(code=code)




