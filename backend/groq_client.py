import os
from openai import OpenAI
import json

class GroqClient:
    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not found")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )
        self.model = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")

    def create_flow(self, summary: dict):
        prompt = f"""You are a conversation flow generator. The input below is a summary of a conversation.

SUMMARY:
{json.dumps(summary, indent=2)}

Create a structured flow/outline describing:
- the emotional tone
- the conversation direction
- recommended assistant response strategy
- key points mentioned by the user

Return ONLY the text, no JSON markers."""

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        return response.output_text

    def generate_final_reply(self, flow: str, final_sentiment: dict):
        prompt = f"""You are an AI assistant. Based on the FLOW and FINAL SENTIMENT below:

FLOW:
{flow}

FINAL SENTIMENT:
{json.dumps(final_sentiment, indent=2)}

Generate a final helpful assistant message that is:
- empathetic to the user's emotional tone
- concise
- meaningful
- based on the conversation summary

Return only the final assistant response."""

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        return response.output_text
