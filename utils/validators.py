from datetime import datetime
from typing import Optional
from app.config import Config

def validate_party_size(party_size: int) -> bool:
    """Validate party size is within acceptable range."""
    return Config.MIN_PARTY_SIZE <= party_size <= Config.MAX_PARTY_SIZE

def validate_datetime(date: str, time: str) -> tuple[bool, Optional[str]]:
    """Validate date and time format and values."""
    try:
        full_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        if full_datetime < datetime.now():
            return False, "Cannot make reservations in the past"
        return True, None
    except ValueError:
        return False, "Invalid date or time format"