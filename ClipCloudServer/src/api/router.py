from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends, File, UploadFile, Form
from src.services.connecrions import ConnectionService
from src.services.room import RoomService
from src.services.message import MessageService
from src.schemas.message import MessageCreate
from datetime import datetime, UTC
import logging
from typing import Annotated, Optional
from src.services.rate_limit import RateLimiter
from src.dependency.factory import create_room_rate_limit, get_room_rate_limit, default_rate_limit
from src.dependency.services import get_message_service, get_room_service, get_connection_service
from src.dependency.factory import rate_limiter_factory
from src.dependency.forms import get_form_data
from src.schemas.message import MessageHistoryResponse
from src.dependency.validation import room_exists



router = APIRouter(prefix='/api')


@router.websocket(
    "/notify/{code}",
    dependencies=[
        Depends(room_exists),
    ]
)
async def websocket_endpoint_v2(
    websocket: WebSocket,
    code: str,
    connections: Annotated[ConnectionService, Depends(get_connection_service)]
):
    try:
        await connections.connect(code, websocket)
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connections.disconnect(code, websocket)


@router.post(
    "/rooms",
    dependencies=[
        Depends(default_rate_limit),
    ]
)
async def create_room(
    service: Annotated[RoomService, Depends(get_room_service)],
):
    room_code = await service.create_room()
    return {"code": room_code}


@router.get(
    "/rooms/{code}",
    dependencies=[
        Depends(default_rate_limit),
        Depends(room_exists),
    ]
)
async def get_room(
    code,
    service: Annotated[RoomService, Depends(get_room_service)],
):
    exists = await service.exists(code)
    return {"is_exists": exists}

@router.get(
    "/rooms/{code}/history",
    response_model=MessageHistoryResponse,
    dependencies=[
        Depends(default_rate_limit),
        Depends(room_exists),
    ]
)
async def get_history(
    service: Annotated[MessageService, Depends(get_message_service)],
):
    return await service.get_history()

@router.post(
    '/rooms/{code}/messages',
    dependencies=[
        Depends(default_rate_limit),
        Depends(room_exists),
    ]
)
async def create_message(
    data: Annotated[MessageCreate, Depends(get_form_data)],
    service: Annotated[MessageService, Depends(get_message_service)],
    file: Optional[UploadFile] = File(None),
):
    return await service.add_message(data, file)

