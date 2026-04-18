import asyncio
from src.repositories.room import RoomRepository


CLEANUP_INTERVAL = 60 * 60 

async def cleanup_expired_rooms(room_repo: RoomRepository):

    while True:
        try:
            await room_repo.batch_delete()
            await asyncio.sleep(CLEANUP_INTERVAL)
            
        except Exception as e:
            print(f"Ошибка при очистке комнат: {e}")
            await asyncio.sleep(CLEANUP_INTERVAL)