from typing import List, Optional
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from models.restaurant import Restaurant
from data.data_manager import get_restaurants, get_reservations
from utils.validators import validate_datetime
from utils.time_utils import get_time_slots

def check_availability(
    restaurant_id: str,
    date: str,
    time: str,
    party_size: int
) -> List[str]:
    """
    Check available time slots for a given restaurant and party size.
    Returns list of available times around the requested time.
    """
    # Validate inputs
    valid, error = validate_datetime(date, time)
    if not valid:
        raise ValueError(error)

    # Get restaurant and current reservations
    restaurant = next((r for r in get_restaurants() if r.id == restaurant_id), None)
    if not restaurant:
        raise ValueError("Restaurant not found")

    # Check if restaurant has tables that can accommodate the party
    suitable_tables = [t for t in restaurant.tables if t.seats >= party_size]
    if not suitable_tables:
        return []

    # Get existing reservations for the date
    existing_reservations = [
        r for r in get_reservations()
        if r.restaurant_id == restaurant_id and r.date == date and r.status == "confirmed"
    ]

    # Get day of week for operating hours
    day_of_week = datetime.strptime(date, "%Y-%m-%d").strftime("%A")
    operating_hours = restaurant.operating_hours.get(day_of_week, {})
    if not operating_hours:
        return []

    # Generate time slots around requested time
    requested_dt = datetime.strptime(time, "%H:%M")
    start_time = (requested_dt - timedelta(hours=1)).strftime("%H:%M")
    end_time = (requested_dt + timedelta(hours=1)).strftime("%H:%M")
    
    # Ensure we're within operating hours
    start_time = max(start_time, operating_hours["open"])
    end_time = min(end_time, operating_hours["close"])
    
    potential_slots = get_time_slots(start_time, end_time)
    available_slots = []

    # Check each time slot
    for slot in potential_slots:
        total_seats_available = sum(table.seats for table in suitable_tables)
        
        # Subtract seats that are already reserved
        for reservation in existing_reservations:
            if reservation.time == slot:
                total_seats_available -= reservation.party_size

        # If we have enough seats available, add the slot
        if total_seats_available >= party_size:
            available_slots.append(slot)

    return available_slots

def is_table_available(
    table: 'Table',
    time_slot: str,
    existing_reservations: List['Reservation']
) -> bool:
    """Check if a specific table is available at a given time."""
    return not any(
        reservation.time == time_slot
        for reservation in existing_reservations
    )