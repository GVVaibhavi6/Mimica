import streamlit as st
from characters import CHARACTERS

def show_selection_page():
    # Back to home button
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("← Back to Home", key="back_to_home"):
            st.session_state.current_page = 'welcome'
            st.rerun()
    
    st.markdown('<h1 class="main-title">💝 MIMICA</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #667eea; font-size: 2rem; margin-bottom: 1rem;">Choose Your Challenge</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem; margin-bottom: 3rem;">Select a scenario and help the AI character improve their emotional state!</p>', unsafe_allow_html=True)
    
    # Character cards
    for name, data in CHARACTERS.items():
        st.markdown(f"""
        <div class="character-card">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="font-size: 3rem; margin-right: 1rem;">{data['emoji']}</div>
                <div>
                    <h3 style="color: #667eea; font-size: 1.8rem; margin: 0;">{data['title']}</h3>
                    <p style="color: #764ba2; margin: 0.5rem 0;">{name}</p>
                </div>
            </div>
            <p style="color: #666; font-size: 1rem; line-height: 1.5; margin-bottom: 1rem;">{data['description']}</p>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                <p style="font-style: italic; color: #555; margin: 0;">"{data['initial_message'][:150]}..."</p>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <span style="background: #e3f2fd; color: #1976d2; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.9rem;">{data['difficulty']}</span>
                <span style="color: #666; font-size: 0.9rem;">Initial Score: {data['initial_score']}%</span>
            </div>
            <p style="color: #667eea; font-size: 0.9rem; margin-bottom: 1rem;">{data['goal']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"Start Challenge with {name}", key=f"select_{name}", use_container_width=True):
            st.session_state.character = name
            st.session_state.emotion_score = data['initial_score']
            st.session_state.current_page = 'chat'
            st.session_state.messages = [
                {"role": "character", "content": data["initial_message"]}
            ]
            st.session_state.is_processing = False
            st.session_state.last_processed_message = ""
            st.session_state.message_counter = 0
            st.rerun()