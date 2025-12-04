import uuid
from datetime import datetime

try:
    from pymongo import MongoClient
except Exception as e:
    raise RuntimeError("pymongo required. Install: pip install pymongo") from e

class MongoManager:
    
    def __init__(self, uri: str, db_name: str, collection_name: str):
        if uri is None:
            raise ValueError("MONGO_URI missing!")

        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.collection.create_index("conversation_id", unique=True)

    def start_conversation(self) -> str:
        conversation_id = str(uuid.uuid4())
        doc = {
            "conversation_id": conversation_id,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "messages": [],
            "final_sentiment": None,
            "groq_flow": None,
            "gpt_response": None
        }
        self.collection.insert_one(doc)
        return conversation_id

    def append_message(self, conversation_id: str, message: dict):
        self.collection.update_one(
            {"conversation_id": conversation_id},
            {"$push": {"messages": message},
             "$set": {"updated_at": datetime.utcnow().isoformat() + "Z"}}
        )

    def get_conversation(self, conversation_id: str) -> dict:
        doc = self.collection.find_one({"conversation_id": conversation_id})
        return doc or {"conversation_id": conversation_id, "messages": []}

    def set_final_sentiment(self, conversation_id: str, sentiment_dict: dict):
        sentiment_dict["timestamp"] = datetime.utcnow().isoformat() + "Z"
        self.collection.update_one(
            {"conversation_id": conversation_id},
            {"$set": {"final_sentiment": sentiment_dict}}
        )

    def set_groq_flow(self, conversation_id: str, flow_dict: dict):
        flow_dict["timestamp"] = datetime.utcnow().isoformat() + "Z"
        self.collection.update_one(
            {"conversation_id": conversation_id},
            {"$set": {"groq_flow": flow_dict}}
        )

    def set_gpt_response(self, conversation_id: str, reply_dict: dict):
        reply_dict["timestamp"] = datetime.utcnow().isoformat() + "Z"
        self.collection.update_one(
            {"conversation_id": conversation_id},
            {"$set": {"gpt_response": reply_dict}}
        )
