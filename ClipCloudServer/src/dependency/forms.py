from fastapi import Depends, Form, HTTPException
from src.schemas.message import MessageCreate
from typing import Optional
from src.enums import MessageTypeEnum, MessageCreateTypeEnum

def get_form_data(
    type: MessageCreateTypeEnum = Form(...),
    text: Optional[str] = Form(None),
    author_name: str = Form(...),
) -> MessageCreate:
    try:
        return MessageCreate(
            type=type,
            text=text,
            author_name=author_name
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid message type. Allowed: {[t.value for t in MessageCreateTypeEnum]}"
        )
