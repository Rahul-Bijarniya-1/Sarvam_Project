import random
from typing import List
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from models.restaurant import Restaurant, Table
from data.data_manager import save_json, RESTAURANTS_FILE


def generate_sample_restaurants(count: int = 30) -> List[dict]:
    """Generate sample restaurant data."""
    cuisines = ['Italian', 'Japanese', 'Indian', 'Mexican', 'Chinese', 'French', 'Thai', 'American']
    locations = ['Downtown', 'Uptown', 'Midtown', 'West End', 'East Side', 'Waterfront']
    restaurant_names = {
        'Italian': ['La Pasta', 'Il Forno', 'Bella Italia', 'Gusto', 'Palazzo'],
        'Japanese': ['Sushi Ko', 'Ramen House', 'Sakura', 'Miyabi', 'Zen'],
        'Indian': ['Taj Mahal', 'Curry House', 'Spice Route', 'Delhi Kitchen', 'Mumbai Masala'],
        'Mexican': ['El Toro', 'La Cantina', 'Mexicana', 'Taqueria', 'Casa Verde'],
        'Chinese': ['Golden Dragon', 'Jade Palace', 'Dynasty', 'Red Lantern', 'Lucky Garden'],
        'French': ['Le Bistro', 'Petit Paris', 'La Maison', 'Cafe Rouge', 'L\'Escargot'],
        'Thai': ['Bangkok Kitchen', 'Thai Orchid', 'Lotus', 'Basil', 'Pepper Thai'],
        'American': ['The Grill', 'Liberty Diner', 'Main Street Cafe', 'Urban Kitchen', 'The Local']
    }

    restaurants = []
    for i in range(count):
        cuisine = random.choice(cuisines)
        base_name = random.choice(restaurant_names[cuisine])
        suffix = random.choice(['', ' Bistro', ' Kitchen', ' Restaurant', ' & Bar'])
        name = f"{base_name}{suffix}"

        # Generate tables
        tables = []
        table_configs = [(2, 'Couple'), (4, 'Family'), (6, 'Group'), (8, 'Large Group')]
        for size, type_name in table_configs:
            count = random.randint(2, 4)
            for j in range(count):
                tables.append({
                    'id': f"T{len(tables)+1}",
                    'seats': size,
                    'description': f"{size}-seat {type_name} Table"
                })

        # Generate operating hours
        operating_hours = {
            day: {
                "open": "11:00",
                "close": "22:00" if day not in ['Friday', 'Saturday'] else "23:00"
            }
            for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        }

        restaurant = {
            'id': f"rest_{i+1}",
            'name': name,
            'location': random.choice(locations),
            'cuisine': cuisine,
            'price_range': random.randint(1, 4),
            'seating_capacity': sum(t['seats'] for t in tables),
            'tables': tables,
            'operating_hours': operating_hours,
            'rating': round(random.uniform(3.5, 5.0), 1),
            'description': f"A {cuisine.lower()} restaurant offering authentic cuisine in a {random.choice(['casual', 'cozy', 'elegant', 'modern'])} atmosphere."
        }
        restaurants.append(restaurant)

    return restaurants

def create_sample_data():
    """Create and save sample restaurant data."""
    restaurants = generate_sample_restaurants()
    save_json(RESTAURANTS_FILE, restaurants)

if __name__ == "__main__":
    create_sample_data()