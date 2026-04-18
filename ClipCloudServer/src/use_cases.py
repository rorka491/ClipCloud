from typing import Annotated
from tortoise.transactions import in_transaction
from src.services import MessageService, RoomService, S3Client
from src.repositories import RoomRepository, MessageRepository


class DeleteRoomUseCase:

    def __init__(
        self, 
        room_repo, 
        message_repo, 
        s3_client
    ) -> None:
        self.room_repo: RoomRepository = room_repo
        self.message_repo: MessageRepository = message_repo
        self.s3_client: S3Client = s3_client


    async def execute(self, code) -> int:
        
        await self.s3_client.delete_room_files(code=code)
        async with in_transaction() as conn:
            await self.room_repo.delete(using_db=conn, code=code)
            delete_count = await self.message_repo.delete(using_db=conn, room_code=code)
        
        return delete_count

        