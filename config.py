import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Configuring OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def setup_page_config():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="MIMICA",
        page_icon="💝",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def initialize_session_state():
    """Initialize all session state variables"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'welcome'
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'emotion_score' not in st.session_state:
        st.session_state.emotion_score = 35
    if 'character' not in st.session_state:
        st.session_state.character = None
    if 'combo' not in st.session_state:
        st.session_state.combo = 0
    if 'level' not in st.session_state:
        st.session_state.level = 1
    if 'is_processing' not in st.session_state:
        st.session_state.is_processing = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'last_processed_message' not in st.session_state:
        st.session_state.last_processed_message = ""
    if 'message_counter' not in st.session_state:
        st.session_state.message_counter = 0
    if 'show_scoreboard' not in st.session_state:
        st.session_state.show_scoreboard = False
    if 'final_stats' not in st.session_state:
        st.session_state.final_stats = {}
    if 'feedback' not in st.session_state:
        st.session_state.feedback = None