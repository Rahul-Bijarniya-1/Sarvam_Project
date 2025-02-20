from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Table:
    id: str
    seats: int
    description: str

@dataclass
class Restaurant:
    id: str
    name: str
    location: str
    cuisine: str
    price_range: int
    seating_capacity: int
    tables: List[Table]
    operating_hours: Dict[str, Dict[str, str]]
    rating: float
    description: str