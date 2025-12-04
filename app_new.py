import sys
import streamlit as st

try:
    from streamlit.runtime.scriptrunner import get_script_run_ctx
    if get_script_run_ctx() is None:
        print("Please run this app using: streamlit run app.py")
        sys.exit(1)
except Exception:
    print("Please run this app using: streamlit run app.py")
    sys.exit(1)

from services.dependencies import db
from services.chat_service import add_user_message
from ui.styles import apply_custom_styles
from ui.sidebar import render_sidebar
from ui.chat_components import render_chat_messages, render_message_input
from ui.advanced_actions import render_advanced_actions

st.set_page_config(page_title="Sentiment Chatbot", page_icon="💬", layout="wide")
apply_custom_styles()

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = db.start_conversation()

if "messages" not in st.session_state:
    conv = db.get_conversation(st.session_state.conversation_id)
    st.session_state.messages = conv.get("messages", [])

st.title("💬 Sentiment Chatbot")

reset_clicked = render_sidebar(st.session_state.messages)

if reset_clicked:
    st.session_state.conversation_id = db.start_conversation()
    st.session_state.messages = []
    st.rerun()

render_chat_messages(st.session_state.messages)

user_text, send_clicked = render_message_input()

if send_clicked and user_text:
    add_user_message(st.session_state.conversation_id, st.session_state.messages, user_text, via="text")
    st.rerun()

render_advanced_actions(st.session_state.conversation_id, st.session_state.messages)
