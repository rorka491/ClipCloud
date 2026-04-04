from typing import Callable
from fastapi import HTTPException, status
from fastapi.datastructures import State
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import Awaitable
from src.services.room import RoomService
import logging 



# class RoomExistsMiddleware(BaseHTTPMiddleware):

#     async def dispatch(self, request: Request[State], call_next: Callable[[Request[State]], Awaitable[Response]]) -> Response:
#         room_service: RoomService = request.app.state.room_service

#         room_code = request.path_params.get("code") or request.path_params.get("room_code")
#         logging.warning('work middleware')
#         logging.warning(room_code)
#         if room_code and not await room_service.exists(code=room_code):
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail='Room not found'
#             )
#         response = await call_next(request)
#         return response


