from fastapi import WebSocket
from typing import Dict, List
import logging


class ConnectionService:
    connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, room_code: str, websocket: WebSocket):
        await websocket.accept()
        self.connections.setdefault(room_code, []).append(websocket)

    def disconnect(self, room_code: str, websocket: WebSocket):
        if room_code in self.connections:
            self.connections[room_code].remove(websocket)
            if not self.connections[room_code]:
                del self.connections[room_code]


    async def broadcast(self, room_code: str, message: dict):
        logging.warning(f"Broadcast to {room_code}")

        if room_code in self.connections:
            for websocket in self.connections[room_code]:
                await websocket.send_json(message)