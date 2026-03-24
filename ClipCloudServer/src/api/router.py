from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
from src.services.connecrions import ConnectionService
from src.services.room import RoomService, MessageService
from src.schemas.message import MessageCreate
from datetime import datetime, UTC
import logging
from typing import Annotated
from src.services.rate_limit import RateLimiter
from src.dependency.dependency_factory import ws_chat_rate_limit
from src.dependency.services import get_rate_limiter


router = APIRouter(prefix='/api')


connections = ConnectionService()
room_service = RoomService()
message_service = MessageService()



@router.websocket("/ws/{room_code}")
async def websocket_endpoint(websocket: WebSocket, room_code: str, rate_limiter: Annotated[RateLimiter, Depends(get_rate_limiter)]):
    await connections.connect(room_code, websocket)
    history = await message_service.get_messages(room_code)
    await websocket.send_json({
        "type": "history",
        "messages": history
        })
    try:
        while True:

            data = await websocket.receive_json()
            msg = MessageCreate(**data)


            limited = await ws_chat_rate_limit(
                rate_limiter,
                websocket.client.host,
                room_code
            )
            if limited:
                await websocket.send_json({
                    "type": "error",
                    "message": "Too many requests"
                })
 

            await message_service.add_message(room_code, msg)

            await connections.broadcast(room_code, {
                "type": msg.type,
                "content": msg.content,
                "created_at": datetime.now(UTC).isoformat()
            })
    except WebSocketDisconnect:
        connections.disconnect(room_code, websocket)

@router.post("/rooms")
async def create_room():
    code = await room_service.create_room()
    return {"code": code}


@router.get("/rooms/{code}")
async def get_room(code):
    code = await room_service.exists(code)
    return {"is_exists": code}


