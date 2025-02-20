from pathlib import Path
import sys
import pytest
from datetime import datetime, timedelta

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from tools.availability import check_availability
from models.restaurant import Restaurant, Table

@pytest.fixture
def sample_restaurant():
    return Restaurant(
        id="test_rest",
        name="Test Restaurant",
        location="Downtown",
        cuisine="Italian",
        price_range=2,
        seating_capacity=20,
        tables=[
            Table(id="T1", seats=4, description="4-seat table"),
            Table(id="T2", seats=6, description="6-seat table")
        ],
        operating_hours={
            "Monday": {"open": "11:00", "close": "22:00"},
            "Tuesday": {"open": "11:00", "close": "22:00"},
            "Wednesday": {"open": "11:00", "close": "22:00"},
            "Thursday": {"open": "11:00", "close": "22:00"},
            "Friday": {"open": "11:00", "close": "23:00"},
            "Saturday": {"open": "11:00", "close": "23:00"},
            "Sunday": {"open": "11:00", "close": "22:00"}
        },
        rating=4.5,
        description="Test restaurant"
    )

def test_check_availability_basic(sample_restaurant, monkeypatch):
    def mock_get_restaurants():
        return [sample_restaurant]
    
    def mock_get_reservations():
        return []
    
    monkeypatch.setattr('tools.availability.get_restaurants', mock_get_restaurants)
    monkeypatch.setattr('tools.availability.get_reservations', mock_get_reservations)
    
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    available_times = check_availability(
        restaurant_id="test_rest",
        date=tomorrow,
        time="18:00",
        party_size=4
    )
    
    assert len(available_times) > 0
    assert "18:00" in available_times

def test_check_availability_full_booking(sample_restaurant, monkeypatch):
    def mock_get_restaurants():
        return [sample_restaurant]
    
    from models.reservation import Reservation
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    def mock_get_reservations():
        return [
            Reservation(
                id="res1",
                restaurant_id="test_rest",
                customer_id="cust1",
                date=tomorrow,
                time="18:00",
                party_size=4,
                status="confirmed"
            ),
            Reservation(
                id="res2",
                restaurant_id="test_rest",
                customer_id="cust2",
                date=tomorrow,
                time="18:00",
                party_size=6,
                status="confirmed"
            )
        ]
    
    monkeypatch.setattr('tools.availability.get_restaurants', mock_get_restaurants)
    monkeypatch.setattr('tools.availability.get_reservations', mock_get_reservations)
    
    available_times = check_availability(
        restaurant_id="test_rest",
        date=tomorrow,
        time="18:00",
        party_size=4
    )
    
    assert "18:00" not in available_times