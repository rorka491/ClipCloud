from fastapi import FastAPI
from src.api.router import router
from fastapi.middleware.cors import CORSMiddleware
from src.dependency.services import get_room_service
# from src.middleware import RoomExistsMiddleware


app = FastAPI()

app.state.room_service = get_room_service()

# app.add_middleware(RoomExistsMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)

