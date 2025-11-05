from typing import Optional, Tuple
from transformers import pipeline

# Lazy pipeline initialization (load on first use)
_summarizer = None
_trans_to_en = {}
_trans_from_en = {}

def get_summarizer():
    global _summarizer
    if _summarizer is None:
        _summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
    return _summarizer

# Map of language codes to translation models (expand as needed)
TO_EN_MODELS = {
    'hi': 'Helsinki-NLP/opus-mt-hi-en',
    'mr': 'Helsinki-NLP/opus-mt-mr-en',
    'auto': 'Helsinki-NLP/opus-mt-mul-en'  # generic multi-to-en
}

FROM_EN_MODELS = {
    'hi': 'Helsinki-NLP/opus-mt-en-hi',
    'mr': 'Helsinki-NLP/opus-mt-en-mr',
    'en': None
}

def get_to_en(lang: str):
    if lang not in _trans_to_en:
        model = TO_EN_MODELS.get(lang, TO_EN_MODELS['auto'])
        _trans_to_en[lang] = pipeline('translation', model=model)
    return _trans_to_en[lang]

def get_from_en(lang: str):
    if lang not in _trans_from_en:
        model = FROM_EN_MODELS.get(lang)
        _trans_from_en[lang] = None if model is None else pipeline('translation', model=model)
    return _trans_from_en[lang]

def maybe_translate_to_en(text: str, source_lang: str) -> Tuple[str, str]:
    if source_lang == 'en':
        return text, 'en'
    translator = get_to_en(source_lang if source_lang in TO_EN_MODELS else 'auto')
    out = translator(text, max_length=512)[0]['translation_text']
    return out, source_lang

def maybe_translate_from_en(text: str, target_lang: str) -> str:
    if target_lang == 'en':
        return text
    translator = get_from_en(target_lang)
    if translator is None:
        return text
    out = translator(text, max_length=512)[0]['translation_text']
    return out

def summarize_article(text: str, source_lang: str = 'auto', target_lang: str = 'en',
                      max_length: int = 120, min_length: int = 40) -> dict:
    # 1) if needed, translate to English
    en_text, detected = (text, 'en') if source_lang == 'en' else maybe_translate_to_en(text, source_lang)
    # 2) summarization
    summ = get_summarizer()(en_text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
    # 3) if needed, back-translate to target
    final_summary = maybe_translate_from_en(summ, target_lang)
    return {"summary": final_summary, "detected_source": detected, "target_lang": target_lang}
