from typing import Any, Dict, List, Optional
from models.restaurant import Restaurant
from models.reservation import Reservation
from tools.search import search_restaurants
from tools.availability import check_availability
from tools.reservation import (
    make_reservation,
    modify_reservation,
    cancel_reservation
)

class ToolManager:
    def __init__(self):
        self.tools = {
            "search_restaurants": search_restaurants,
            "check_availability": check_availability,
            "make_reservation": make_reservation,
            "modify_reservation": modify_reservation,
            "cancel_reservation": cancel_reservation
        }
    
    def execute_tool(self, tool_name: str, parameters: Dict) -> Any:
        """Execute a tool with given parameters."""
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")
            
        tool_func = self.tools[tool_name]
        return tool_func(**parameters)