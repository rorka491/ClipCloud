from datetime import timedelta, datetime, UTC
from uuid import uuid4
import logging
from fastapi import File, UploadFile, HTTPException
from src.schemas.message import MessageCreate, MessageHistoryResponse, MessageCreateInternal, MessageReadInternal
from src.core.config import TTL
from src.validate import FileValidator
from src.services.s3client import S3Client
from src.services.connecrions import ConnectionService
from src.repositories import MessageRepository




class MessageService:
    def __init__(self, code, s3_client, connection_service, repo):
        self.room_code = code
        self.room_key = f"room:{code}"
        self.s3_client: S3Client = s3_client
        self.connections: ConnectionService = connection_service
        self.repo: MessageRepository = repo


    async def add_message(
        self,
        message: MessageCreate,
        file: UploadFile = None
    ):
        file_url = await self._handle_file_upload(file, message)

        msg = self._build_message(message, file_url)
        msg_dict = msg.model_dump(mode='json')

        await self._save_message(msg)

        await self.connections.broadcast(
            room_code=self.room_code,
            message=msg_dict
        )
        return msg_dict
    
    
    async def get_history(self) -> list[MessageReadInternal]:
        messages = await self.repo.list()
        history = []
        for m in messages:
            msg_obj = MessageReadInternal.model_validate(m)
            history.append(msg_obj.model_dump())

        return history


    async def _handle_file_upload(
        self,
        file: UploadFile,
        message: MessageCreate
    ) -> str | None:

        if not (file and message.message_type in ("image", "file")):
            return None

        logging.warning("File start preproccess")

        file_data = await FileValidator.validate_file(file)

        object_path = f"{self.room_key}/{file.filename}"
        file_content = await file.read()

        file_url = await self.s3_client.upload(
            key=object_path,
            data=file_content,
            content_type=file_data["content_type"]
        )

        return file_url
    

    async def _save_message(self, msg: MessageCreateInternal):
        await self.repo.create(msg)


    def _build_message(
        self,
        message: MessageCreate,
        file_url: str | None
    ) -> MessageCreateInternal:
        
        return MessageCreateInternal(
            room_id=self.repo.room_id,
            message_type=message.message_type,
            file_url=file_url,
            text=message.text,
            username=message.username,
            created_at=datetime.now(UTC)
        )

