
from uuid import uuid4
from src.models import Message
from tortoise.expressions import Q
from src.schemas.message import MessageCreate, MessageCreateInternal
import logging

class MessageRepository:
    model = Message

    def __init__(self, room_id) -> None:
        self.room_id = room_id

    async def list(self) -> list[Message]:
        messages = await self.model.filter(room_id=self.room_id).order_by('created_at')
        return list(messages)

    async def create(self, data: MessageCreateInternal):
        logging.info(repr(data))
        await self.model.create(**data.model_dump())

    async def delete(self, using_db: None, **filters) -> int:
        if using_db:
            return await self.model.filter(**filters).using_db(using_db).delete()
        return await self.model.filter(**filters).delete()


