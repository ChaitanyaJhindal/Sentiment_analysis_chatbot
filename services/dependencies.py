import streamlit as st

from backend.sentiment import SentimentAnalyzer
from backend.db import MongoManager
from config.settings import MONGO_URI, MONGO_DB, MONGO_COLLECTION, MODEL_SENTIMENT

try:
    from backend.groq_client import GroqClient
    GROQ_AVAILABLE = True
except Exception:
    GROQ_AVAILABLE = False

@st.cache_resource(show_spinner=False)
def get_db_manager(uri, db_name, coll_name):
    if not uri:
        raise ValueError("MONGO_URI not set!")
    return MongoManager(uri, db_name, coll_name)

@st.cache_resource(show_spinner=False)
def get_sentiment_analyzer(model_name):
    return SentimentAnalyzer(model_name=model_name)

@st.cache_resource(show_spinner=False)
def get_groq_client():
    if not GROQ_AVAILABLE:
        return None
    try:
        return GroqClient()
    except Exception:
        return None

db = get_db_manager(MONGO_URI, MONGO_DB, MONGO_COLLECTION)
sentiment = get_sentiment_analyzer(MODEL_SENTIMENT)
groq = get_groq_client()
