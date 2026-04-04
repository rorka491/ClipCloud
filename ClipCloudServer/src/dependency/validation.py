from fastapi import Depends, Path, HTTPException
from typing import Annotated
from src.services.room import RoomService
from src.dependency.services import get_room_service

async def room_exists(
    code: Annotated[str, Path(...)],
    room_service: Annotated[RoomService, Depends(get_room_service)] 
):
    if not await room_service.exists(code):
        raise HTTPException(
                403,
                detail='Room does not exists'
            )
