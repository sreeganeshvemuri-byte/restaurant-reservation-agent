"""Streamlit app for Restaurant Reservation AI Agent."""
import streamlit as st
import os
from dotenv import load_dotenv
import sys

# Add paths
sys.path.append(os.path.dirname(__file__))

from data.restaurants import ReservationDatabase, RESTAURANTS
from agent.gemini_agent import RestaurantAgent

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="GoodFoods - AI Reservation Assistant",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4ECDC4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #E3F2FD;
        margin-left: 2rem;
    }
    .assistant-message {
        background-color: #F5F5F5;
        margin-right: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF6B6B;
        color: white;
    }
    .restaurant-card {
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if "database" not in st.session_state:
        st.session_state.database = ReservationDatabase()
    
    if "agent" not in st.session_state:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            st.session_state.agent = RestaurantAgent(api_key, st.session_state.database)
            st.session_state.agent.start_chat()
        else:
            st.session_state.agent = None
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "api_key_set" not in st.session_state:
        st.session_state.api_key_set = bool(os.getenv("GEMINI_API_KEY"))

def main():
    """Main application."""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🍽️ GoodFoods AI Reservation Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your intelligent companion for restaurant reservations</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📊 System Info")
        st.write(f"**Total Restaurants:** {len(RESTAURANTS)}")
        st.write(f"**Total Reservations:** {len(st.session_state.database.reservations)}")
        st.write(f"**Active Reservations:** {sum(1 for r in st.session_state.database.reservations if r['status'] == 'confirmed')}")
        
        st.divider()
        
        st.header("🔑 API Configuration")
        if not st.session_state.api_key_set:
            api_key_input = st.text_input("Enter Gemini API Key", type="password")
            if st.button("Set API Key"):
                if api_key_input:
                    os.environ["GEMINI_API_KEY"] = api_key_input
                    st.session_state.agent = RestaurantAgent(api_key_input, st.session_state.database)
                    st.session_state.agent.start_chat()
                    st.session_state.api_key_set = True
                    st.success("API Key set successfully!")
                    st.rerun()
                else:
                    st.error("Please enter an API key")
        else:
            st.success("✅ API Key configured")
            if st.button("Change API Key"):
                st.session_state.api_key_set = False
                st.session_state.agent = None
                st.rerun()
        
        st.divider()
        
        st.header("🍴 Quick Stats")
        cuisines = set(r["cuisine"] for r in RESTAURANTS)
        locations = set(r["location"] for r in RESTAURANTS)
        st.write(f"**Cuisines Available:** {len(cuisines)}")
        st.write(f"**Locations:** {len(locations)}")
        
        st.divider()
        
        st.header("💡 Example Queries")
        st.markdown("""
        - "I'm looking for Italian restaurants in Koramangala"
        - "Can you recommend a romantic restaurant?"
        - "I need a table for 4 on Friday at 7 PM"
        - "Show me vegetarian restaurants"
        - "What are the top-rated restaurants?"
        """)
        
        st.divider()
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            if st.session_state.agent:
                st.session_state.agent.start_chat()
            st.rerun()
    
    # Main chat interface
    if not st.session_state.api_key_set:
        st.warning("⚠️ Please set your Gemini API Key in the sidebar to start using the assistant.")
        st.info("👈 You can get a free API key from [Google AI Studio](https://aistudio.google.com/apikey)")
        return
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                st.markdown(f'<div class="chat-message user-message">👤 **You:** {content}</div>', 
                          unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message assistant-message">🤖 **Assistant:** {content}</div>', 
                          unsafe_allow_html=True)
    
    # Chat input
    st.divider()
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_input("Type your message here...", key="user_input", label_visibility="collapsed")
    
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
    
    # Quick action buttons
    st.divider()
    st.subheader("🚀 Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔍 Browse Restaurants", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Show me all available restaurants"})
            response = st.session_state.agent.send_message("Show me all available restaurants")
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        if st.button("⭐ Top Rated", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Show me the highest rated restaurants"})
            response = st.session_state.agent.send_message("Show me the highest rated restaurants")
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col3:
        if st.button("💝 Romantic Dining", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Recommend restaurants for a romantic dinner"})
            response = st.session_state.agent.send_message("Recommend restaurants for a romantic dinner")
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col4:
        if st.button("🥗 Vegetarian", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Show me vegetarian restaurants"})
            response = st.session_state.agent.send_message("Show me vegetarian restaurants")
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Powered by Google Gemini AI | Built for Sarvam AI Forward Deployed Engineer Challenge</p>
        <p>🍽️ Helping you find the perfect dining experience</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
