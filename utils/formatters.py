from models.restaurant import Restaurant
from models.reservation import Reservation

def format_restaurant_info(restaurant: Restaurant) -> str:
    """Format restaurant information for display."""
    return f"""
    **{restaurant.name}** - {restaurant.cuisine}
    📍 {restaurant.location} | 💰 {'$' * restaurant.price_range} | ⭐ {restaurant.rating}
    Capacity: {restaurant.seating_capacity} seats
    {restaurant.description}
    """

def format_reservation_info(reservation: Reservation) -> str:
    """Format reservation information for display."""
    return f"""
    **Reservation Details**
    📅 Date: {reservation.date}
    🕒 Time: {reservation.time}
    👥 Party Size: {reservation.party_size}
    Status: {reservation.status.capitalize()}
    """