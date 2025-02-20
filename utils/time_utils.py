from datetime import datetime, timedelta

def parse_time_slot(time_str: str) -> datetime:
    """Convert time string to datetime object."""
    try:
        return datetime.strptime(time_str, "%H:%M")
    except ValueError:
        raise ValueError("Invalid time format. Please use HH:MM format.")

def get_time_slots(start_time: str, end_time: str, interval: int = 30) -> list[str]:
    """Generate time slots between start and end time."""
    start = parse_time_slot(start_time)
    end = parse_time_slot(end_time)
    
    slots = []
    current = start
    while current <= end:
        slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=interval)
    
    return slots

def is_valid_date(date_str: str) -> bool:
    """Check if date string is valid and not in the past."""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date.date() >= datetime.now().date()
    except ValueError:
        return False