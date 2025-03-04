from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class Customer:
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    preferences: Dict[str, str] = None
    
    def __post_init__(self):
        if self.preferences is None:
            self.preferences = {}
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "preferences": self.preferences
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Customer':
        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            phone=data.get("phone"),
            preferences=data.get("preferences", {})
        )