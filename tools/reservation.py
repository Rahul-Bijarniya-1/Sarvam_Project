from typing import Optional, Dict
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from models.reservation import Reservation
from tools.availability import check_availability
from data.data_manager import (
    get_reservations,
    save_reservation,
    update_reservation,
    get_restaurants
)
from utils.validators import validate_datetime, validate_party_size

def make_reservation(
    restaurant_id: str,
    date: str,
    time: str,
    party_size: int,
    customer_details: Dict
) -> Optional[Reservation]:
    """
    Create a new reservation if the slot is available.
    """
    # Validate inputs
    if not validate_party_size(party_size):
        raise ValueError("Invalid party size")
    
    valid, error = validate_datetime(date, time)
    if not valid:
        raise ValueError(error)

    # Check availability
    available_times = check_availability(restaurant_id, date, time, party_size)
    if time not in available_times:
        return None

    # Create reservation
    reservation_id = f"res_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    reservation = Reservation(
        id=reservation_id,
        restaurant_id=restaurant_id,
        customer_id=customer_details.get('id', 'unknown'),
        date=date,
        time=time,
        party_size=party_size,
        status='confirmed'
    )

    # Save reservation
    save_reservation(reservation)
    return reservation

def modify_reservation(
    reservation_id: str,
    new_time: Optional[str] = None,
    new_date: Optional[str] = None,
    new_party_size: Optional[int] = None
) -> Optional[Reservation]:
    """
    Modify an existing reservation.
    """
    # Get existing reservation
    reservations = get_reservations()
    reservation = next((r for r in reservations if r.id == reservation_id), None)
    if not reservation:
        return None

    # Update fields if provided
    if new_time:
        # Check availability for new time
        available_times = check_availability(
            reservation.restaurant_id,
            new_date or reservation.date,
            new_time,
            new_party_size or reservation.party_size
        )
        if new_time not in available_times:
            return None
        reservation.time = new_time
    
    if new_date:
        valid, error = validate_datetime(new_date, reservation.time)
        if not valid:
            raise ValueError(error)
        reservation.date = new_date
    
    if new_party_size:
        reservation.party_size = new_party_size

    # Update reservation
    update_reservation(reservation)
    return reservation

def cancel_reservation(reservation_id: str) -> bool:
    """
    Cancel an existing reservation.
    """
    reservations = get_reservations()
    reservation = next((r for r in reservations if r.id == reservation_id), None)
    if not reservation:
        return False

    reservation.status = "cancelled"
    update_reservation(reservation)
    return True