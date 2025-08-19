import streamlit as st

def apply_custom_css():
    """Apply all custom CSS styling"""
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Global styles */
        .main {
            font-family: 'Inter', sans-serif;
        }
        
        /* Background gradient */
        .stApp {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            min-height: 100vh;
        }
        
        /* FIXED: Purple title color for visibility */
        .main-title {
            color: #6B46C1 !important;
            font-size: 3.5rem !important;
            font-weight: 700 !important;
            text-align: center !important;
            margin-bottom: 1rem !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
        }
        
        /* Welcome page sections */
        .welcome-section {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 1rem;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        /* FIXED: Grid for exactly 4 tiles in 2x2 layout */
        .feature-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin: 3rem 0;
            max-width: 1000px;
            margin-left: auto;
            margin-right: auto;
        }
        
        /* FIXED: Same size for all 4 feature cards */
        .feature-card {
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
            min-height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
        
        /* Character cards */
        .character-card {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 0;
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .character-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
            background: rgba(255, 255, 255, 0.95);
        }
        
        /* Chat messages */
        .user-message {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 12px 18px;
            border-radius: 18px 18px 4px 18px;
            margin: 8px 0;
            max-width: 70%;
            margin-left: auto;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        .bot-message {
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            padding: 12px 18px;
            border-radius: 18px 18px 18px 4px;
            margin: 8px 0;
            max-width: 70%;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #667eea;
        }
        
        /* Progress bar at top */
        .top-progress {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        
        /* Progress bar */
        .stProgress > div > div > div > div {
            background: linear-gradient(135deg, #667eea, #764ba2);
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 12px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            background: linear-gradient(135deg, #764ba2, #667eea);
        }
        
        /* Score display */
        .score-display {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin: 15px 0;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }
        
        /* Chat input styling - FIXED FOR VISIBILITY */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.95) !important;
            border: 2px solid rgba(102, 126, 234, 0.3) !important;
            border-radius: 25px !important;
            padding: 12px 20px !important;
            color: #333 !important;
            font-size: 14px !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #888 !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 1px #667eea !important;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Add padding to main content to account for fixed input */
        .main-content {
            padding-bottom: 120px;
        }
        
        /* Loading spinner */
        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(102, 126, 234, 0.3);
            border-radius: 50%;
            border-top-color: #667eea;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Chat history styling */
        .chat-history {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .chat-history:hover {
            background: rgba(255, 255, 255, 0.25);
            transform: translateY(-2px);
        }
        
        /* Mission box alignment fix */
        .mission-box {
            text-align: center;
        }
        
        .mission-box p {
            text-align: center !important;
        }
        
        .feature-card {
            border: 1px solid #ddd;
            padding: 1rem;
            box-sizing: border-box;
            height: 250px;  /* Set uniform height */
            overflow: auto;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        .main-title {
            color: #667eea;
            text-align: center;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)