import streamlit as st
import json
from config.settings import MONGO_URI, GROQ_API_KEY
from services.dependencies import db

def render_sidebar(messages):
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        st.markdown("---")
        
        mongo_status = "🟢 Connected" if MONGO_URI else "🔴 Disconnected"
        groq_status = "🟢 Enabled" if GROQ_API_KEY else "🔴 Disabled"
        
        st.markdown(f"**Database:** {mongo_status}")
        st.markdown(f"**AI Engine:** {groq_status}")
        st.markdown(f"**Model:** `nlptown/bert`")
        
        st.markdown("---")
        st.markdown("### 🔄 Actions")
        
        reset_clicked = st.button("🗑️ Reset Conversation", use_container_width=True)
        
        if st.button("📥 Export Chat", use_container_width=True):
            conv = db.get_conversation(st.session_state.conversation_id)
            st.download_button(
                "📄 Download JSON",
                json.dumps(conv, indent=2),
                "conversation.json",
                use_container_width=True
            )
        
        st.markdown("---")
        st.markdown("### 📊 Conversation Stats")
        user_msgs = [m for m in messages if m["role"] == "user"]
        
        if user_msgs:
            pos = len([m for m in user_msgs if m.get("sentiment", {}).get("label") == "positive"])
            neu = len([m for m in user_msgs if m.get("sentiment", {}).get("label") == "neutral"])
            neg = len([m for m in user_msgs if m.get("sentiment", {}).get("label") == "negative"])
            
            st.markdown(f"**Total Messages:** {len(messages)}")
            st.markdown(f"😊 Positive: {pos}")
            st.markdown(f"😐 Neutral: {neu}")
            st.markdown(f"😞 Negative: {neg}")
        else:
            st.markdown("*No messages yet*")
    
    return reset_clicked
