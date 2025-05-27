import streamlit as st
import requests
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

# Configure the page
st.set_page_config(
    page_title="AI PDF Chat Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for chat interface
st.markdown("""
<style>
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .stApp {
        background-color: #f8f9fa;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        padding: 1rem;
        max-height: 70vh;
        overflow-y: auto;
    }
    .message {
        display: flex;
        margin-bottom: 1rem;
        animation: fadeIn 0.3s ease-in;
    }
    .message.user {
        justify-content: flex-end;
    }
    .message.assistant {
        justify-content: flex-start;
    }
    .message-content {
        max-width: 80%;
        padding: 1rem;
        border-radius: 1rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    .message.user .message-content {
        background-color: #2b313e;
        color: white;
        border-bottom-right-radius: 0.2rem;
    }
    .message.assistant .message-content {
        background-color: #e3f2fd;
        color: #1a1a1a;
        border-bottom-left-radius: 0.2rem;
    }
    .message-header {
        font-size: 0.8rem;
        margin-bottom: 0.3rem;
        opacity: 0.8;
    }
    .message-text {
        line-height: 1.5;
    }
    .typing-indicator {
        display: flex;
        gap: 0.3rem;
        padding: 0.5rem;
        background-color: #e3f2fd;
        border-radius: 1rem;
        width: fit-content;
        margin: 0.5rem 0;
    }
    .typing-dot {
        width: 0.5rem;
        height: 0.5rem;
        background-color: #1f77b4;
        border-radius: 50%;
        animation: typing 1s infinite ease-in-out;
    }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes typing {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
    }
    .stButton>button:hover {
        background-color: #1668a1;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    @media (max-width: 768px) {
        .message-content {
            max-width: 90%;
        }
    }
</style>
""", unsafe_allow_html=True)

def render_message(role: str, content: str):
    """Render a single chat message with appropriate styling."""
    role_display = "You" if role == "user" else "Assistant"
    return f"""
    <div class="message {role}">
        <div class="message-content">
            <div class="message-header">{role_display}</div>
            <div class="message-text">{content}</div>
        </div>
    </div>
    """

def render_typing_indicator():
    """Render the typing indicator animation."""
    return """
    <div class="message assistant">
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    </div>
    """

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "file_processed" not in st.session_state:
    st.session_state.file_processed = False

# App title and description
st.title("📄 AI PDF Chat Assistant")
st.markdown("""
Welcome! Upload a PDF document and ask questions about its content. 
The AI will analyze the document and provide relevant answers.
""")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file is not None:
    try:
        with st.spinner("Processing your document..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            response = requests.post(f"{API_URL}/upload", files=files)
            response.raise_for_status()
            
            result = response.json()
            st.session_state.file_processed = True
            
            st.markdown(f"""
            <div class="success-message">
                ✅ File processed successfully with {result['num_chunks']} chunks.
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.markdown(f"""
        <div class="error-message">
            ❌ Error processing file: {str(e)}
        </div>
        """, unsafe_allow_html=True)

# Chat interface
st.markdown("---")
st.subheader("Chat with your document")

# Chat container
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        st.markdown(render_message(message["role"], message["content"]), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Chat input
if st.session_state.file_processed:
    question = st.text_input("Ask a question about your document", key="question")
    col1, col2 = st.columns([6, 1])
    
    with col2:
        submit = st.button("Send", use_container_width=True)
    
    if submit and question:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": question})
        
        # Show typing indicator
        with chat_container:
            st.markdown(render_typing_indicator(), unsafe_allow_html=True)
        
        try:
            # Get response from API
            response = requests.post(
                f"{API_URL}/chat",
                json={"question": question}
            )
            response.raise_for_status()
            result = response.json()
            
            # Add assistant response to chat
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"{result['answer']}\n\n**Sources:**\n" + "\n".join([f"- {source}" for source in result['sources']])
            })
            
            # Rerun to update the chat display
            st.rerun()
            
        except Exception as e:
            st.markdown(f"""
            <div class="error-message">
                ❌ Error: {str(e)}
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("Please upload a PDF document to start chatting.") 