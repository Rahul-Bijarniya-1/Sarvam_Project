import pytest
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from tools.reservation import make_reservation, modify_reservation, cancel_reservation
from models.reservation import Reservation

@pytest.fixture
def sample_reservation():
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    return Reservation(
        id="test_res",
        restaurant_id="test_rest",
        customer_id="test_cust",
        date=tomorrow,
        time="18:00",
        party_size=4,
        status="confirmed"
    )

def test_make_reservation(monkeypatch):
    def mock_check_availability(*args, **kwargs):
        return ["18:00"]
    
    def mock_save_reservation(reservation):
        pass
    
    monkeypatch.setattr('tools.reservation.check_availability', mock_check_availability)
    monkeypatch.setattr('tools.reservation.save_reservation', mock_save_reservation)
    
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    reservation = make_reservation(
        restaurant_id="test_rest",
        date=tomorrow,
        time="18:00",
        party_size=4,
        customer_details={"id": "test_cust"}
    )
    
    assert reservation is not None
    assert reservation.status == "confirmed"
    assert reservation.party_size == 4

def test_modify_reservation(sample_reservation, monkeypatch):
    def mock_get_reservations():
        return [sample_reservation]
    
    def mock_check_availability(*args, **kwargs):
        return ["19:00"]
    
    def mock_update_reservation(reservation):
        pass
    
    monkeypatch.setattr('tools.reservation.get_reservations', mock_get_reservations)
    monkeypatch.setattr('tools.reservation.check_availability', mock_check_availability)
    monkeypatch.setattr('tools.reservation.update_reservation', mock_update_reservation)
    
    modified = modify_reservation(
        reservation_id="test_res",
        new_time="19:00"
    )
    
    assert modified is not None
    assert modified.time == "19:00"

def test_cancel_reservation(sample_reservation, monkeypatch):
    def mock_get_reservations():
        return [sample_reservation]
    
    def mock_update_reservation(reservation):
        pass
    
    monkeypatch.setattr('tools.reservation.get_reservations', mock_get_reservations)
    monkeypatch.setattr('tools.reservation.update_reservation', mock_update_reservation)
    
    result = cancel_reservation("test_res")
    assert result is True