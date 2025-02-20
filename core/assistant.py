import json
from foodiespot.core.prompt_templates import PromptTemplates
from foodiespot.core.conversation_state import ConversationState
from foodiespot.core.tool_manager import ToolManager
from foodiespot.core.llm_manager import LLMManager
from typing import List, Dict, Optional, Tuple
from datetime import datetime

class FoodieSpotAssistant:
    def __init__(self):
        self.conversation_state = ConversationState()
        self.tool_manager = ToolManager()
        self.llm_manager = LLMManager()
        self.prompt_templates = PromptTemplates()

    def update_preferences_based_on_input(self, user_message: str) -> None:
        """Update preferences based on user input."""
        # Convert to lowercase for case-insensitive matching
        message_lower = user_message.lower()
        
        # Define valid options
        cuisines = {
            "italian": "Italian",
            "chinese": "Chinese",
            "mexican": "Mexican",
            "indian": "Indian"
        }
        
        locations = {
            "downtown": "Downtown",
            "uptown": "Uptown",
            "suburbs": "Suburbs"
        }
        
        price_ranges = {
            "low": "low",
            "medium": "medium",
            "high": "high"
        }

        # Check for cuisine
        for key, value in cuisines.items():
            if key in message_lower:
                self.conversation_state.update_preference("cuisine", value)
                return  # Return after finding a match to avoid multiple updates

        # Check for location
        for key, value in locations.items():
            if key in message_lower:
                self.conversation_state.update_preference("location", value)
                return

        # Check for price range
        for key, value in price_ranges.items():
            if key in message_lower:
                self.conversation_state.update_preference("price_range", value)
                return

        # Check for seating information
        words = message_lower.split()
        for word in words:
            if word.isdigit():
                self.conversation_state.update_preference("seating", int(word))
                return

    def determine_next_question(self) -> str:
        """Determine the next question based on missing information."""
        preferences = self.conversation_state.get_active_preferences()
        
        if "cuisine" not in preferences:
            return "What type of cuisine are you interested in? (Italian, Chinese, Mexican, Indian)"
        
        if "location" not in preferences:
            return f"Great choice! For {preferences['cuisine']} cuisine, which area would you prefer? (Downtown, Uptown, Suburbs)"
        
        if "price_range" not in preferences:
            return f"And what's your preferred price range for {preferences['cuisine']} food in {preferences['location']}? (low, medium, high)"
        
        if "seating" not in preferences:
            return "How many people will be dining?"
        
        # If we have all preferences, proceed to restaurant search
        return self._generate_search_response(preferences)

    def _generate_search_response(self, preferences: dict) -> str:
        """Generate a response based on collected preferences."""
        return (
            f"I'll help you find a {preferences['cuisine']} restaurant in {preferences['location']} "
            f"within the {preferences['price_range']} price range. "
            "Let me search for available options..."
        )

    def process_user_input(self, user_message: str) -> str:
        """Process user input and generate appropriate response."""
        # Add message to history
        self.conversation_state.add_message("user", user_message)
        
        # Check if context is stale
        if self.conversation_state.is_context_stale():
            self.conversation_state.reset_context()
            return self._start_new_conversation()
        
        # Get current state and active restaurant
        current_restaurant = self.conversation_state.active_context.get('current_restaurant')
        preferences = self.conversation_state.get_active_preferences()
        
        # If there's an active restaurant, handle that flow
        if current_restaurant:
            return self._handle_active_restaurant_flow(user_message)
        
        # If we have all preferences but no restaurant selected
        if self._has_all_required_preferences(preferences):
            return self._handle_restaurant_search_flow(user_message)
            
        # Otherwise, collect missing preferences
        return self._collect_missing_preferences(user_message)

    def _start_new_conversation(self) -> str:
        """Start a fresh conversation."""
        return ("Welcome! I'll help you find the perfect restaurant. "
                "What type of cuisine are you interested in? (Italian, Chinese, Mexican, Indian, etc.)")

    def _has_all_required_preferences(self, preferences: Dict) -> bool:
        """Check if all required preferences are present."""
        required_preferences = {'cuisine', 'location', 'price_range', 'party_size'}
        return all(pref in preferences for pref in required_preferences)

    def _collect_missing_preferences(self, user_message: str) -> str:
        """Collect missing preferences in order."""
        preferences = self.conversation_state.get_active_preferences()
        
        # Try to extract preference from user message
        extracted_pref = self._extract_preference(user_message)
        if extracted_pref:
            key, value = extracted_pref
            self.conversation_state.update_preference(key, value)
            preferences = self.conversation_state.get_active_preferences()

        # Return next question based on missing preferences
        if 'cuisine' not in preferences:
            return ("What type of cuisine are you interested in? "
                   "(Italian, Chinese, Mexican, Indian, etc.)")
        elif 'location' not in preferences:
            return f"Great choice! Which area would you prefer for {preferences['cuisine']} cuisine? (Downtown, Uptown, Suburbs)"
        elif 'price_range' not in preferences:
            return "What's your preferred price range? (low, medium, high)"
        elif 'party_size' not in preferences:
            return "How many people will be dining?"
        
        return self._handle_restaurant_search_flow(user_message)

    def _handle_restaurant_search_flow(self, user_message: str) -> str:
        """Handle restaurant search and selection."""
        preferences = self.conversation_state.get_active_preferences()
        
        # If no search results yet, perform search
        if not self.conversation_state.active_context.get('last_search_results'):
            search_results = self.tool_manager.execute_tool(
                "search_restaurants",
                {
                    "cuisine": preferences['cuisine'],
                    "location": preferences['location'],
                    "price_range": preferences['price_range'],
                    "party_size": preferences['party_size']
                }
            )
            
            if not search_results:
                self.conversation_state.reset_context()
                return ("I couldn't find any restaurants matching your criteria. "
                       "Would you like to try different preferences?")
            
            self.conversation_state.active_context['last_search_results'] = search_results
            return self._format_search_results(search_results)
        
        # Handle restaurant selection
        try:
            selection = int(user_message.strip())
            results = self.conversation_state.active_context['last_search_results']
            
            if 1 <= selection <= len(results):
                selected_restaurant = results[selection - 1]
                self.conversation_state.set_active_restaurant(selected_restaurant['id'])
                return ("When would you like to make the reservation?\n"
                       "Please provide the date and time in format: YYYY-MM-DD HH:MM")
            else:
                return "Please select a valid restaurant number from the list above."
        except ValueError:
            return "Please select a restaurant by entering its number from the list."

    def _handle_active_restaurant_flow(self, user_message: str) -> str:
        """Handle reservation flow for selected restaurant."""
        try:
            date, time = user_message.split(' ')
            datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            
            availability = self.tool_manager.execute_tool(
                "check_availability",
                {
                    "restaurant_id": self.conversation_state.active_context['current_restaurant'],
                    "date": date,
                    "time": time,
                    "party_size": self.conversation_state.preferences['party_size']
                }
            )
            
            if availability:
                reservation = self.tool_manager.execute_tool(
                    "make_reservation",
                    {
                        "restaurant_id": self.conversation_state.active_context['current_restaurant'],
                        "date": date,
                        "time": time,
                        "party_size": self.conversation_state.preferences['party_size'],
                        "customer_details": {"id": "user_1"}
                    }
                )
                
                if reservation:
                    self.conversation_state.reset_context()
                    return f"Perfect! Your reservation is confirmed for {date} at {time}. Your reservation ID is {reservation.id}."
                
            return ("I apologize, but that time slot isn't available. "
                   "Would you like to see alternative times?")
        except ValueError:
            return ("Please provide the date and time in the correct format: YYYY-MM-DD HH:MM\n"
                   "For example: 2024-03-20 19:00")

    def _extract_preference(self, message: str) -> Optional[Tuple[str, str]]:
        """Extract preference from user message."""
        message = message.lower().strip()
        
        # Cuisine detection
        cuisines = {'italian', 'chinese', 'mexican', 'indian', 'japanese', 'thai'}
        for cuisine in cuisines:
            if cuisine in message:
                return ('cuisine', cuisine)
        
        # Location detection
        locations = {'downtown', 'uptown', 'suburbs'}
        for location in locations:
            if location in message:
                return ('location', location)
        
        # Price range detection
        if 'low' in message or 'cheap' in message:
            return ('price_range', 'low')
        elif 'high' in message or 'expensive' in message:
            return ('price_range', 'high')
        elif 'medium' in message or 'moderate' in message:
            return ('price_range', 'medium')
        
        # Party size detection
        try:
            numbers = [int(word) for word in message.split() if word.isdigit()]
            if numbers:
                return ('party_size', numbers[0])
        except ValueError:
            pass
        
        return None

    def _format_search_results(self, results: List[Dict]) -> str:
        """Format search results for display."""
        response = "I found these restaurants matching your criteria:\n\n"
        for idx, restaurant in enumerate(results, 1):
            response += f"{idx}. {restaurant['name']} - {restaurant['cuisine']}\n"
            response += f"   📍 {restaurant['location']} | 💰 {'$' * restaurant['price_range']} | ⭐ {restaurant['rating']}\n"
            response += f"   {restaurant['description']}\n\n"
        
        response += "Would you like to make a reservation at any of these restaurants? Please respond with the number of your choice."
        return response

    def call_model_api(self, prompt):
        # Simulated API call to the language model.
        print("Sending prompt to model:\n", prompt)
        # In production, replace the following with an actual API call.
        return "Simulated Assistant Response based on current conversation." 