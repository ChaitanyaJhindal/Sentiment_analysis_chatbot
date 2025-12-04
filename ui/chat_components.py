import streamlit as st
from datetime import datetime

def render_message_bubble(msg):
    ts = msg.get("created_at", "")
    role = msg.get("role", "user")
    text = msg.get("text", "")
    sent = msg.get("sentiment")

    try:
        time_str = datetime.fromisoformat(ts.replace('Z', '')).strftime("%I:%M %p")
    except:
        time_str = ts

    if role == "user":
        sentiment_html = ""
        if sent:
            sentiment_html = f"<div class='sentiment-badge sentiment-{sent['label']}'>{sent['label'].upper()} {'⭐' * sent['star']} ({round(sent['confidence']*100)}%)</div>"
        
        st.markdown(f"""
            <div style="text-align: right; margin-bottom: 1rem;">
                <div class="user-message">
                    <div style="font-size: 1rem;">{text}</div>
                    <div class="timestamp" style="color: rgba(255,255,255,0.8);">{time_str}</div>
                </div>
                {sentiment_html}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="margin-bottom: 1rem;">
                <div class="assistant-message">
                    <div style="font-size: 1rem;">🤖 {text}</div>
                    <div class="timestamp">{time_str}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

def render_chat_messages(messages):
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    
    if messages:
        for msg in messages:
            render_message_bubble(msg)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 3rem; color: #888;">
                <h2 style="color: #667eea;">👋 Welcome!</h2>
                <p>Start a conversation by typing a message.</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_message_input():
    st.markdown("### 💭 Send a Message")
    
    with st.form("input_form", clear_on_submit=True):
        user_text = st.text_input(
            "Type your message...", 
            key="user_input", 
            label_visibility="collapsed", 
            placeholder="Type your message here..."
        )
        send_clicked = st.form_submit_button("📤 Send", use_container_width=True)
    
    return user_text, send_clicked
