"""Table Turner - Production-Ready Restaurant Reservation Assistant."""
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
    page_title="Table Turner - GoodFoods",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Clean, professional CSS
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Header */
    .app-header {
        text-align: center;
        padding: 2rem 1rem 1.5rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 0 0 20px 20px;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .logo {
        font-size: 3rem;
        margin-bottom: 0.3rem;
    }
    
    .app-title {
        font-size: 2.2rem;
        color: white;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .app-subtitle {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.9);
        margin: 0.3rem 0 0 0;
        font-weight: 400;
    }
    
    /* Chat messages */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
    
    .chat-message {
        padding: 1rem 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        position: relative;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        animation: fadeIn 0.3s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: #e3f2fd;
        border-left: 3px solid #2196F3;
        margin-left: 3rem;
    }
    
    .assistant-message {
        background: white;
        border-left: 3px solid #667eea;
        margin-right: 3rem;
    }
    
    .message-role {
        font-weight: 600;
        margin-bottom: 0.3rem;
        font-size: 0.9rem;
    }
    
    .message-content {
        line-height: 1.6;
        color: #333;
    }
    
    .volume-icon {
        position: absolute;
        right: 12px;
        top: 12px;
        cursor: pointer;
        font-size: 1.1rem;
        opacity: 0.4;
        transition: all 0.2s;
        padding: 0.3rem;
        border-radius: 50%;
    }
    
    .volume-icon:hover {
        opacity: 1;
        background: rgba(102, 126, 234, 0.1);
    }
    
    /* Input area */
    .input-container {
        max-width: 800px;
        margin: 2rem auto 1rem auto;
        padding: 1.5rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    .stTextInput input {
        border-radius: 25px;
        border: 2px solid #e0e0e0;
        padding: 0.8rem 1.2rem;
        font-size: 1rem;
    }
    
    .stTextInput input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Voice button */
    .voice-btn {
        background: #667eea !important;
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        cursor: pointer;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .voice-btn:hover {
        background: #764ba2 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .voice-recording {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8787 100%) !important;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Hide expandable sections */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #667eea;
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
    
    if "api_key_set" not in st.session_state:
        st.session_state.api_key_set = bool(os.getenv("GEMINI_API_KEY"))

def create_voice_script():
    """Create voice functionality script."""
    return """
    <script>
        // Text-to-Speech
        function speakText(text) {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 0.95;
                utterance.pitch = 1.0;
                utterance.volume = 1.0;
                
                const voices = window.speechSynthesis.getVoices();
                const voice = voices.find(v => v.lang.includes('en') && v.name.includes('Female')) || voices[0];
                if (voice) utterance.voice = voice;
                
                window.speechSynthesis.speak(utterance);
            }
        }
        
        // Speech Recognition
        let recognition = null;
        if ('webkitSpeechRecognition' in window) {
            recognition = new webkitSpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';
            
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                const inputs = window.parent.document.querySelectorAll('input[type="text"]');
                const textInput = Array.from(inputs).find(input => 
                    input.placeholder && input.placeholder.includes('message')
                );
                if (textInput) {
                    textInput.value = transcript;
                    const inputEvent = new Event('input', { bubbles: true });
                    textInput.dispatchEvent(inputEvent);
                }
            };
            
            recognition.onerror = function(event) {
                console.error('Recognition error:', event.error);
            };
        }
        
        function startVoice() {
            if (recognition) {
                recognition.start();
            } else {
                alert('Voice input requires Chrome, Edge, or Safari');
            }
        }
        
        window.speakText = speakText;
        window.startVoice = startVoice;
        
        if ('speechSynthesis' in window) {
            speechSynthesis.onvoiceschanged = () => speechSynthesis.getVoices();
        }
    </script>
    """

def main():
    """Main application."""
    initialize_session_state()
    
    # Voice script
    components.html(create_voice_script(), height=0)
    
    # Simple header
    st.markdown("""
    <div class="app-header">
        <div class="logo">🍽️</div>
        <h1 class="app-title">Table Turner</h1>
        <p class="app-subtitle">GoodFoods Restaurant Reservations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # API key check
    if not st.session_state.api_key_set:
        st.warning("Please configure your API key to continue")
        api_key_input = st.text_input("Gemini API Key", type="password")
        if st.button("Continue"):
            if api_key_input:
                os.environ["GEMINI_API_KEY"] = api_key_input
                st.session_state.agent = HybridAgentV3(api_key_input, st.session_state.database)
                greeting = st.session_state.agent.start_chat()
                st.session_state.messages = [{"role": "assistant", "content": greeting}]
                st.session_state.api_key_set = True
                st.rerun()
        return
    
    # Chat messages
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for idx, message in enumerate(st.session_state.messages):
        role = message["role"]
        content = message["content"]
        safe_content = content.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')
        
        if role == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-role" style="color: #1976D2;">You</div>
                <div class="message-content">{content}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <div class="message-role" style="color: #667eea;">Table Turner</div>
                <div class="message-content">{content}</div>
                <span class="volume-icon" onclick="window.speakText('{safe_content}')" title="Listen">🔊</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([6, 1, 1])
    
    with col1:
        user_input = st.text_input(
            "Message",
            key="user_input",
            placeholder="Type your message or use voice...",
            label_visibility="collapsed"
        )
    
    with col2:
        # Voice button
        voice_html = """
        <button onclick="window.startVoice()" class="voice-btn" style="
            width: 100%;
            background: #667eea;
            color: white;
            border: none;
            padding: 0.75rem;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1.2rem;
        " title="Voice input">🎤</button>
        """
        components.html(voice_html, height=50)
    
    with col3:
        send_button = st.button("Send", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle message sending
    if send_button and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.spinner(""):
            response = st.session_state.agent.send_message(user_input)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    # Simple footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0 1rem 0; color: #999; font-size: 0.85rem;">
        Powered by AI • GoodFoods Restaurant Group
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
