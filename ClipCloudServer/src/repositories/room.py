from uuid import uuid4
from tortoise.transactions import in_transaction
from tortoise.expressions import Q
from tortoise.exceptions import IntegrityError
from src.repositories.base import BaseRepository
from src.models.room import Room
from src.core.config import TTL
from datetime import datetime, UTC, timedelta


class RoomRepository:
    model = Room


    async def get(self, code: str):
        return await self.model.filter(
            Q(room_code=code) & 
            Q(expires_at__gt=datetime.now(UTC))
        ).get_or_none()
    
    async def exists(self, code) -> bool:
        is_refreshed, room = await self.refresh_expires_at(code)
        if is_refreshed:
            return await self.model.filter(
                Q(room_code=code) & 
                Q(expires_at__gt=datetime.now(UTC))
            ).exists()
        return False
    
    async def get_expired_rooms(self) -> list[str]:
        room_codes = await self.model.filter(expires_at__lt=datetime.now(UTC)).values_list('room_code', flat=True)
        return room_codes


    @staticmethod
    def _generate_code():
        return uuid4().hex[:4].upper()
    
    @staticmethod
    def _get_expired_at():
        return datetime.now(UTC) + timedelta(seconds=TTL)
        
    async def _get_exists_codes(self):
        codes = await self.model.all().values_list('room_code', flat=True)
        return set(codes)

    async def create(self, max_attempts=10) -> tuple[str, int]:
        codes = await self._get_exists_codes()

        for attempt in range(max_attempts):
            code = self._generate_code()
            if code not in codes:
                room = await self.model.create(
                    room_code=code,
                    expires_at=self._get_expired_at(),
                )
                return code, room.id
        raise IntegrityError(f'Failed to generate unique code after {max_attempts} attempts')
    
    async def delete(self, code: str, using_db: None):
        if using_db:
            return await self.model.filter(room_code=code).using_db(using_db).delete()
        return await self.model.filter(room_code=code).delete()
    

    async def batch_delete(self) -> int:
        return await self.model.filter(expires_at__lt=datetime.now(UTC)).delete()
        
    async def refresh_expires_at(self, code: str) -> tuple:
        async with in_transaction() as conn:
            room = await self.model.filter(room_code=code, expires_at__gt=datetime.now(UTC)).select_for_update().get_or_none()
            if room:
                room.expires_at += timedelta(seconds=TTL)
                await room.save(using_db=conn)
                return True, room
            return False, None




