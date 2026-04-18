import asyncio
from src.repositories.room import RoomRepository
import logging 

CLEANUP_INTERVAL = 60

async def cleanup_expired_rooms(room_repo: RoomRepository):

    while True:
        try:
            count_rooms = await room_repo.batch_delete()
            logging.warning(f'count rooms {count_rooms}')
            await asyncio.sleep(CLEANUP_INTERVAL)
            
        except Exception as e:
            await asyncio.sleep(CLEANUP_INTERVAL)

