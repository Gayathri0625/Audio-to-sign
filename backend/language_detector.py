"""
SignSpeak Mini Demo — Language Detector
========================================
Simplified demo-based language detection using Unicode script analysis.

NOTE: The full research architecture uses Whisper/fastText for language
identification. This module demonstrates the pipeline concept only.
"""


def detect_language(text: str, selected_language: str = "Auto Detect") -> dict:
    """
    Detect the language of input text.
    
    If user selected a specific language, use that.
    Otherwise, use Unicode range heuristics.
    
    Returns:
        dict with 'language', 'method', and 'confidence' keys.
    """
    # If user explicitly selected a language, trust that
    if selected_language != "Auto Detect":
        return {
            "language": selected_language,
            "method": "User-selected",
            "confidence": "User-specified"
        }
    
    # Count characters in each script range
    telugu_count = 0
    japanese_count = 0
    latin_count = 0
    
    for char in text:
        code_point = ord(char)
        # Telugu Unicode block: U+0C00 to U+0C7F
        if 0x0C00 <= code_point <= 0x0C7F:
            telugu_count += 1
        # Japanese: Hiragana (3040-309F), Katakana (30A0-30FF), CJK (4E00-9FFF)
        elif (0x3040 <= code_point <= 0x309F or
              0x30A0 <= code_point <= 0x30FF or
              0x4E00 <= code_point <= 0x9FFF):
            japanese_count += 1
        # Basic Latin letters
        elif (0x0041 <= code_point <= 0x005A or
              0x0061 <= code_point <= 0x007A):
            latin_count += 1
    
    # Determine language based on highest count
    counts = {
        "Telugu": telugu_count,
        "Japanese": japanese_count,
        "English": latin_count
    }
    
    detected = max(counts, key=counts.get)
    
    # If no characters matched any script
    if counts[detected] == 0:
        detected = "Unknown"
    
    return {
        "language": detected,
        "method": "Unicode script analysis",
        "confidence": "Demo-based detection"
    }
