"""Table Turner V2 - Production-ready with SQLite database."""
import streamlit as st
import os
from dotenv import load_dotenv
import sys

sys.path.append(os.path.dirname(__file__))

from data.database import TableTurnerDB
from agent.table_turner_agent_v2 import TableTurnerAgentV2

load_dotenv()

st.set_page_config(
    page_title="Table Turner - GoodFoods",
    page_icon="🍽️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .logo-text {
        font-size: 3.5rem;
        color: white;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    .tagline {
        font-size: 1.3rem;
        color: #f0f0f0;
        margin: 0.5rem 0 0 0;
    }
    .chat-message {
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        position: relative;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .user-message {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        margin-left: 3rem;
        border-left: 4px solid #2196F3;
    }
    .assistant-message {
        background: linear-gradient(135deg, #F5F5F5 0%, #EEEEEE 100%);
        margin-right: 3rem;
        border-left: 4px solid #667eea;
    }
    .volume-icon {
        cursor: pointer;
        font-size: 1.1rem;
        opacity: 0.6;
        margin-left: 0.5rem;
    }
    .volume-icon:hover {
        opacity: 1;
    }
    .input-mode-btn {
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 500;
    }
    .stButton>button {
        background-color: #667eea;
        color: white;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #764ba2;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .stat-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state."""
    if "database" not in st.session_state:
        st.session_state.database = TableTurnerDB()
        st.session_state.database.seed_data()
    
    if "agent" not in st.session_state:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            st.session_state.agent = TableTurnerAgentV2(api_key, st.session_state.database)
            if "messages" not in st.session_state:
                st.session_state.messages = []
                greeting = st.session_state.agent.start_chat()
                st.session_state.messages.append({"role": "assistant", "content": greeting})
        else:
            st.session_state.agent = None
    
    if "input_mode" not in st.session_state:
        st.session_state.input_mode = "text"
    
    if "api_key_set" not in st.session_state:
        st.session_state.api_key_set = bool(os.getenv("GEMINI_API_KEY"))

def main():
    """Main application."""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="logo-text">🍽️ Table Turner</h1>
        <p class="tagline">by GoodFoods - Your Smart Dining Companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API key
    if not st.session_state.api_key_set:
        st.warning("⚠️ Please set your Gemini API Key to use Table Turner.")
        col1, col2 = st.columns([3, 1])
        with col1:
            api_key_input = st.text_input("Enter Gemini API Key", type="password")
        with col2:
            if st.button("Set API Key"):
                if api_key_input:
                    os.environ["GEMINI_API_KEY"] = api_key_input
                    st.session_state.agent = TableTurnerAgentV2(api_key_input, st.session_state.database)
                    greeting = st.session_state.agent.start_chat()
                    st.session_state.messages = [{"role": "assistant", "content": greeting}]
                    st.session_state.api_key_set = True
                    st.rerun()
        st.info("🔑 Get your free API key from: https://aistudio.google.com/apikey")
        return
    
    # Stats bar
    stats = st.session_state.database.get_stats()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="stat-card">
            <h3>🍽️ {stats['restaurants']}</h3>
            <p>Restaurants</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="stat-card">
            <h3>👥 {stats['users']}</h3>
            <p>Users</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="stat-card">
            <h3>📅 {stats['active_reservations']}</h3>
            <p>Active Bookings</p>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="stat-card">
            <h3>🪑 {stats['total_tables']}</h3>
            <p>Total Tables</p>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chat messages
    chat_container = st.container()
    with chat_container:
        for idx, message in enumerate(st.session_state.messages):
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 You:</strong> {content}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 Table Turner:</strong> {content}
                    <span class="volume-icon" title="Click to hear message">🔊</span>
                </div>
                """, unsafe_allow_html=True)
    
    # Input section
    st.markdown("---")
    
    # Input mode selection
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown("**Choose input method:**")
    with col2:
        if st.button("📝 Text", use_container_width=True, type="primary" if st.session_state.input_mode == "text" else "secondary"):
            st.session_state.input_mode = "text"
            st.rerun()
    with col3:
        if st.button("🎤 Voice", use_container_width=True, type="primary" if st.session_state.input_mode == "voice" else "secondary"):
            st.info("🎤 Voice input coming soon! Please use text for now.")
    
    # Text input
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
        
        # Handle sending
        if send_button and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            with st.spinner("🤔 Processing..."):
                response = st.session_state.agent.send_message(user_input)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    # Sidebar
    with st.sidebar:
        st.header("📊 System Statistics")
        st.json(stats)
        
        st.divider()
        
        st.header("💡 Quick Tips")
        st.markdown("""
        - Bookings up to **3 days** in advance
        - Time slots: **11:00 AM - 11:00 PM**
        - Tables: **2, 4, or 6 people**
        - **30-minute** slot intervals
        """)
        
        st.divider()
        
        if st.button("🔄 Start New Conversation"):
            st.session_state.messages = []
            greeting = st.session_state.agent.reset_conversation()
            st.session_state.messages.append({"role": "assistant", "content": greeting})
            st.rerun()
        
        if st.button("🗑️ Clear All Data"):
            # Reset database
            if os.path.exists("table_turner.db"):
                os.remove("table_turner.db")
            st.session_state.database = TableTurnerDB()
            st.session_state.database.seed_data()
            st.session_state.messages = []
            greeting = st.session_state.agent.reset_conversation()
            st.session_state.messages.append({"role": "assistant", "content": greeting})
            st.success("Database reset successfully!")
            st.rerun()
    
    # Footer
    st.markdown("---")
    with st.expander("ℹ️ About Table Turner"):
        st.markdown("""
        ### 🎯 How It Works
        
        1. **Authentication**: Provide your mobile number
        2. **Personalization**: Returning users get customized greetings
        3. **Choose Restaurant**: Specific restaurant or get suggestions
        4. **Select Date/Time**: Natural language date parsing
        5. **Confirm Booking**: Get unique reservation ID
        6. **Multiple Bookings**: Book multiple restaurants in one session
        
        ### 🏗️ Technical Architecture
        
        - **Database**: SQLite with proper indexing
        - **AI**: Google Gemini 1.5 Flash with function calling
        - **Frontend**: Streamlit with modern UI
        - **Scalability**: Indexed queries, connection pooling ready
        
        ### 📊 Database Schema
        
        - **Users**: Phone-based authentication
        - **Restaurants**: 10+ locations (expandable)
        - **Tables**: Physical table management (2, 4, 6 seats)
        - **Time Slots**: 30-minute intervals
        - **Reservations**: Full booking history with indexing
        
        ### 🚀 Performance Optimizations
        
        - ✅ Indexed queries on common filters
        - ✅ Composite indexes for date-time lookups
        - ✅ Connection management with context managers
        - ✅ Transaction safety for concurrent bookings
        - ✅ Optimized availability checking algorithm
        
        **Built for Sarvam AI Challenge** | Powered by Gemini AI
        """)
    
    # Debug info
    if st.checkbox("🐛 Show Debug Info"):
        user_context = st.session_state.agent.get_user_context()
        st.json(user_context)

if __name__ == "__main__":
    main()
