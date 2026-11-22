"""
SignSpeak Mini Demo — Tokenizer
=================================
Basic NLP tokenization: lowercase, remove punctuation, split into tokens.

NOTE: The full research architecture uses advanced NLP tokenization
(spaCy, NLTK) with lemmatization and stop-word handling.
"""

import re


def tokenize(text: str) -> dict:
    """
    Tokenize English text into individual word tokens.
    
    Steps:
        1. Convert to lowercase
        2. Remove punctuation
        3. Split on whitespace
        4. Filter empty tokens
    
    Args:
        text: English text to tokenize.
    
    Returns:
        dict with 'tokens', 'original_text', and 'count' keys.
    """
    # Step 1: Convert to lowercase
    lowered = text.lower()
    
    # Step 2: Remove punctuation (keep only letters, numbers, spaces)
    cleaned = re.sub(r'[^\w\s]', '', lowered)
    
    # Step 3: Split on whitespace
    raw_tokens = cleaned.split()
    
    # Step 4: Filter empty strings
    tokens = [t for t in raw_tokens if t.strip()]
    
    return {
        "tokens": tokens,
        "original_text": text,
        "count": len(tokens)
    }
