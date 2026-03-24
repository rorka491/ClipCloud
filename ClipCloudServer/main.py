from fastapi import FastAPI
from src.api.router import router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://clipcloud.cloud.nstu.ru",
        "http://clipcloud.cloud.nstu.ru",
        "https://localhost",
        "http://localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

