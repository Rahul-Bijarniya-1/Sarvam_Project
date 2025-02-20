from collections import deque
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

class ConversationState:
    def __init__(self):
        self.history = deque(maxlen=7)  # Store last 7 interactions
        self.preferences = {}  # Stores user preferences
        self.active_context = {
            'current_restaurant': None,
            'reservation_attempt': {},
            'modification_request': None,
            'last_search_results': [],
            'last_interaction_time': None
        }
    
    def add_message(self, sender: str, message: str) -> None:
        """Add a message to the conversation history."""
        timestamp = datetime.now()
        self.history.append({
            "sender": sender,
            "message": message,
            "timestamp": timestamp
        })
        self.active_context['last_interaction_time'] = timestamp

    def update_preference(self, key: str, value: Any) -> None:
        """Update user preferences with timestamp."""
        self.preferences[key] = {
            'value': value,
            'timestamp': datetime.now()
        }

    def set_active_restaurant(self, restaurant_id: str) -> None:
        """Set the currently discussed restaurant."""
        self.active_context['current_restaurant'] = restaurant_id

    def update_reservation_attempt(self, details: Dict[str, Any]) -> None:
        """Update current reservation attempt details."""
        self.active_context['reservation_attempt'] = {
            **self.active_context['reservation_attempt'],
            **details,
            'last_updated': datetime.now()
        }

    def serialize_memory(self) -> Dict:
        """Serialize the current memory state."""
        return {
            "history": list(self.history),
            "preferences": self.preferences,
            "active_context": {
                k: v for k, v in self.active_context.items()
                if k != 'last_interaction_time' or v is None or isinstance(v, (str, int, float, bool, list, dict))
            }
        }

    def summarize_context(self) -> Dict:
        """Create a summary of current context."""
        active_prefs = {
            k: v['value'] for k, v in self.preferences.items()
            if not self.is_preference_stale(k)
        }
        
        recent_msgs = self.get_recent_history(3)
        
        return {
            "current_preferences": active_prefs,
            "recent_interaction_summary": recent_msgs,
            "active_restaurant": self.active_context['current_restaurant'],
            "pending_reservation": bool(self.active_context['reservation_attempt'])
        }

    def cleanup_stale_preferences(self, hours: int = 24) -> None:
        """Remove preferences older than specified hours."""
        current_time = datetime.now()
        self.preferences = {
            k: v for k, v in self.preferences.items()
            if (current_time - v['timestamp']).total_seconds() / 3600 < hours
        }

    def is_preference_stale(self, preference_key: str, hours: int = 24) -> bool:
        """Check if a specific preference is stale."""
        if preference_key not in self.preferences:
            return True
            
        current_time = datetime.now()
        pref_time = self.preferences[preference_key]['timestamp']
        return (current_time - pref_time).total_seconds() / 3600 >= hours

    def is_context_stale(self, minutes: int = 30) -> bool:
        """Check if conversation context is stale."""
        if not self.active_context['last_interaction_time']:
            return True
        
        time_diff = datetime.now() - self.active_context['last_interaction_time']
        return time_diff.total_seconds() / 60 > minutes

    def get_recent_history(self, num: int = 5) -> List[Dict[str, Any]]:
        """Get recent conversation history."""
        history_list = list(self.history)[-num:]
        return [
            {
                "sender": msg["sender"],
                "message": msg["message"],
                "timestamp": msg["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            }
            for msg in history_list
        ]

    def get_active_preferences(self) -> Dict[str, Any]:
        """Get non-stale preferences."""
        return {
            k: v['value'] for k, v in self.preferences.items()
            if not self.is_preference_stale(k)
        }

    def clear_reservation_attempt(self) -> None:
        """Clear the current reservation attempt."""
        self.active_context['reservation_attempt'] = {}

    def reset_context(self) -> None:
        """Reset the active context when conversation becomes stale."""
        self.active_context = {
            'current_restaurant': None,
            'reservation_attempt': {},
            'modification_request': None,
            'last_search_results': [],
            'last_interaction_time': None
        } 