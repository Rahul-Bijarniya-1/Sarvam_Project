import pytest
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from tools.search import search_restaurants
from data.sample_data_generator import generate_sample_restaurants

@pytest.fixture
def sample_data(monkeypatch):
    restaurants = generate_sample_restaurants(10)
    def mock_get_restaurants():
        return restaurants
    monkeypatch.setattr('tools.search.get_restaurants', mock_get_restaurants)
    return restaurants

def test_search_by_cuisine(sample_data):
    results = search_restaurants(cuisine="Italian")
    assert all(r.cuisine == "Italian" for r in results)

def test_search_by_location(sample_data):
    results = search_restaurants(location="Downtown")
    assert all("Downtown" in r.location for r in results)

def test_search_by_price_range(sample_data):
    results = search_restaurants(price_range=2)
    assert all(r.price_range <= 2 for r in results)

def test_search_by_seating(sample_data):
    results = search_restaurants(seating_required=6)
    assert all(any(t.seats >= 6 for t in r.tables) for r in results)