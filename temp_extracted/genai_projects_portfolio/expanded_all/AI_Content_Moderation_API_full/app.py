from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="Content Moderation API")
classifier = pipeline("text-classification", model="unitary/toxic-bert", return_all_scores=True)

class TextIn(BaseModel):
    text: str

@app.post("/moderate")
def moderate(inp: TextIn):
    scores = classifier(inp.text)
    return {"scores": scores}
