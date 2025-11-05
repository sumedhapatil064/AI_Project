from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
from pipeline import summarize_article

app = FastAPI(title="Multilingual News Summarization API")

class SummarizeIn(BaseModel):
    text: str = Field(..., description="Long article text to summarize")
    source_lang: str = Field("auto", description="Source language code or 'auto'")
    target_lang: str = Field("en", description="Target language code (en|hi|mr)")
    max_length: int = Field(120, ge=20, le=300)
    min_length: int = Field(40, ge=10, le=150)

@app.post("/summarize")
def summarize(payload: SummarizeIn):
    result = summarize_article(payload.text, payload.source_lang, payload.target_lang, payload.max_length, payload.min_length)
    return result

@app.get("/health")
def health():
    return {"status": "ok"}
