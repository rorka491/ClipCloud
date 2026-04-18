from typing import Annotated
from fastapi import Depends
from src.use_cases import DeleteRoomUseCase
from src.dependency.repositories import get_message_repository, get_room_repository
from src.dependency.services import get_s3_client


def provide_delete_room_use_case(
    room_repo=Depends(get_room_repository),
    message_repo=Depends(get_message_repository),
    s3_client=Depends(get_s3_client)
) -> DeleteRoomUseCase:
    return DeleteRoomUseCase(
        room_repo=room_repo,
        message_repo=message_repo,
        s3_client=s3_client
    )
