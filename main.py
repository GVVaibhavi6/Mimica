import streamlit as st
from config import setup_page_config, initialize_session_state
from styles import apply_custom_css
from pages.welcome import show_welcome_page
from pages.selection import show_selection_page
from pages.chat import show_chat_page

def main():
    """Main application entry point"""
    st.markdown("""
        <style>
            div[data-testid="stSidebarNav"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

    # Setup page configuration
    setup_page_config()
    apply_custom_css()
    
    # Initialize session state variables
    initialize_session_state()
    
    # Main app navigation
    if st.session_state.current_page == 'welcome':
        show_welcome_page()
    elif st.session_state.current_page == 'selection':
        show_selection_page()
    elif st.session_state.current_page == 'chat':
        show_chat_page()

if __name__ == "__main__":
    main()
