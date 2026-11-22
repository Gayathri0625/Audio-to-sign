"""
SignSpeak Mini Demo — Sign Mapper
====================================
Maps English word tokens to sign language glosses using a local dictionary.
Tokens not found in the dictionary receive a fallback indicator.

NOTE: The full research architecture maps tokens to 3D avatar animations.
This module demonstrates the mapping + fallback concept.
"""

import json
import os


def load_sign_dictionary() -> dict:
    """Load the predefined sign dictionary from JSON."""
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "sign_dictionary.json"
    )
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def map_tokens_to_signs(tokens: list) -> dict:
    """
    Map a list of word tokens to sign language entries.
    
    For each token:
        - If found in sign dictionary → type='sign', show gloss
        - If NOT found → type='fallback', show fallback indicator
    
    Args:
        tokens: List of lowercase English word tokens.
    
    Returns:
        dict with 'mappings', 'sign_count', 'fallback_count', and 'sequence' keys.
    """
    dictionary = load_sign_dictionary()
    
    mappings = []
    sign_count = 0
    fallback_count = 0
    
    for token in tokens:
        if token in dictionary:
            entry = dictionary[token]
            mappings.append({
                "token": token,
                "type": "sign",
                "gloss": entry["gloss"],
                "icon": "\U0001f91f"  # 🤟
            })
            sign_count += 1
        else:
            mappings.append({
                "token": token,
                "type": "fallback",
                "gloss": token.upper(),
                "icon": "\u2753"  # ❓
            })
            fallback_count += 1
    
    # Build the final display sequence
    sequence = []
    for m in mappings:
        sequence.append(f"{m['icon']} {m['gloss']}")
    
    return {
        "mappings": mappings,
        "sign_count": sign_count,
        "fallback_count": fallback_count,
        "sequence": sequence
    }
