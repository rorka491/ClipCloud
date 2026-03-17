from datetime import datetime


class Room:
    code: str
    created_at: datetime
    expires_at: datetime
    messages_count: int