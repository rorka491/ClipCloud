from typing import Annotated
from fastapi import Depends, Path, HTTPException
from src.repositories import MessageRepository, RoomRepository
from src.services.room import RoomService
from src.models import Room




def get_room_repository():
    return RoomRepository()

async def get_room_or_exc(
    code: Annotated[str, Path(...)],
    room_repo: Annotated[RoomService, Depends(get_room_repository)] 
):  
    room = await room_repo.get(code=code)
    if not room:
        raise HTTPException(
                403,
                detail='Room does not exists'
            )
    return room


async def get_room_id(
    room: Annotated[Room, Depends(get_room_or_exc)]
):
    return room.id

def get_message_repository(room_id: Annotated[int, Depends(get_room_id)]):
    return MessageRepository(room_id)





