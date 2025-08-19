import streamlit as st
import datetime

def save_chat_to_history():
    """Save current chat to history"""
    if st.session_state.messages and st.session_state.character:
        chat_entry = {
            'character': st.session_state.character,
            'messages': st.session_state.messages.copy(),
            'final_score': st.session_state.emotion_score,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            'title': f"Chat with {st.session_state.character} - {st.session_state.emotion_score}%"
        }
        st.session_state.chat_history = [
            chat for chat in st.session_state.chat_history 
            if chat['character'] != st.session_state.character
        ]
        st.session_state.chat_history.insert(0, chat_entry)
        st.session_state.chat_history = st.session_state.chat_history[:10]

def load_chat_from_history(chat_entry):
    """Load a chat from history"""
    st.session_state.character = chat_entry['character']
    st.session_state.messages = chat_entry['messages']
    st.session_state.emotion_score = chat_entry['final_score']
    st.session_state.current_page = 'chat'
    st.session_state.is_processing = False
    st.session_state.last_processed_message = ""