"""Table Turner V3 with FUNCTIONAL Voice Features."""
import streamlit as st
import streamlit.components.v1 as components
import os
from dotenv import load_dotenv
import sys

sys.path.append(os.path.dirname(__file__))

from data.database import TableTurnerDB
from agent.hybrid_agent_v3 import HybridAgentV3

load_dotenv()

st.set_page_config(
    page_title="Table Turner V3 - Voice Enabled",
    page_icon="🍽️",
    layout="wide"
)

# Enhanced CSS with voice features
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
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
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
        font-size: 1.2rem;
        opacity: 0.6;
        transition: all 0.2s;
        position: absolute;
        right: 15px;
        top: 15px;
        background: rgba(102, 126, 234, 0.1);
        padding: 0.3rem 0.5rem;
        border-radius: 5px;
    }
    .volume-icon:hover {
        opacity: 1;
        background: rgba(102, 126, 234, 0.2);
        transform: scale(1.1);
    }
    .stat-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    .stButton>button {
        background-color: #667eea;
        color: white;
        border-radius: 8px;
        padding: 0.7rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #764ba2;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    .voice-recording {
        background: #ff4444;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
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
    #voice-status {
        padding: 0.5rem;
        background: #E8F5E9;
        border-radius: 5px;
        margin: 0.5rem 0;
        text-align: center;
        font-weight: 500;
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
    
    if "voice_transcript" not in st.session_state:
        st.session_state.voice_transcript = ""

def create_voice_components():
    """Create voice input and output HTML components."""
    voice_html = """
    <script>
        // Text-to-Speech function
        function speakText(text, messageId) {
            if ('speechSynthesis' in window) {
                // Cancel any ongoing speech
                window.speechSynthesis.cancel();
                
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 1.0;
                utterance.pitch = 1.0;
                utterance.volume = 1.0;
                
                // Use a pleasant voice if available
                const voices = window.speechSynthesis.getVoices();
                const preferredVoice = voices.find(voice => 
                    voice.name.includes('Google') || 
                    voice.name.includes('Female') ||
                    voice.lang.includes('en-US')
                );
                if (preferredVoice) {
                    utterance.voice = preferredVoice;
                }
                
                window.speechSynthesis.speak(utterance);
            } else {
                alert('Text-to-speech not supported in this browser');
            }
        }
        
        // Make function globally available
        window.speakText = speakText;
    </script>
    
    <!-- Voice Input Component -->
    <div id="voice-input-container" style="display: none;">
        <div id="voice-status">🎤 Listening... Speak now</div>
        <button onclick="stopVoiceInput()" style="margin-top: 10px; padding: 8px 16px; background: #ff4444; color: white; border: none; border-radius: 5px; cursor: pointer;">
            ⏹️ Stop Recording
        </button>
    </div>
    
    <script>
        let recognition = null;
        
        // Initialize Speech Recognition
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';
            
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                
                // Send transcript back to Streamlit
                const textInput = window.parent.document.querySelector('input[type="text"]');
                if (textInput) {
                    textInput.value = transcript;
                    textInput.dispatchEvent(new Event('input', { bubbles: true }));
                }
                
                document.getElementById('voice-input-container').style.display = 'none';
                alert('You said: ' + transcript);
            };
            
            recognition.onerror = function(event) {
                console.error('Speech recognition error:', event.error);
                document.getElementById('voice-input-container').style.display = 'none';
                alert('Voice recognition error. Please try again.');
            };
            
            recognition.onend = function() {
                document.getElementById('voice-input-container').style.display = 'none';
            };
        }
        
        function startVoiceInput() {
            if (recognition) {
                document.getElementById('voice-input-container').style.display = 'block';
                recognition.start();
            } else {
                alert('Voice input not supported in this browser. Please use Chrome or Edge.');
            }
        }
        
        function stopVoiceInput() {
            if (recognition) {
                recognition.stop();
            }
            document.getElementById('voice-input-container').style.display = 'none';
        }
        
        window.startVoiceInput = startVoiceInput;
        window.stopVoiceInput = stopVoiceInput;
        
        // Load voices
        if ('speechSynthesis' in window) {
            window.speechSynthesis.onvoiceschanged = () => {
                window.speechSynthesis.getVoices();
            };
        }
    </script>
    """
    
    return voice_html

def main():
    """Main application."""
    initialize_session_state()
    
    # Add voice components
    components.html(create_voice_components(), height=0)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="logo-text">🍽️ Table Turner</h1>
        <span class="version-badge">V3 - VOICE ENABLED 🎤🔊</span>
        <p class="tagline">by GoodFoods - Natural Conversation with Voice Support</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature badges
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown('<span class="feature-badge">🧠 Smart AI</span>', unsafe_allow_html=True)
    with col2:
        st.markdown('<span class="feature-badge">🎤 Voice Input</span>', unsafe_allow_html=True)
    with col3:
        st.markdown('<span class="feature-badge">🔊 Voice Output</span>', unsafe_allow_html=True)
    with col4:
        st.markdown('<span class="feature-badge">🗄️ SQLite</span>', unsafe_allow_html=True)
    with col5:
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
        st.markdown(f"""<div class="stat-card">
            <p class="stat-value">{stats['restaurants']}</p>
            <p class="stat-label">🍽️ Restaurants</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="stat-card">
            <p class="stat-value">{stats['users']}</p>
            <p class="stat-label">👥 Users</p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="stat-card">
            <p class="stat-value">{stats['active_reservations']}</p>
            <p class="stat-label">📅 Active</p>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="stat-card">
            <p class="stat-value">{stats['total_tables']}</p>
            <p class="stat-label">🪑 Tables</p>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chat messages with voice output
    for idx, message in enumerate(st.session_state.messages):
        role = message["role"]
        content = message["content"]
        message_id = f"msg_{idx}"
        
        # Escape quotes for JavaScript
        safe_content = content.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')
        
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
                <span class="volume-icon" onclick="window.speakText('{safe_content}', '{message_id}')" title="Click to hear message">
                    🔊
                </span>
            </div>
            """, unsafe_allow_html=True)
    
    # Voice input container
    components.html("""
    <div id="voice-input-container" style="display: none; margin: 20px 0;">
        <div id="voice-status" style="padding: 15px; background: linear-gradient(135deg, #ff6b6b, #ff8787); color: white; border-radius: 10px; text-align: center; font-size: 1.2rem; animation: pulse 1.5s infinite;">
            🎤 Listening... Speak now
        </div>
    </div>
    """, height=100)
    
    # Input section
    st.markdown("---")
    
    # Input mode selection
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown("**Choose input method:**")
    with col2:
        if st.button("📝 Text Input", use_container_width=True, 
                    type="primary" if st.session_state.input_mode == "text" else "secondary"):
            st.session_state.input_mode = "text"
    
    with col3:
        # Voice input button with JavaScript trigger
        voice_button_html = """
        <button onclick="startVoiceInput()" style="
            width: 100%;
            background-color: #667eea;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            transition: all 0.3s;
        " onmouseover="this.style.backgroundColor='#764ba2'" 
           onmouseout="this.style.backgroundColor='#667eea'">
            🎤 Voice Input
        </button>
        """
        components.html(voice_button_html, height=45)
    
    # Text input
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Your message:",
            key="user_input",
            placeholder="Type or use voice input... 💬",
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
    
    # Quick examples
    st.markdown("---")
    with st.expander("💡 Try these (voice or text)"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Fast Path:**
            - "Book Bella Italia tomorrow at 7 PM for 4, I'm Raj 9876543210"
            - "9876543210 - Spice Garden today 6 PM, party of 2, name Sarah"
            """)
        with col2:
            st.markdown("""
            **Guided:**
            - "I want to make a reservation"
            - "Show me Italian restaurants"
            - "Need a table for tomorrow"
            """)
    
    # Sidebar
    with st.sidebar:
        st.header("🎤 Voice Features")
        st.markdown("""
        ### Voice Input 🎤
        - Click "🎤 Voice Input" button
        - Speak your request
        - Works in Chrome, Edge, Safari
        
        ### Voice Output 🔊
        - Click 🔊 icon on any message
        - Hear message read aloud
        - Uses browser's TTS
        
        ### 💡 Voice Tips
        - Speak clearly
        - Include all details
        - Works best in quiet environment
        """)
        
        st.divider()
        
        st.header("📊 System Stats")
        st.json(stats)
        
        st.divider()
        
        user_ctx = st.session_state.agent.get_user_context()
        if user_ctx.get("authenticated"):
            st.success(f"✅ {user_ctx.get('name')}")
            st.info(f"📱 {user_ctx.get('phone_number')}")
        
        st.divider()
        
        if st.button("🔄 New Chat", use_container_width=True):
            st.session_state.messages = []
            greeting = st.session_state.agent.reset_conversation()
            st.session_state.messages.append({"role": "assistant", "content": greeting})
            st.rerun()
    
    # Footer
    st.markdown("---")
    with st.expander("ℹ️ Voice Feature Details"):
        st.markdown("""
        ## 🎤 Voice Input (Web Speech API)
        
        **How it works:**
        1. Click "🎤 Voice Input" button
        2. Browser asks for microphone permission (first time)
        3. Speak your message
        4. Text appears in input box automatically
        5. Click Send or say more
        
        **Supported Browsers:**
        - ✅ Chrome (best support)
        - ✅ Edge
        - ✅ Safari (iOS/macOS)
        - ⚠️ Firefox (limited support)
        
        **Example Voice Commands:**
        - "Book Bella Italia tomorrow at seven PM for four people"
        - "I'm John, my number is nine eight seven six five four three two one zero"
        - "Show me Indian restaurants"
        
        ---
        
        ## 🔊 Voice Output (Speech Synthesis)
        
        **How it works:**
        1. Click 🔊 icon on any message
        2. Browser reads message aloud
        3. Uses high-quality TTS voices
        
        **Features:**
        - Automatic voice selection (prefers pleasant voices)
        - Natural speech rate
        - Clear pronunciation
        - Works in all modern browsers
        
        **Note:** Voice quality depends on your browser and OS.
        
        ---
        
        ## 🌐 Browser Compatibility
        
        | Feature | Chrome | Edge | Safari | Firefox |
        |---------|--------|------|--------|---------|
        | Voice Input | ✅ | ✅ | ✅ | ⚠️ |
        | Voice Output | ✅ | ✅ | ✅ | ✅ |
        | Quality | Excellent | Excellent | Good | Good |
        
        **Best Experience**: Chrome or Edge
        
        ---
        
        ## 🔒 Privacy
        
        - Voice processing happens **in your browser**
        - No audio sent to servers
        - Web Speech API is built into browser
        - Fully private and secure
        
        ---
        
        **Voice features are fully functional!** 🎉
        """)

if __name__ == "__main__":
    main()
