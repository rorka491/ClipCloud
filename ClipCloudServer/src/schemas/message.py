from datetime import datetime
from pydantic import BaseModel

class MessageCreate(BaseModel):
    type: str
    content: str


class MessageRead(BaseModel):
    id: str
    type: str
    content: str
    created_at: datetime


class RoomRead(BaseModel):
    code: str
    messages: list[MessageRead]
