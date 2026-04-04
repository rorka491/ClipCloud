from pydantic import BaseModel


class RateLimitException(BaseModel):
    detail: str = ''
