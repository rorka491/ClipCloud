from pydantic import BaseModel 
from datetime import datetime
from src.schemas.message import MessageCreate


class RoomCreate(BaseModel):
    room_code: str
    created_at: datetime
    expires_at: datetime
    messages_count: int
    messages: list = []



class RoomResponse(BaseModel):
    id: int
    room_code: str
    created_at: datetime
    expires_at: datetime

