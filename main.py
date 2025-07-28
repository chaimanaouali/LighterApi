from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from typing import List

# Use PyTorch-backed model (default backend)
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

app = FastAPI()

class CommentList(BaseModel):
    comments: List[str]

@app.post("/analyze")
def analyze_sentiment(data: CommentList):
    comments = data.comments
    results = classifier(comments)

    counts = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}

    for result in results:
        label = result["label"]
        if label in counts:
            counts[label] += 1
        else:
            counts["NEUTRAL"] += 1

    total = len(comments)
    percentages = {
        "positive": round(100 * counts["POSITIVE"] / total, 2),
        "negative": round(100 * counts["NEGATIVE"] / total, 2),
        "neutral": round(100 * counts["NEUTRAL"] / total, 2)
    }

    return percentages
