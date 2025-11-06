"""Table Turner V3 - Hybrid: Natural + Guided Conversation."""
import streamlit as st
import os
from dotenv import load_dotenv
import sys

sys.path.append(os.path.dirname(__file__))

from data.database import TableTurnerDB
from agent.hybrid_agent_v3 import HybridAgentV3

load_dotenv()

st.set_page_config(
    page_title="Table Turner V3 - Hybrid AI",
    page_icon="🍽️",
    layout="wide"
)

# Enhanced CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }
    .logo-text {
        font-size: 4rem;
        color: white;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    .version-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    .tagline {
        font-size: 1.4rem;
        color: #f0f0f0;
        margin: 0.5rem 0 0 0;
    }
    .chat-message {
        padding: 1.3rem;
        border-radius: 12px;
        margin-bottom: 1.2rem;
        position: relative;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        animation: slideIn 0.3s ease-out;
    }
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .user-message {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        margin-left: 2rem;
        border-left: 4px solid #2196F3;
    }
    .assistant-message {
        background: linear-gradient(135deg, #F5F5F5 0%, #EEEEEE 100%);
        margin-right: 2rem;
        border-left: 4px solid #667eea;
    }
    .volume-icon {
        cursor: pointer;
        font-size: 1.1rem;
        opacity: 0.5;
        margin-left: 0.8rem;
        transition: opacity 0.2s;
    }
    .volume-icon:hover {
        opacity: 1;
    }
    .stat-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border: 1px solid #e0e0e0;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
        margin: 0;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #666;
        margin: 0.3rem 0 0 0;
    }
    .stButton>button {
        background-color: #667eea;
        color: white;
        border-radius: 8px;
        padding: 0.7rem 2rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #764ba2;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    .feature-badge {
        display: inline-block;
        background: #4CAF50;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 12px;
        font-size: 0.8rem;
        margin: 0.2rem;
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
            st.session_state.agent = HybridAgentV3(api_key, st.session_state.database)
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
        <span class="version-badge">V3 - HYBRID AI 🚀</span>
        <p class="tagline">by GoodFoods - Conversational + Guided Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<span class="feature-badge">🧠 Smart Extraction</span>', unsafe_allow_html=True)
    with col2:
        st.markdown('<span class="feature-badge">💬 Natural Flow</span>', unsafe_allow_html=True)
    with col3:
        st.markdown('<span class="feature-badge">🗄️ SQLite DB</span>', unsafe_allow_html=True)
    with col4:
        st.markdown('<span class="feature-badge">⚡ Fast Path</span>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Check API key
    if not st.session_state.api_key_set:
        st.warning("⚠️ Please set your Gemini API Key")
        col1, col2 = st.columns([4, 1])
        with col1:
            api_key_input = st.text_input("Gemini API Key", type="password", placeholder="AIza...")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Set Key", use_container_width=True):
                if api_key_input:
                    os.environ["GEMINI_API_KEY"] = api_key_input
                    st.session_state.agent = HybridAgentV3(api_key_input, st.session_state.database)
                    greeting = st.session_state.agent.start_chat()
                    st.session_state.messages = [{"role": "assistant", "content": greeting}]
                    st.session_state.api_key_set = True
                    st.rerun()
        st.info("🔑 Get free key: https://aistudio.google.com/apikey")
        return
    
    # Stats
    stats = st.session_state.database.get_stats()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <p class="stat-value">{stats['restaurants']}</p>
            <p class="stat-label">🍽️ Restaurants</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <p class="stat-value">{stats['users']}</p>
            <p class="stat-label">👥 Users</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <p class="stat-value">{stats['active_reservations']}</p>
            <p class="stat-label">📅 Active Bookings</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <p class="stat-value">{stats['total_tables']}</p>
            <p class="stat-label">🪑 Tables</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chat messages
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
                <span class="volume-icon" title="Listen">🔊</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Input section
    st.markdown("---")
    
    # Quick examples
    with st.expander("💡 Try these example messages"):
        st.markdown("""
        **Fast Path (All info at once):**
        - "Book Bella Italia tomorrow at 7 PM for 4 people, I'm Raj 9876543210"
        - "9876543210 - want to book Spice Garden today 6 PM, party of 2, name is Sarah"
        
        **Guided (Step by step):**
        - "I want to make a reservation"
        - "9876543210"
        - "Looking for Italian food"
        
        **Natural Language:**
        - "Need a table for dinner tomorrow"
        - "Can I book for next Saturday evening?"
        - "Show me what's available"
        """)
    
    # Input mode
    col1, col2, col3 = st.columns([4, 1, 1])
    with col1:
        st.markdown("**Input method:**")
    with col2:
        if st.button("📝 Text", use_container_width=True):
            st.session_state.input_mode = "text"
    with col3:
        if st.button("🎤 Voice", use_container_width=True):
            st.info("Voice input coming soon!")
    
    # Chat input
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Your message:",
            key="user_input",
            placeholder="Type anything - I'll figure out what you need! 💬",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send 📤", use_container_width=True)
    
    if send_button and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.spinner("🤔 Processing..."):
            response = st.session_state.agent.send_message(user_input)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 V3 Hybrid Features")
        st.markdown("""
        ### 🧠 Smart Extraction
        - Understands full requests
        - Extracts phone, name, details
        - Fast-path for power users
        
        ### 💬 Natural Conversation
        - Not rigid step-by-step
        - Adapts to your style
        - Asks only what's missing
        
        ### ✅ Still Enforces Rules
        - 3-day booking limit
        - Phone authentication
        - Data validation
        
        ### 🔄 Hybrid Intelligence
        - Guided when you need it
        - Fast when you don't
        - Best of both worlds!
        """)
        
        st.divider()
        
        st.header("🎭 Conversation Modes")
        
        user_ctx = st.session_state.agent.get_user_context()
        
        if user_ctx.get("authenticated"):
            st.success(f"✅ Authenticated: {user_ctx.get('name')}")
            st.info(f"📱 Phone: {user_ctx.get('phone_number')}")
        else:
            st.warning("🔓 Not authenticated yet")
        
        if user_ctx.get("pending_booking"):
            st.info(f"📋 Booking in progress")
            with st.expander("Show details"):
                st.json(user_ctx["pending_booking"])
        
        st.divider()
        
        if st.button("🔄 New Conversation", use_container_width=True):
            st.session_state.messages = []
            greeting = st.session_state.agent.reset_conversation()
            st.session_state.messages.append({"role": "assistant", "content": greeting})
            st.rerun()
        
        if st.button("🗑️ Reset Database", use_container_width=True):
            if os.path.exists("table_turner.db"):
                os.remove("table_turner.db")
            st.session_state.database = TableTurnerDB()
            st.session_state.database.seed_data()
            st.success("Database reset!")
            st.rerun()
    
    # Footer info
    st.markdown("---")
    with st.expander("ℹ️ About V3 Hybrid Approach"):
        st.markdown("""
        ## 🎯 What Makes V3 Different?
        
        ### The Problem with Traditional Chatbots:
        
        **Too Rigid**:
        ```
        User: "Book Bella Italia tomorrow at 7 PM for 4, I'm Raj 9876543210"
        Bot: "Can I get your mobile number?"  ← Ignores everything!
        ```
        
        **Too Loose**:
        ```
        User: "I want to book"
        Bot: "Sure! When and where?"  ← Doesn't guide
        ```
        
        ### V3 Hybrid Solution:
        
        **Smart Extraction**:
        - Recognizes info in ANY order
        - Processes what you give
        - Only asks for missing pieces
        
        **Example**:
        ```
        User: "Book Bella Italia tomorrow at 7 PM for 4, I'm Raj 9876543210"
        V3: "Perfect! Checking Bella Italia for tomorrow at 7 PM for 4 people...
             [finds availability]
             Great! Available. Confirming for Raj at 9876543210?"
        ```
        
        **Another Example**:
        ```
        User: "I want a reservation"
        V3: "I'd love to help! Just need a few details:
             - Your mobile number
             - Which restaurant (or I can suggest based on cuisine)
             - Date, time, and party size"
        ```
        
        ### Technical Implementation:
        
        - **Information Extraction Functions**: Parse phone, name, booking details
        - **Context Tracking**: Remembers what you've provided
        - **Gap Analysis**: Asks only for missing data
        - **Validation**: Still enforces 3-day rule, phone auth, etc.
        - **Natural Flow**: Conversation feels human-like
        
        ### Best Practices Demonstrated:
        
        1. **User-Centric Design**: Adapt to user, not force them to adapt
        2. **Efficiency**: Power users get fast path
        3. **Accessibility**: New users get guidance
        4. **Compliance**: Still collect required data
        5. **Scalability**: Works for various user types
        
        ### Business Impact:
        
        - 📈 Higher conversion (less friction)
        - ⚡ Faster bookings (no rigid steps)
        - 😊 Better UX (feels natural)
        - ✅ Same compliance (all data collected)
        
        ---
        
        **V3 = Production-Ready + User-Friendly** 🎯
        """)

if __name__ == "__main__":
    main()
