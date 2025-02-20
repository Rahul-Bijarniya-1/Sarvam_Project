
import json
import os
from typing import List
from models.restaurant import Restaurant, Table
from models.reservation import Reservation

DATA_DIR = os.path.join(os.path.dirname(__file__))
RESTAURANTS_FILE = os.path.join(DATA_DIR, 'restaurants.json')
RESERVATIONS_FILE = os.path.join(DATA_DIR, 'reservations.json')

def load_json(filepath: str) -> List[dict]:
    """Load data from JSON file."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json(filepath: str, data: List[dict]):
    """Save data to JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def get_restaurants() -> List[Restaurant]:
    """Get list of restaurants."""
    data = load_json(RESTAURANTS_FILE)
    return [
        Restaurant(
            id=r['id'],
            name=r['name'],
            location=r['location'],
            cuisine=r['cuisine'],
            price_range=r['price_range'],
            seating_capacity=r['seating_capacity'],
            tables=[Table(**t) for t in r['tables']],
            operating_hours=r['operating_hours'],
            rating=r['rating'],
            description=r['description']
        )
        for r in data
    ]

def get_reservations() -> List[Reservation]:
    """Get list of reservations."""
    data = load_json(RESERVATIONS_FILE)
    return [Reservation(**r) for r in data]

def save_reservation(reservation: Reservation):
    """Save a new reservation."""
    reservations = get_reservations()
    reservations.append(reservation)
    save_json(RESERVATIONS_FILE, [r.to_dict() for r in reservations])

def update_reservation(updated_reservation: Reservation):
    """Update an existing reservation."""
    reservations = get_reservations()
    reservations = [
        updated_reservation if r.id == updated_reservation.id else r
        for r in reservations
    ]
    save_json(RESERVATIONS_FILE, [r.to_dict() for r in reservations])