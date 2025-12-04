import uuid
from datetime import datetime
from services.dependencies import db, sentiment, groq

def generate_sentiment_response(sentiment_label: str, user_text: str) -> str:
    if groq is None:
        import random
        fallback = {
            "positive": ["I'm glad to hear that! How can I help you further?"],
            "negative": ["I understand your concern. I'll make sure this is addressed properly."],
            "neutral": ["I understand. What would you like to know more about?"]
        }
        return random.choice(fallback.get(sentiment_label, ["How can I assist you?"]))
    
    try:
        prompt = f"""You are a helpful, empathetic customer service chatbot. 
The user just said: "{user_text}"
The sentiment detected is: {sentiment_label.upper()}

Generate a complete, natural response (2-3 sentences) that:
- Acknowledges their message with empathy
- Matches their emotional tone
- Offers specific help or encouragement
- Sounds professional and complete

IMPORTANT: Generate a COMPLETE response, not a partial one.

Response:"""
        
        response = groq.client.chat.completions.create(
            model=groq.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.6,
            stop=None
        )
        
        reply = response.choices[0].message.content.strip()
        
        # Ensure the response ends properly
        if reply and not reply[-1] in '.!?':
            # If incomplete, add a period
            if len(reply.split()) > 5:
                reply = reply.rsplit(' ', 1)[0] + '.'
        
        return reply if reply else "I understand. How can I assist you better?"
    except Exception as e:
        print(f"Groq response generation failed: {e}")
        return "I understand. How can I assist you?"

def add_user_message(conversation_id: str, messages: list, text: str, via: str = "text", timestamp: str = None):
    if not text:
        return
    
    ts = timestamp or (datetime.utcnow().isoformat() + "Z")
    sent = sentiment.analyze(text)
    
    user_msg = {
        "message_id": str(uuid.uuid4()),
        "role": "user",
        "text": text,
        "transcript": text,
        "sentiment": sent,
        "via": via,
        "created_at": ts
    }
    db.append_message(conversation_id, user_msg)
    messages.append(user_msg)
    
    bot_response = generate_sentiment_response(sent["label"], text)
    bot_msg = {
        "message_id": str(uuid.uuid4()),
        "role": "assistant",
        "text": bot_response,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "auto_generated": True
    }
    db.append_message(conversation_id, bot_msg)
    messages.append(bot_msg)

def compute_final_sentiment(messages: list):
    stars = [m["sentiment"]["star"] for m in messages if m["role"] == "user" and m.get("sentiment")]
    if not stars:
        return None
    return sentiment.conversation_sentiment(stars)

def create_conversation_flow(conversation_id: str, messages: list):
    if groq is None:
        raise Exception("Groq not configured")
    
    stars = [m["sentiment"]["star"] for m in messages if m["role"] == "user" and m.get("sentiment")]
    if not stars:
        raise Exception("No messages to analyze")
    
    final = sentiment.conversation_sentiment(stars)
    summary = {
        "conversation_id": conversation_id,
        "final_sentiment": {"label": final.get("label"), "score": final.get("score")},
        "n_messages": len([m for m in messages if m["role"] == "user"]),
        "n_positive": len([m for m in messages if m["role"] == "user" and m["sentiment"]["label"] == "positive"]),
        "n_neutral": len([m for m in messages if m["role"] == "user" and m["sentiment"]["label"] == "neutral"]),
        "n_negative": len([m for m in messages if m["role"] == "user" and m["sentiment"]["label"] == "negative"]),
        "sentiment_timeseries": [{"ts": m["created_at"], "star": m["sentiment"]["star"]} for m in messages if m["role"] == "user" and m.get("sentiment")]
    }
    
    flow = groq.create_flow(summary)
    db.set_groq_flow(conversation_id, flow if isinstance(flow, dict) else {"flow_text": flow})
    return flow

def generate_ai_summary_reply(conversation_id: str, messages: list):
    if groq is None:
        raise Exception("Groq not configured")
    
    conv = db.get_conversation(conversation_id)
    flow = conv.get("groq_flow")
    
    if not flow:
        raise Exception("Create flow first")
    
    final = conv.get("final_sentiment") or compute_final_sentiment(messages)
    flow_text = flow if isinstance(flow, str) else (flow.get("flow_text") or str(flow))
    
    reply = groq.generate_final_reply(flow_text, final)
    reply_doc = {
        "message_id": str(uuid.uuid4()),
        "role": "assistant",
        "text": reply,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "groq_generated": True
    }
    
    db.append_message(conversation_id, reply_doc)
    messages.append(reply_doc)
    return reply
