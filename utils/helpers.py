import re
import uuid
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

def generate_id(prefix: str = "") -> str:
    """Generate a unique ID with optional prefix."""
    return f"{prefix}{uuid.uuid4().hex[:8]}"

def extract_entities(text: str, entity_patterns: Dict[str, str]) -> Dict[str, str]:
    """Extract entities from text using regex patterns."""
    extracted = {}
    
    for entity_name, pattern in entity_patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            extracted[entity_name] = matches[0]
            
    return extracted

def extract_date_time(text: str) -> Dict[str, str]:
    """Extract date and time from text."""
    # Date patterns
    date_patterns = [
        r'(\d{4}-\d{2}-\d{2})',                    # YYYY-MM-DD
        r'(\d{1,2}/\d{1,2}/\d{2,4})',              # MM/DD/YYYY or M/D/YY
        r'(tomorrow|today|next week)',             # Relative dates
        r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?(?:\s*,\s*\d{4})?'  # Month Day, Year
    ]
    
    # Time patterns
    time_patterns = [
        r'(\d{1,2}:\d{2}(?:\s*[ap]m)?)',           # HH:MM or H:MM am/pm
        r'(\d{1,2}\s*[ap]m)',                      # H am/pm
        r'(\d{1,2})',                              # Just a number (context dependent)
        r'(noon|midnight)'                         # Special times
    ]
    
    result = {}
    
    # Extract date
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            raw_date = match.group(1).lower()
            # Convert relative dates
            if raw_date == 'today':
                result['date'] = datetime.now().strftime('%Y-%m-%d')
            elif raw_date == 'tomorrow':
                result['date'] = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            elif raw_date == 'next week':
                result['date'] = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
            else:
                # This is just a placeholder - actual implementation would need more complex date parsing
                result['date'] = raw_date
            break
    
    # Extract time
    for pattern in time_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            raw_time = match.group(1).lower()
            # Convert special times
            if raw_time == 'noon':
                result['time'] = '12:00'
            elif raw_time == 'midnight':
                result['time'] = '00:00'
            else:
                # This is just a placeholder - actual implementation would need more complex time parsing
                result['time'] = raw_time
            break
    
    return result

def format_currency(amount: float) -> str:
    """Format a number as currency."""
    return f"${amount:.2f}"

def parse_json_safely(json_str: str) -> Dict[str, Any]:
    """Parse JSON string with error handling."""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {}