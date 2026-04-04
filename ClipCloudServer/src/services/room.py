from datetime import timedelta, datetime, UTC
from uuid import uuid4
import json
from src.models import Room, Message
from src.dependency.redis import get_redis
from src.core.config import TTL
from src.schemas.room import RoomCreate
from src.constants import ALL



class RoomService:
    ROOM = 'room:{}'
    MESSAGES = 'room:{}:messages'
    
    def __init__(self):
        self.redis = get_redis()
        self.TTL = TTL

    async def create_room(self) -> str:
        while True:
            code = uuid4().hex[:4].upper()
            room_key = self.ROOM.format(code)

            now = datetime.now(UTC)
            expires_at = now + timedelta(seconds=self.TTL)

            room_data = RoomCreate(
                created_at=now,
                expires_at=expires_at,
                messages_count=0
            ).model_dump(mode='json')

            created = await self.redis.set(
                room_key,
                json.dumps(room_data),
                ex=self.TTL,
                nx=True
            )

            if created:
                return code


    async def exists(self, code: str) -> bool:
        return await self.redis.exists(f"room:{code}") > 0

    async def delete_room(self, code: str):
        room_key = f"room:{code}"
        async with self.redis.pipeline() as pipe:
            pipe.multi()
            pipe.delete(room_key)
            await pipe.execute()
    
    async def _refresh_ttl(self, code: str):
        room_key = f"room:{code}"
        
        async with self.redis.pipeline() as pipe:
            pipe.expire(room_key, self.TTL)
            await pipe.execute()



