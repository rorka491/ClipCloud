from tortoise import models, fields
from src.models.base import BaseModelPK
from src.enums import MessageCreateTypeEnum


class Message(BaseModelPK):
    room = fields.ForeignKeyRelation('models.Room', on_delete=fields.CASCADE)
    message_type = fields.CharEnumField(enum_type=MessageCreateTypeEnum)
    username = fields.CharField(max_length=255)
    file_url = fields.CharField(max_length=6000, null=True)
    text = fields.CharField(max_length=6000)


    class Meta:
        table = 'messages'


