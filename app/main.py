
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from core.llm_manager import LLMManager
from core.tool_manager import ToolManager
from utils.formatters import format_restaurant_info

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'tool_manager' not in st.session_state:
        st.session_state.tool_manager = ToolManager()
    if 'llm_manager' not in st.session_state:
        st.session_state.llm_manager = LLMManager()

def main():
    st.title("🍽️ FoodieSpot Reservations")
    
    initialize_session_state()
    
    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("How can I help you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Get bot response
        with st.chat_message("assistant"):
            response = st.session_state.llm_manager.process_message(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()