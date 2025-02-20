from dataclasses import dataclass
from datetime import datetime

@dataclass
class Reservation:
    id: str
    restaurant_id: str
    customer_id: str
    date: str
    time: str
    party_size: int
    status: str  # confirmed, cancelled, completed
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "restaurant_id": self.restaurant_id,
            "customer_id": self.customer_id,
            "date": self.date,
            "time": self.time,
            "party_size": self.party_size,
            "status": self.status
        }