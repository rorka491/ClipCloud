# from fastapi import Depends
# from typing import Annotated
# from src.models import Room
# from src.dependency.validation import get_room_or_exc




# async def get_room_id(
#     room: Annotated[Room, Depends(get_room_or_exc)]
# ):
#     return room.id