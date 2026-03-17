from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter
from src.services.connecrions import ConnectionService
from src.services.room import RoomService, MessageService
from src.schemas.message import MessageCreate
from datetime import datetime, UTC
import logging

router = APIRouter()


connections = ConnectionService()
room_service = RoomService()
message_service = MessageService()



@router.post("/rooms")
async def create_room():
    code = await room_service.create_room()
    return {"code": code}

@router.websocket("/rooms/{room_code}")
async def websocket_endpoint(websocket: WebSocket, room_code: str):
    await connections.connect(room_code, websocket)
    history = await message_service.get_messages(room_code)
    await websocket.send_json({
        "type": "history",
        "messages": history
        })
    try:
        while True:
            data = await websocket.receive_json()
            logging.warning(data)
            msg = MessageCreate(**data)

            await message_service.add_message(room_code, msg)

            await connections.broadcast(room_code, {
                "type": msg.type,
                "content": msg.content,
                "created_at": datetime.now(UTC).isoformat()
            })
    except WebSocketDisconnect:
        connections.disconnect(room_code, websocket)