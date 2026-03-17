from src.models import Room, Message
from src.schemas.message import MessageCreate
from redis.asyncio import Redis
from datetime import timedelta, datetime, UTC
from uuid import uuid4
import json
import logging

redis = Redis.from_url("redis://localhost:6379", decode_responses=True)


class RoomService:

    ROOM_TTL = 3600

    async def create_room(self) -> str:
        code = uuid4().hex[:6].upper()
        now = datetime.now(UTC)
        expires_at = (now + timedelta(seconds=self.ROOM_TTL)).isoformat()
        room_data = {
            "code": code,
            "created_at": now.isoformat(),
            "expires_at": expires_at,
            "messages_count": 0
        }
        await redis.set(f"room:{code}", json.dumps(room_data), ex=self.ROOM_TTL)
        return code

    async def get_room(self, code: str) -> Room | None:
        room_raw = await redis.get(f"room:{code}")
        if not room_raw:
            return None

        room_data = json.loads(room_raw)
        messages_raw = await redis.lrange(f"room:{code}:messages", 0, -1)
        messages = [Message.model_validate_json(m) for m in messages_raw]

        return Room(
            code=room_data["code"],
            created_at=datetime.fromisoformat(room_data["created_at"]),
            expires_at=datetime.fromisoformat(room_data["expires_at"]),
            messages=messages
        )

    async def exists(self, code: str) -> bool:
        return await redis.exists(f"room:{code}") > 0


class MessageService:

    MAX_MESSAGES = 50

    async def add_message(self, code: str, message: MessageCreate):
        msg = Message(
            id=uuid4().hex,
            type=message.type,
            content=message.content,
            created_at=datetime.now(UTC)
        )
        await redis.lpush(f"room:{code}:messages", msg.json())

        await redis.ltrim(f"room:{code}:messages", 0, self.MAX_MESSAGES - 1)

        room_raw = await redis.get(f"room:{code}")
        if room_raw:
            room_data = json.loads(room_raw)
            room_data["messages_count"] = min(room_data.get("messages_count", 0) + 1, self.MAX_MESSAGES)
            await redis.set(f"room:{code}", json.dumps(room_data))

    async def get_messages(self, code: str) -> list[dict]:
        messages_raw = await redis.lrange(f"room:{code}:messages", 0, -1)
        result = []
        for m in messages_raw:
            msg_obj = Message.parse_raw(m).dict()
            # Преобразуем datetime в строку
            if isinstance(msg_obj.get("created_at"), datetime):
                msg_obj["created_at"] = msg_obj["created_at"].isoformat()
            result.append(msg_obj)
        logging.warning(result)
        return result[::-1]