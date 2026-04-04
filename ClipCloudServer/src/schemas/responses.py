from pydantic import BaseModel, Field, HttpUrl
from src.enums import MessageTypeEnum
from typing import Literal
from src.schemas.message import MessageRead
from datetime import datetime

class BaseResponse(BaseModel):
    created_at: datetime


class RateLimitResponse(BaseResponse):
    type: Literal[MessageTypeEnum.RATE_LIMIT_ERROR] = MessageTypeEnum.RATE_LIMIT_ERROR
    content: str = Field(default='Too many requests')
    
class MessageHistoryResponse(BaseResponse):
    type: Literal[MessageTypeEnum.HISTORY] = MessageTypeEnum.HISTORY
    content: list[MessageRead]

class TextMessageResponse(BaseResponse):
    type: Literal[MessageTypeEnum.TEXT] = MessageTypeEnum.TEXT
    content: MessageRead

class ImageMessageResponse(BaseResponse):
    type: Literal[MessageTypeEnum.IMAGE] = MessageTypeEnum.IMAGE
    content: HttpUrl

class FileMassageResponse(BaseResponse):
    type: Literal[MessageTypeEnum.FILE] = MessageTypeEnum.FILE
    content: HttpUrl