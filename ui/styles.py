import streamlit as st

def apply_custom_styles():
    st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .chat-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .assistant-message {
        background: #f0f2f6;
        color: #1f1f1f;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-right: auto;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .sentiment-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .sentiment-positive {
        background: #d4edda;
        color: #155724;
    }
    
    .sentiment-neutral {
        background: #fff3cd;
        color: #856404;
    }
    
    .sentiment-negative {
        background: #f8d7da;
        color: #721c24;
    }
    
    .timestamp {
        font-size: 0.75rem;
        color: #888;
        margin-top: 0.3rem;
    }
    
    .stTextInput input {
        border-radius: 25px;
        padding: 0.8rem 1.2rem;
        border: 2px solid #e0e0e0;
    }
    
    .stTextInput input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
    
    .stButton button {
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    h1 {
        color: white;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    h3 {
        color: white;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)
