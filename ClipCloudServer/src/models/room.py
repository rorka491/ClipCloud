from tortoise import models, fields
from src.models.base import BaseModelPK
from src.enums import MessageCreateTypeEnum


class Room(BaseModelPK):
    room_code = fields.CharField(max_length=255, unique=True)
    expires_at = fields.DatetimeField()

    class Meta:
        table = 'rooms'

