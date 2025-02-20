# core/llm_manager.py

import json
import requests
from typing import Dict, Any, Optional, List
from app.config import Config
from core.prompt_templates import PromptTemplates
from .conversation_state import ConversationState

class LLMManager:
    def __init__(self):
        self.api_key = Config.LLM_API_KEY
        self.api_url = Config.LLM_API_URL
        self.model = "llama3-8b-8192"
        self.conversation_state = ConversationState()
        self.prompt_templates = PromptTemplates()
    
    def process_message(self, user_message: str) -> str:
        """Process user message with memory context."""
        # Check for stale context
        if self.conversation_state.is_context_stale():
            self.conversation_state.reset_context()
            self.conversation_state.cleanup_stale_preferences()
        
        # Add user message to history
        self.conversation_state.add_message("user", user_message)
        
        # Build context-aware prompt
        context_summary = self.conversation_state.summarize_context()
        memory_prompt = self.prompt_templates.build_memory_prompt(
            message=user_message,
            conversation_state=self.conversation_state
        )
        
        # Prepare messages for LLM
        messages = [
            {"role": "system", "content": self.prompt_templates.SYSTEM_PROMPT},
            {"role": "system", "content": memory_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # Get LLM response
        try:
            response = self.call_llm_api(messages)
            self.conversation_state.add_message("assistant", response)
            return response
        except Exception as e:
            error_response = self.prompt_templates.ERROR_RESPONSE.format(
                error_type=type(e).__name__,
                recovery_suggestion="Let's start over with your request."
            )
            self.conversation_state.add_message("assistant", error_response)
            return error_response

    def call_llm_api(self, messages: List[Dict[str, str]]) -> str:
        """Call the LLM API with messages."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data
            )
            
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            print(f"Error calling LLM API: {e}")
            return "I apologize, but I'm having trouble processing your request right now."

    def parse_tool_call(self, response: str) -> Optional[Dict[str, Any]]:
        """Parse tool calling format from LLM response."""
        try:
            lines = response.strip().split('\n')
            tool_call = {}
            
            for line in lines:
                if line.startswith('TOOL:'):
                    tool_call['name'] = line.replace('TOOL:', '').strip()
                elif line.startswith('PARAMS:'):
                    params_str = line.replace('PARAMS:', '').strip()
                    tool_call['parameters'] = json.loads(params_str)
            
            return tool_call if 'name' in tool_call else None
            
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing tool call: {e}")
            return None