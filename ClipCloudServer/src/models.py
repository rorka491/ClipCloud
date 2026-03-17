from pydantic import BaseModel
from datetime import datetime


class Message(BaseModel):
    id: str
    type: str
    content: str
    created_at: datetime

class Room(BaseModel):
    code: str
    created_at: datetime
    expires_at: datetime
    messages: list[Message] = []

