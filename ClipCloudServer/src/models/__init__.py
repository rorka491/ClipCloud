from src.models.message import Message
from src.models.room import Room
from aerich import Command
from tortoise import Tortoise
from src.core.db import TORTOISE_ORM

async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)

    command = Command(tortoise_config=TORTOISE_ORM, app='models')
    await command.init()
    await command.upgrade()