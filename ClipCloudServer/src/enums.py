from enum import Enum



class MessageCreateTypeEnum(str, Enum):
    FILE = 'file'
    IMAGE = 'image'
    TEXT = 'text'


class MessageTypeEnum(str, Enum):
    FILE = 'file'
    IMAGE = 'image'
    TEXT = 'text'
    ERROR = 'error'
    RATE_LIMIT_ERROR = 'rate_limit_error'
    HISTORY = 'history'




