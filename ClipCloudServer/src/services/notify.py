
from fastapi import WebSocket
from fastapi.responses import JSONResponse
from typing import Annotated
import asyncio


class NotificationManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}
    
    async def connect(self, room_code: str, websocket: WebSocket):
        await websocket.accept()
        if room_code not in self.active_connections:
            self.active_connections[room_code] = []
        self.active_connections[room_code].append(websocket)
        print(f"Client connected to room {room_code}. Total: {len(self.active_connections[room_code])}")
    
    def disconnect(self, room_code: str, websocket: WebSocket):
        if room_code in self.active_connections:
            self.active_connections[room_code].remove(websocket)
            if not self.active_connections[room_code]:
                del self.active_connections[room_code]
        print(f"Client disconnected from room {room_code}")
    
    async def notify_room(self, room_code: str, notification: dict):
        """Отправляет уведомление всем в комнате"""
        if room_code in self.active_connections:

            connections = self.active_connections[room_code].copy()
            for connection in connections:
                try:
                    await connection.send_json(notification)
                except Exception as e:
                    print(f"Error sending notification: {e}")

    
    async def notify_user(self, websocket: WebSocket, notification: dict):
        """Отправляет уведомление конкретному пользователю"""
        try:
            await websocket.send_json(notification)
        except Exception as e:
            print(f"Error sending notification to user: {e}")



