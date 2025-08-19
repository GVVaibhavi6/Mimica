import streamlit as st

def show_welcome_page():
    st.markdown('<h1 class="main-title">💝 MIMICA</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.3rem; margin-bottom: 3rem;">Help AI friends feel better through kind conversations</p>', unsafe_allow_html=True)
    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; font-size: 1.5rem; margin-bottom: 1rem;">💝 YOUR MISSION</h3>
            <p style="color: #666; line-height: 1.6;">Chat with AI friends who need emotional support. Use empathy, kindness, and creativity to help them feel better!</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; font-size: 1.5rem; margin-bottom: 1rem;">📊 HAPPINESS METER</h3>
            <p style="color: #666; line-height: 1.6;">Watch the happiness meter rise as you send thoughtful messages. Each response shows how much you've helped!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Second row of cards
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; font-size: 1.5rem; margin-bottom: 1rem;">🏆 WIN CONDITION</h3>
            <p style="color: #666; line-height: 1.6;">Reach 60% happiness to complete your mission. It's achievable and rewarding!</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #667eea; font-size: 1.5rem; margin-bottom: 1rem;">💡 HELPFUL TIPS</h3>
            <ul style="color: #666; line-height: 1.6; margin-left: 1rem;">
                <li>Show genuine care and understanding</li>
                <li>Ask thoughtful follow-up questions</li>
                <li>Share positive encouragement</li>
                <li>Be creative with your responses</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💝 Start Helping Friends!", key="start_game", use_container_width=True):
            st.session_state.current_page = 'selection'
            st.rerun()