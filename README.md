# Sentiment Analysis Chatbot

Modern, modular chatbot with real-time sentiment analysis, MongoDB storage, and Groq AI integration.

## Project Structure

```
Sentiment_Analysis_chatbot/
├── app_new.py              # New modular entry point
├── config/
│   └── settings.py         # Configuration management
├── services/
│   ├── dependencies.py     # Service initialization
│   └── chat_service.py     # Core business logic
├── ui/
│   ├── styles.py           # UI styling
│   ├── chat_components.py  # Chat interface components
│   ├── sidebar.py          # Sidebar components
│   └── advanced_actions.py # Advanced features UI
└── backend/
    ├── db.py               # MongoDB operations
    ├── sentiment.py        # Sentiment analysis
    └── groq_client.py      # Groq AI integration
```

## Features

- Real-time sentiment analysis (positive/neutral/negative)
- AI-powered responses using Groq
- MongoDB conversation storage
- Beautiful gradient UI
- Conversation flow analysis
- Export chat history

## Setup

1. Install dependencies:
```bash
pip install streamlit pymongo transformers torch python-dotenv openai certifi
```

2. Configure environment (.env):
```
MONGO_URI=your_mongodb_uri
GROQ_API_KEY=your_groq_key
```

3. Run the app:
```bash
streamlit run app_new.py
```

## Scaling

The modular structure allows easy extension:
- Add new UI components in `ui/`
- Add new services in `services/`
- Add new models in `backend/`
- Modify config in `config/settings.py`
