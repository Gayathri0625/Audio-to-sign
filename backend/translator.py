"""
SignSpeak Mini Demo — Translator
==================================
Simplified dictionary-based translation using a predefined dataset.

NOTE: The full research architecture uses neural machine translation models.
This module demonstrates the pipeline concept using a small local dictionary.
"""

import json
import os


def load_translation_dataset() -> dict:
    """Load the predefined translation dataset from JSON."""
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "translation_dataset.json"
    )
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def translate_to_english(text: str, language: str) -> dict:
    """
    Translate input text to English using the local dataset.
    
    Args:
        text: Input text in any supported language.
        language: Detected language of the text.
    
    Returns:
        dict with 'english_text', 'method', and 'found' keys.
    """
    # If already English, return as-is
    if language == "English":
        return {
            "english_text": text,
            "method": "No translation needed (English input)",
            "found": True
        }
    
    # Look up in the translation dataset
    dataset = load_translation_dataset()
    
    # Try exact match first
    cleaned_input = text.strip()
    if cleaned_input in dataset:
        return {
            "english_text": dataset[cleaned_input],
            "method": "Mini demo dictionary lookup",
            "found": True
        }
    
    # Try case-insensitive match for safety
    for key, value in dataset.items():
        if key.strip().lower() == cleaned_input.lower():
            return {
                "english_text": value,
                "method": "Mini demo dictionary lookup (case-insensitive)",
                "found": True
            }
    
    # Not found in dataset
    return {
        "english_text": None,
        "method": "Translation unavailable in demo dataset",
        "found": False
    }
