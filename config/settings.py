import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_secret(key: str):
    try:
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key)

# Database config
MONGO_URI = get_secret("MONGO_URI")
MONGO_DB = get_secret("MONGO_DB") or "chatbot_db"
MONGO_COLLECTION = get_secret("MONGO_COLLECTION") or "conversations"

# Model config
MODEL_SENTIMENT = get_secret("MODEL_SENTIMENT") or "nlptown/bert-base-multilingual-uncased-sentiment"

# Groq config
GROQ_API_KEY = get_secret("GROQ_API_KEY")
GROQ_MODEL = get_secret("GROQ_MODEL") or "openai/gpt-oss-120b"
