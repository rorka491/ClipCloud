from pydantic import BaseModel 
from datetime import datetime
from src.schemas.message import MessageCreate


class RoomCreate(BaseModel):
    created_at: datetime
    expires_at: datetime
    messages_count: int
    messages: list = []

