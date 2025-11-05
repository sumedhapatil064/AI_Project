# Multilingual News Summarization — Full Starter (Transformers)

## Overview
End-to-end service that takes a long-form news article in any supported language, summarizes it, and optionally outputs in a target language (e.g., English, Hindi, Marathi). This uses Hugging Face Transformers for translation and summarization.

## Features
- Language-agnostic input (auto choose translation pipeline)
- Abstractive summarization using BART/T5
- Optional back-translation to target language
- FastAPI microservice with a single `/summarize` endpoint
- Dockerized for easy deployment

## API
`POST /summarize`
```json
{
  "text": "<long article text>",
  "source_lang": "auto|en|hi|mr|...",
  "target_lang": "en|hi|mr",
  "max_length": 120,
  "min_length": 40
}
```
**Response:**
```json
{"summary": "...", "detected_source": "en", "target_lang": "hi"}
```

## Local Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Then test:
```bash
curl -X POST http://127.0.0.1:8000/summarize -H "Content-Type: application/json"   -d @- <<'JSON'
{"text":"<paste long article here>","source_lang":"auto","target_lang":"en","max_length":120,"min_length":40}
JSON
```

## Models (suggested)
- Summarization: `facebook/bart-large-cnn`
- Translation (to English): `Helsinki-NLP/opus-mt-xx-en` variants (e.g., `Helsinki-NLP/opus-mt-hi-en`, `opus-mt-mul-en`)
- Translation (from English): `Helsinki-NLP/opus-mt-en-xx` variants (e.g., `Helsinki-NLP/opus-mt-en-hi`, `opus-mt-en-mr`)

> Note: First run will download models. You can swap in smaller models for resource-constrained environments.

## Interview Talking Points
- Why chain translation → summarization → back-translation
- Latency/cost: model caching, ONNX export, batch inference
- Quality: ROUGE/BERTScore; guardrails against hallucination
- Domain adaptation via fine-tuning and prompt control

## Production Notes
- Add caching for repeated articles
- Precompile models and mount into the container
- Add tracing (OpenTelemetry) and structured logs