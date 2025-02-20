import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    LLM_API_URL = os.getenv("LLM_API_URL")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # Restaurant search settings
    MAX_SEARCH_RESULTS = 5
    
    # Reservation settings
    MIN_PARTY_SIZE = 1
    MAX_PARTY_SIZE = 20
    
    # Time slot settings
    TIME_SLOT_INTERVAL = 30  # minutes