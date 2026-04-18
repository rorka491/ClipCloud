from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
from src.repositories.room import RoomRepository
from src.tasks import cleanup_expired_rooms


room_repo = RoomRepository()

@asynccontextmanager
async def lifespan(app: FastAPI):
    

    task = asyncio.create_task(cleanup_expired_rooms(room_repo))
    
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    
