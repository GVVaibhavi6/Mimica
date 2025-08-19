import streamlit as st
from characters import CHARACTERS
from emotion_analysis import analyze_emotion, generate_character_response
from chat_history import save_chat_to_history, load_chat_from_history

def _display_final_scoreboard(): # displays final scoreboard
    """Renders the final scoreboard screen with improved styling."""
    stats = st.session_state.final_stats
    
    st.markdown("""
    <style>
    .metric-label {
        color: #4a5568; /* Darker grey for better readability */
        font-size: 1.1rem;
        font-weight: bold;
    }
    .metric-value {
        font-size: 2rem;
        color: #2d3748;
    }
    .play-again-button {
        display: flex;
        justify-content: center;
        margin-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.balloons()
    st.markdown('<h1 class="main-title" style="text-align: center;">🎉 Mission Complete! 🎉</h1>', unsafe_allow_html=True)
    st.markdown(f'<h2 style="text-align: center; color: #667eea;">You\'re an amazing friend to {stats.get("character", "them")}!</h2>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-label">Character Helped</div><div class="metric-value">{stats.get("character", "N/A")}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-label">Final Happiness</div><div class="metric-value">100%</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-label">Messages Sent</div><div class="metric-value">{stats.get("user_message_count", 0)}</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown('<div class="play-again-button">', unsafe_allow_html=True)
    if st.button("🙌 Play Again With Another Friend"):
        st.session_state.current_page = 'selection'
        st.session_state.show_scoreboard = False
        st.session_state.character = None
        st.session_state.messages = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def show_chat_page():
    if st.session_state.get('show_scoreboard', False):
        _display_final_scoreboard()
        return 

    st.markdown("""
    <style>
    @keyframes fade-in-out {
        0% { opacity: 0; transform: translateY(20px); }
        10% { opacity: 1; transform: translateY(0); }
        90% { opacity: 1; transform: translateY(0); }
        100% { opacity: 0; transform: translateY(20px); }
    }
    .score-popup {
        position: fixed; bottom: 20px; right: 20px; padding: 0.75rem 1.25rem;
        border-radius: 10px; color: white; font-size: 1rem; font-weight: bold;
        z-index: 1000; animation: fade-in-out 4s ease-in-out forwards;
    }
    .score-popup.success { background-color: #28a745; }
    .score-popup.info { background-color: #17a2b8; }
    .score-popup.warning { background-color: #ffc107; color: #333; }
    </style>
    """, unsafe_allow_html=True)

    character_data = CHARACTERS[st.session_state.character]
    
    # Top progress bar
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
        <h3 style="color: #667eea; margin: 0;">🎯 Target: 60% to win!</h3>
        <h3 style="color: #667eea; margin:0;">{st.session_state.emotion_score}%</h3>
    </div>
    """, unsafe_allow_html=True)
    st.progress(st.session_state.emotion_score / 100)
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 2rem;">
            <div style="font-size: 3rem; margin-right: 1rem;">{character_data['emoji']}</div>
            <h2 style="color: white; margin: 0;">{st.session_state.character}</h2>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="mission-box">
            <h3 style="color: white; text-align: center;">💝 Your Mission</h3>
            <p style="color: rgba(255,255,255,0.9); font-size: 0.9rem; text-align: center;">{character_data['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Choose Another Friend"):
            if st.session_state.messages and len(st.session_state.messages) > 1:
                save_chat_to_history()
            st.session_state.current_page = 'selection'
            st.rerun()
            
    # Main chat UI
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message["role"] == "character":
            st.markdown(f'<div style="display: flex; align-items: flex-start; margin: 15px 0;"><div style="font-size: 2rem; margin-right: 10px;">{character_data["emoji"]}</div><div class="bot-message">{message["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="display: flex; justify-content: flex-end; margin: 15px 0;"><div class="user-message">{message["content"]}</div></div>', unsafe_allow_html=True)

    if st.session_state.is_processing:
        st.markdown(f'<div style="display: flex; align-items: flex-start; margin: 15px 0;"><div style="font-size: 2rem; margin-right: 10px;">{character_data["emoji"]}</div><div class="bot-message"><div class="loading-spinner"></div> Thinking...</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # User input handling
    if user_input := st.chat_input("Type your message...", disabled=st.session_state.is_processing):
        st.session_state.last_processed_message = user_input
        st.session_state.is_processing = True
        st.rerun()

    # Main processing block
    if st.session_state.is_processing and st.session_state.last_processed_message:
        try:
            current_user_input = st.session_state.last_processed_message
            st.session_state.messages.append({"role": "user", "content": current_user_input})
            impact_score = analyze_emotion(current_user_input, character_data["personality"])
            
            old_score = st.session_state.emotion_score
            change = (impact_score - 50) // 4
            st.session_state.emotion_score = max(0, min(100, old_score + change))
            
            character_response = generate_character_response(current_user_input, st.session_state.character, character_data["personality"], st.session_state.emotion_score)
            st.session_state.messages.append({"role": "character", "content": character_response})

            # Store feedback message in session state
            if change > 5: st.session_state.feedback = {"message": f"Excellent! +{change} Happiness", "type": "success"}
            elif change > 0: st.session_state.feedback = {"message": f"Good job! +{change} Happiness", "type": "info"}
            else: st.session_state.feedback = {"message": f"Score changed by {change}. Try being more empathetic.", "type": "warning"}
            
            # Check for 100 points to trigger scoreboard
            if st.session_state.emotion_score >= 100:
                user_message_count = len([msg for msg in st.session_state.messages if msg['role'] == 'user'])
                st.session_state.final_stats = {
                    "character": st.session_state.character,
                    "user_message_count": user_message_count
                }
                st.session_state.show_scoreboard = True
                save_chat_to_history()

        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            st.session_state.is_processing = False
            st.session_state.last_processed_message = ""
            st.rerun()

    # Display the score change pop-up bar
    if "feedback" in st.session_state and st.session_state.feedback:
        feedback = st.session_state.feedback
        st.markdown(f'<div class="score-popup {feedback["type"]}">{feedback["message"]}</div>', unsafe_allow_html=True)
        st.session_state.feedback = None
