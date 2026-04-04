from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, AnyUrl, Discriminator
import uuid
from src.enums import MessageTypeEnum, MessageCreateTypeEnum
from typing import Optional, Literal, Union, Annotated


# class AnyUrl(BaseModel):

class BaseMessage(BaseModel):
    author_name: str = Field(max_length=12, default='User')
    created_at: datetime


class TextMessageRead(BaseMessage):
    type: Literal[MessageCreateTypeEnum.TEXT] = MessageCreateTypeEnum.TEXT
    text: str = Field(..., max_length=6000)


class ImageMessageRead(BaseMessage):
    type: Literal[MessageCreateTypeEnum.IMAGE] = MessageCreateTypeEnum.IMAGE
    text: Optional[str] = Field(None, max_length=200)
    file_url: AnyUrl


class FileMessageRead(BaseMessage):
    type: Literal[MessageCreateTypeEnum.FILE] = MessageCreateTypeEnum.FILE
    text: Optional[str] = Field(None, max_length=200)
    file_url: AnyUrl


MessageRead = Annotated[
    Union[
        TextMessageRead,
        ImageMessageRead,
        FileMessageRead,
    ],
    Discriminator('type') 
]

class MessageHistoryResponse(BaseModel):
    type: Literal[MessageTypeEnum.HISTORY] = MessageTypeEnum.HISTORY
    messages_history: list[MessageRead] 


class RateLimitResponse(BaseModel):
    type: Literal[MessageTypeEnum.RATE_LIMIT_ERROR] = MessageTypeEnum.RATE_LIMIT_ERROR
    content: str = Field(default='Too many requests')

# class MessageResponse(BaseModel):
#     type: Literal[MessageTypeEnum.HISTORY] = MessageTypeEnum.HISTORY
#     content: MessageRead

# class RoomRead(BaseModel):
#     code: str
#     messages: list[MessageRead]




# class MessageRead(BaseMessage):
#     type: MessageTypeEnum
#     text: Optional[str] = None
#     file_url: Optional[AnyUrl] = None
#     created_at: datetime


class MessageCreate(BaseModel):
    type: MessageCreateTypeEnum
    text: str = Field(..., max_length=6000)
    author_name: str = Field(max_length=12, default='User')




