"""Table Turner - Enhanced Streamlit app with voice features and specific flow."""
import streamlit as st
import os
from dotenv import load_dotenv
import sys
from datetime import datetime

# Add paths
sys.path.append(os.path.dirname(__file__))

from data.table_turner_db import TableTurnerDatabase
from agent.table_turner_agent import TableTurnerAgent

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Table Turner - GoodFoods",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .logo-text {
        font-size: 3rem;
        color: white;
        font-weight: bold;
        margin: 0;
    }
    .tagline {
        font-size: 1.2rem;
        color: #f0f0f0;
        margin: 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        position: relative;
    }
    .user-message {
        background-color: #E3F2FD;
        margin-left: 3rem;
        border-left: 4px solid #2196F3;
    }
    .assistant-message {
        background-color: #F5F5F5;
        margin-right: 3rem;
        border-left: 4px solid #667eea;
    }
    .volume-icon {
        position: absolute;
        right: 10px;
        top: 10px;
        cursor: pointer;
        font-size: 1.2rem;
    }
    .input-option-button {
        background-color: #667eea;
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 5px;
        border: none;
        font-size: 1rem;
        cursor: pointer;
        margin: 0.5rem;
    }
    .stButton>button {
        background-color: #667eea;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        border: none;
        font-size: 1rem;
    }
    .stButton>button:hover {
        background-color: #764ba2;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if "database" not in st.session_state:
        st.session_state.database = TableTurnerDatabase()
    
    if "agent" not in st.session_state:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            st.session_state.agent = TableTurnerAgent(api_key, st.session_state.database)
            if "messages" not in st.session_state:
                st.session_state.messages = []
                # Add initial greeting
                greeting = st.session_state.agent.start_chat()
                st.session_state.messages.append({"role": "assistant", "content": greeting})
        else:
            st.session_state.agent = None
    
    if "input_mode" not in st.session_state:
        st.session_state.input_mode = "text"  # "text" or "voice"
    
    if "api_key_set" not in st.session_state:
        st.session_state.api_key_set = bool(os.getenv("GEMINI_API_KEY"))

def text_to_speech_button(text: str, message_id: int):
    """Create a volume icon that reads text when clicked."""
    # Using HTML audio player (browser's built-in TTS)
    # Note: For production, you'd use a proper TTS service
    st.markdown(f"""
        <span class="volume-icon" onclick="responsiveVoice.speak('{text.replace("'", "\\'")}', 'UK English Female');" title="Listen to message">
            🔊
        </span>
    """, unsafe_allow_html=True)

def main():
    """Main application."""
    initialize_session_state()
    
    # Header with logo
    st.markdown("""
    <div class="main-header">
        <h1 class="logo-text">🍽️ Table Turner</h1>
        <p class="tagline">by GoodFoods - Your Smart Dining Companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API key
    if not st.session_state.api_key_set:
        st.warning("⚠️ Please set your Gemini API Key to use Table Turner.")
        api_key_input = st.text_input("Enter Gemini API Key", type="password")
        if st.button("Set API Key"):
            if api_key_input:
                os.environ["GEMINI_API_KEY"] = api_key_input
                st.session_state.agent = TableTurnerAgent(api_key_input, st.session_state.database)
                greeting = st.session_state.agent.start_chat()
                st.session_state.messages = [{"role": "assistant", "content": greeting}]
                st.session_state.api_key_set = True
                st.rerun()
        return
    
    # Add ResponsiveVoice for text-to-speech
    st.markdown("""
    <script src="https://code.responsivevoice.org/responsivevoice.js?key=YOUR_KEY"></script>
    """, unsafe_allow_html=True)
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for idx, message in enumerate(st.session_state.messages):
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    👤 <strong>You:</strong> {content}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    🤖 <strong>Table Turner:</strong> {content}
                    <span class="volume-icon" title="Listen to message">🔊</span>
                </div>
                """, unsafe_allow_html=True)
    
    # Input mode selection
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.write("**Choose your input method:**")
    
    with col2:
        if st.button("📝 Text Input", use_container_width=True):
            st.session_state.input_mode = "text"
    
    with col3:
        if st.button("🎤 Voice Input", use_container_width=True):
            st.session_state.input_mode = "voice"
            st.info("Voice input feature coming soon! Please use text for now.")
    
    # Chat input
    st.markdown("---")
    
    if st.session_state.input_mode == "text":
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Your message:",
                key="user_input",
                placeholder="Type your message here...",
                label_visibility="collapsed"
            )
        
        with col2:
            send_button = st.button("Send 📤", use_container_width=True)
        
        # Handle message sending
        if send_button and user_input:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get agent response
            with st.spinner("🤔 Thinking..."):
                response = st.session_state.agent.send_message(user_input)
            
            # Add assistant message
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Rerun to update chat
            st.rerun()
    
    # Footer with info
    st.markdown("---")
    with st.expander("ℹ️ About Table Turner"):
        st.markdown("""
        ### How to Use Table Turner
        
        1. **Provide your phone number** to get started
        2. **Tell us your preference** - specific restaurant or need suggestions
        3. **Choose date and time** - bookings available up to 3 days in advance
        4. **Confirm your reservation** - get a unique reservation ID
        5. **Make another booking** or explore more options
        
        ### Booking Rules
        - 📅 Bookings can be made up to **3 days in advance**
        - ⏰ Time slots available from **11:00 AM to 11:00 PM**
        - 🪑 Table sizes: 2, 4, or 6 people
        - 🕐 Reservations in **30-minute slots**
        
        ### Features
        - 🔊 Voice playback for all messages
        - 📝 Text and voice input options
        - 🎯 Smart date parsing (today, tomorrow, next Saturday)
        - 💡 Personalized recommendations
        - 📱 User profile with reservation history
        
        Powered by Google Gemini AI | Built with ❤️ for GoodFoods
        """)
    
    # Context display (for debugging - remove in production)
    if st.checkbox("Show Debug Info", value=False):
        user_context = st.session_state.agent.get_user_context()
        st.json(user_context)

if __name__ == "__main__":
    main()
