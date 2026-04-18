from datetime import datetime, UTC

def is_expired(expires_at: str) -> bool:
    expires = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
    return expires < datetime.now(UTC)