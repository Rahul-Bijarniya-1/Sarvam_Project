import json

class PromptTemplates:
    def __init__(self):
        # Define available cuisines based on actual data
        self.AVAILABLE_CUISINES = {
            "Available Cuisines": [
                "American",
                "Chinese",
                "French",
                "Indian",
                "Italian",
                "Japanese",
                "Mexican",
                "Thai"
            ]
        }

        # Define locations based on actual data
        self.LOCATIONS = [
            "Downtown",
            "East Side",
            "Midtown",
            "Uptown",
            "Waterfront",
            "West End"
        ]

        # Define price ranges
        self.PRICE_RANGES = {
            1: "$ (Budget-friendly)",
            2: "$$ (Moderate)",
            3: "$$$ (Upscale)",
            4: "$$$$ (Fine Dining)"
        }

        # Define table types
        self.TABLE_TYPES = {
            2: "Couple Table (2 seats)",
            4: "Family Table (4 seats)",
            6: "Group Table (6 seats)",
            8: "Large Group Table (8 seats)"
        }

        self.DATE_FORMAT_RULES = """
Date Format Requirements:
- Use specific date format: MM/DD/YYYY (e.g., 03/15/2024)
- Or use relative dates: "today", "tomorrow"
- For days of the week, must include date (e.g., "Friday 03/15/2024")
- Date must be within 30 days from today
"""

        self.SYSTEM_PROMPT = f"""You are a restaurant reservation assistant for FoodieSpot. You must strictly maintain context and track the active restaurant throughout the conversation.

IMPORTANT: NEVER show internal context or system state to the user. Keep all context tracking internal.

{self.DATE_FORMAT_RULES}

CONTEXT MAINTENANCE RULES (INTERNAL ONLY):
1. Maintain active restaurant being discussed
2. Track current reservation details
3. Keep conversation history
4. Monitor special requests
5. NEVER expose these tracking details to the user

Available Commands (TO SHOW TO USERS):

1. SEARCH RESTAURANTS
   Format: "search [cuisine/location/price range]"
   Examples:
   - "search Italian restaurants"
   - "search restaurants in Downtown"
   - "search budget-friendly restaurants"
   - "search Italian restaurants in Downtown under $$"

2. CHECK AVAILABILITY
   Format: "check availability [restaurant name] [date in MM/DD/YYYY] [time] [party size]"
   Examples:
   - "check availability at La Pasta for 03/15/2024 at 7:00 PM for 4 people"
   - "check availability at Curry House for tomorrow at 6:30 PM for 6 people"
   
   Note: 
   - Date must be specified in MM/DD/YYYY format or as "today"/"tomorrow"
   - Time must be in HH:MM AM/PM format
   - Party size must match available table types (2, 4, 6, or 8 people)
   - Reservations available during operating hours only

3. MAKE RESERVATION
   Format: "reserve [restaurant name] [date in MM/DD/YYYY] [time] [party size] [special requests]"
   Examples:
   - "make a reservation at Miyabi for 03/15/2024 at 7:00 PM for 4 people"
   - "reserve a table at The Local for tomorrow at 6:00 PM for 6 people, birthday celebration"

4. ADD/MODIFY SPECIAL REQUESTS
   Format: "add special request to [restaurant name/reservation ID]: [request details]"
   Examples:
   - "add special request to reservation #1234: spicy food preference"
   - "update special request: need high chair for baby"
   
   Note: Special requests must be linked to a specific restaurant or reservation

5. CHECK MY RESERVATIONS
   Format: "show my reservations" or "view my bookings"
   - Shows all active reservations under your name

6. MODIFY RESERVATION
   Format: "modify reservation [reservation ID/restaurant name] [what to change]"
   Examples:
   - "change my reservation at La Pasta to 03/16/2024 8:00 PM"
   - "update party size for Miyabi reservation to 6 people"

7. CANCEL RESERVATION
   Format: "cancel reservation [reservation ID]"
   Example: "cancel my reservation #1234"

RESPONSE FORMATTING:
1. Only show relevant information to users
2. Keep all context tracking internal
3. Present information in a clean, user-friendly format
4. Never expose system state or tracking information

How can I assist you today?"""

    def _format_list(self, items):
        return "\n".join(f"- {item}" for item in items)

    def _format_price_ranges(self):
        return "\n".join(f"- {v}" for v in self.PRICE_RANGES.values())

    def _format_table_types(self):
        return "\n".join(f"- {v}" for v in self.TABLE_TYPES.values())

    def build_memory_prompt(self, message: str, conversation_state: 'ConversationState', customer_name: str) -> str:
        context = conversation_state.summarize_context()
        
        # This is internal context that should never be shown to users
        memory_prompt = f"""INTERNAL CONTEXT (NEVER SHOW TO USER):
Current Customer: {customer_name}
Active Restaurant: {context['active_restaurant'] or 'None'}
Pending Reservation: {'Yes' if context['pending_reservation'] else 'No'}
Last Restaurant: {context.get('last_restaurant') or 'None'}
Active Reservation ID: {context.get('active_reservation_id') or 'None'}

INTERNAL REQUIREMENTS:
1. Track context but never expose it
2. Maintain conversation state privately
3. Use context for decision making only
4. Keep all system state internal

Recent Preferences (INTERNAL):
{self._format_preferences(context['current_preferences'])}

Recent Conversation (INTERNAL):
{self._format_history(context['recent_interaction_summary'])}

Response Guidelines:
1. Address {customer_name} naturally without exposing context
2. Use tracked information for decisions only
3. Present only relevant details to user
4. Format responses cleanly without system information
5. Keep all tracking and context internal
"""
        return memory_prompt

    def _format_preferences(self, preferences: dict) -> str:
        if not preferences:
            return "No recent preferences found"
        
        return "\n".join([f"- {k}: {v}" for k, v in preferences.items()])

    def _format_history(self, history: list) -> str:
        if not history:
            return "No recent conversation history"
        
        return "\n".join([
            f"- {msg['sender'].title()}: {msg['message']}"
            for msg in history
        ])

    def format_user_response(self, response_type: str, details: dict) -> str:
        """Format responses to users without exposing internal context"""
        if response_type == "reservation_confirmation":
            return f"""Thank you! Here are your reservation details:

Restaurant: {details['restaurant']}
Date: {details['date']}
Time: {details['time']}
Party Size: {details['party_size']}
{f"Special Requests: {details['special_requests']}" if details.get('special_requests') else ""}
Reservation ID: #{details['reservation_id']}"""

        elif response_type == "special_request_update":
            return f"""I've updated your special request for {details['restaurant']}.

Your reservation details:
Date: {details['date']}
Time: {details['time']}
Party Size: {details['party_size']}
Special Requests: {details['special_requests']}
Reservation ID: #{details['reservation_id']}"""

        # Add more response formats as needed...

    ERROR_RESPONSE = """I need some additional information to help you:

Please provide:
1. Which restaurant you'd like to make changes to
2. The specific details you want to modify

For example:
"add special request to La Pasta: spicy food preference"
"""
