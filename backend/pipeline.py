"""
SignSpeak Mini Demo — Main Pipeline
======================================
Orchestrates the complete backend processing pipeline:

    Input → Language Detection → Translation → Tokenization → Sign Mapping

This is the central module that ties all stages together.
"""

from backend.language_detector import detect_language
from backend.translator import translate_to_english
from backend.tokenizer import tokenize
from backend.sign_mapper import map_tokens_to_signs


def process_input(text: str, selected_language: str = "Auto Detect") -> dict:
    """
    Run the full SignSpeak backend pipeline on input text.
    
    Pipeline Stages:
        1. Language Detection
        2. Translation to English
        3. Tokenization
        4. Sign Mapping (with fallback handling)
    
    Args:
        text: Raw input text (any supported language).
        selected_language: Language dropdown selection.
    
    Returns:
        dict containing results from every pipeline stage.
    """
    # Stage 1: Language Detection
    detection_result = detect_language(text, selected_language)
    detected_language = detection_result["language"]
    
    # Stage 2: Translation to English
    translation_result = translate_to_english(text, detected_language)
    
    # If translation was not found, return partial results
    if not translation_result["found"]:
        return {
            "success": False,
            "raw_input": text,
            "detection": detection_result,
            "translation": translation_result,
            "tokenization": None,
            "sign_mapping": None,
            "error": "Translation unavailable in demo dataset."
        }
    
    english_text = translation_result["english_text"]
    
    # Stage 3: Tokenization
    tokenization_result = tokenize(english_text)
    
    # Stage 4: Sign Mapping
    sign_mapping_result = map_tokens_to_signs(tokenization_result["tokens"])
    
    return {
        "success": True,
        "raw_input": text,
        "detection": detection_result,
        "translation": translation_result,
        "tokenization": tokenization_result,
        "sign_mapping": sign_mapping_result
    }
