from datetime import datetime

class Message:
    id: str
    room_code: str
    type: str
    content: str
    created_at: datetime