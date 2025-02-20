from typing import List, Optional, Union, Dict
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from models.restaurant import Restaurant, Table
from data.data_manager import get_restaurants

def dict_to_restaurant(restaurant_dict: Dict) -> Restaurant:
    """Convert a dictionary to a Restaurant object."""
    tables = [Table(**table) if isinstance(table, dict) else table 
              for table in restaurant_dict.get('tables', [])]
    
    return Restaurant(
        id=restaurant_dict['id'],
        name=restaurant_dict['name'],
        location=restaurant_dict['location'],
        cuisine=restaurant_dict['cuisine'],
        price_range=restaurant_dict['price_range'],
        seating_capacity=restaurant_dict['seating_capacity'],
        tables=tables,
        operating_hours=restaurant_dict['operating_hours'],
        rating=restaurant_dict['rating'],
        description=restaurant_dict['description']
    )

def search_restaurants(
    cuisine: Optional[str] = None,
    location: Optional[str] = None,
    price_range: Optional[int] = None,
    seating_required: Optional[int] = None
) -> List[Restaurant]:
    """
    Search restaurants based on various criteria.
    """

    if price_range is not None and price_range < 1:
        raise ValueError("Price range must be a positive integer")
    if seating_required is not None and seating_required < 1:
        raise ValueError("Seating required must be a positive integer")

    restaurants = get_restaurants()

    # Convert dictionaries to Restaurant objects if needed
    results = [
        dict_to_restaurant(r) if isinstance(r, dict) else r 
        for r in restaurants
    ]

    if cuisine:
        results = [r for r in results if r.cuisine.lower() == cuisine.lower()]
    if location:
        results = [r for r in results if location.lower() in r.location.lower()]
    if price_range:
        results = [r for r in results if r.price_range <= price_range]
    if seating_required:
        results = [r for r in results if any(t.seats >= seating_required for t in r.tables)]

    return results