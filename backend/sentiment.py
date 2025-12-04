from typing import List, Dict, Any
import numpy as np

_tokenizer = None
_model = None

def _ensure_model_loaded(model_name: str):
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        try:
            from transformers import AutoTokenizer, AutoModelForSequenceClassification
            import torch
        except Exception as e:
            raise RuntimeError("transformers and torch required. Install: pip install transformers torch") from e

        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _model = AutoModelForSequenceClassification.from_pretrained(model_name)
        _model.eval()
    return _tokenizer, _model


class SentimentAnalyzer:
    
    def __init__(self, model_name: str = "nlptown/bert-base-multilingual-uncased-sentiment"):
        self.model_name = model_name

    def analyze(self, text: str) -> Dict[str, Any]:
        if not text:
            return {"label": "neutral", "star": 3, "confidence": 1.0, "probs": [0, 0, 1.0, 0, 0]}

        tokenizer, model = _ensure_model_loaded(self.model_name)

        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with __import__("torch").no_grad():
            outputs = model(**inputs)
            logits = outputs.logits[0].numpy()

        exp = np.exp(logits - np.max(logits))
        probs = (exp / exp.sum()).tolist()

        star = int(np.argmax(probs)) + 1
        confidence = float(probs[star - 1])

        if star in (1, 2):
            label = "negative"
        elif star == 3:
            label = "neutral"
        else:
            label = "positive"

        return {"label": label, "star": star, "confidence": confidence, "probs": probs}

    def conversation_sentiment(self, stars: List[int], method: str = "average_star") -> Dict[str, Any]:
        if not stars:
            return {"label": "neutral", "score": 3.0, "method": method}

        if method == "average_star":
            avg = float(np.mean(stars))
        elif method == "recency_weighted":
            n = len(stars)
            weights = np.arange(1, n + 1)
            avg = float(np.average(stars, weights=weights))
        else:
            avg = float(np.mean(stars))

        if avg <= 2.5:
            label = "negative"
        elif avg <= 3.5:
            label = "neutral"
        else:
            label = "positive"

        return {"label": label, "score": avg, "method": method}
