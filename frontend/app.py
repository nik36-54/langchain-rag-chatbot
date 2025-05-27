import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="LLM Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# App title and description
st.title("🤖 LLM-Powered Chatbot")
st.markdown("""
This chatbot uses advanced language models to provide intelligent responses.
Feel free to ask any questions!
""")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get backend URL from environment variable
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
    
    try:
        # Send request to backend
        response = requests.post(
            f"{backend_url}/chat",
            json={"message": prompt}
        )
        response.raise_for_status()
        bot_response = response.json()["response"]
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(bot_response)
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Please make sure the backend server is running and accessible.") 