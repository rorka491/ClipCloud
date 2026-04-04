import magic
from datetime import timedelta, datetime, UTC
from uuid import uuid4
import logging
import json
from fastapi import File, UploadFile, HTTPException
from src.models import Message
from src.schemas.message import MessageCreate, MessageHistoryResponse
from src.dependency.redis import get_redis
from src.core.config import TTL
from src.validate import FileValidator
from src.services.s3client import S3Client
from src.services.connecrions import ConnectionService
from src.constants import ALL




class MessageService:
    def __init__(self, code, s3_client, connection_service):
        self.redis = get_redis()
        self.MAX_MESSAGES = 50
        self.TTL = TTL
        self.room_code = code
        self.room_key = f"room:{code}"
        self.s3_client: S3Client = s3_client
        self.connections: ConnectionService = connection_service

    async def add_message(
        self,
        message: MessageCreate,
        file: UploadFile = None
    ):
        file_url = await self._handle_file_upload(file, message)

        msg = self._build_message(message, file_url)

        await self._save_message(msg)

        await self.connections.broadcast(
            room_code=self.room_code,
            message=msg
        )

        return msg
    
    
    async def get_history(self) -> MessageHistoryResponse:
        room_raw = await self.redis.get(self.room_key)
        await self.redis.expire(self.room_key, self.TTL)
        room_data = json.loads(room_raw)
        messages = room_data.get("messages", [])
        history = []
        for m in messages:
            msg_obj = Message.model_validate(m)
            history.append(msg_obj.model_dump())

        return MessageHistoryResponse(messages_history=history)

    async def _handle_file_upload(
        self,
        file: UploadFile,
        message: MessageCreate
    ) -> str | None:

        if not (file and message.type in ("image", "file")):
            return None

        logging.warning("File start preproccess")

        file_data = await FileValidator.validate_file(file)

        object_name = f"{self.room_key}/files/{file.filename}"

        is_upload, file_url = await self.s3_client.upload_file_stream(
            file_obj=file.file,
            object_name=object_name,
            content_type=file_data["content_type"]
        )

        if not is_upload:
            raise HTTPException(500, "something went wrong")

        return file_url
    

    async def _save_message(self, msg: dict):

        room_raw = await self.redis.get(self.room_key)
        room_data = json.loads(room_raw)

        room_data["messages"].append(msg)

        room_data["messages_count"] = min(
            room_data.get("messages_count", 0) + 1,
            self.MAX_MESSAGES
        )

        room_data["expires_at"] = (
            datetime.now(UTC) + timedelta(seconds=self.TTL)
        ).isoformat()

        await self.redis.set(
            self.room_key,
            json.dumps(room_data),
            ex=self.TTL
        )

    def _build_message(
        self,
        message: MessageCreate,
        file_url: str | None
    ) -> dict:
        return Message(
            id=uuid4().hex,
            type=message.type,
            file_url=file_url,
            text=message.text,
            author_name=message.author_name,
            created_at=datetime.now(UTC) + timedelta(hours=7)
        ).model_dump(mode="json")


