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
    if 'customer_name' not in st.session_state:
        st.session_state.customer_name = None


def main():
    st.title("🍽️ FoodieSpot Reservations")
    
    initialize_session_state()
    
    # Customer Name Input
    if not st.session_state.customer_name:
        with st.form("customer_form"):
            customer_name = st.text_input("Please enter your name:")
            submit_button = st.form_submit_button("Start Chatting")
            if submit_button and customer_name:
                st.session_state.customer_name = customer_name
                st.experimental_rerun()
    else:
        st.write(f"Welcome back, {st.session_state.customer_name}! 👋")
        
        # Add a button to change name if needed
        if st.button("Change Name"):
            st.session_state.customer_name = None
            st.experimental_rerun()
    
    # Only show chat interface if customer name is provided
    if st.session_state.customer_name:
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
                response = st.session_state.llm_manager.process_message(prompt, st.session_state.customer_name)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()