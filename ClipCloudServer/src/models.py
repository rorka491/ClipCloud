from pydantic import BaseModel, Field, FileUrl, AnyUrl
from datetime import datetime
from src.enums import MessageTypeEnum
from typing import Optional



class Message(BaseModel):
    id: str
    type: MessageTypeEnum
    text: str = Field(..., max_length=6000)
    author_name: str = Field(..., max_length=12)
    file_url: Optional[AnyUrl] = None
    created_at: datetime



class Room(BaseModel):
    code: str
    created_at: datetime
    expires_at: datetime
    messages: list[Message] = []

