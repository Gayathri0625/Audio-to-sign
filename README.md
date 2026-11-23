# SignSpeak — Mini Backend Demonstrator

**Multilingual Voice-to-Sign Translation Pipeline**

A simplified, self-contained conference-demo prototype that demonstrates the core backend processing pipeline of the **SignSpeak** research project: *AI-Powered Multilingual Voice-to-Sign Language Translation Using a 3D Sign Language Avatar*.

🚀 **Live Demo:** [https://audio-to-sign-system.streamlit.app/](https://audio-to-sign-system.streamlit.app/)

> **Note:** This is NOT the full research implementation. It is a small, reliable prototype designed to run live during a conference presentation to explain how the backend processing works.

---

## Architecture

```text
INPUT (text)
    ↓
LANGUAGE DETECTION (Unicode script analysis)
    ↓
TRANSLATION (local dictionary lookup)
    ↓
TOKENIZATION (lowercase → remove punctuation → split)
    ↓
SIGN MAPPING (dictionary lookup + fallback handling)
    ↓
FINAL SIGN SEQUENCE
```

---

## Project Structure

```text
signspeak-mini-demo/
│
├── app.py                          # Streamlit UI application
├── backend/
│   ├── __init__.py
│   ├── language_detector.py        # Unicode-based language detection
│   ├── translator.py               # Dictionary-based translation
│   ├── tokenizer.py                # Basic NLP tokenization
│   ├── sign_mapper.py              # Sign dictionary lookup + fallback
│   └── pipeline.py                 # Orchestrates all stages
│
├── data/
│   ├── translation_dataset.json    # Predefined translation pairs
│   └── sign_dictionary.json        # Sign language word mappings
│
├── assets/
│   └── README.txt                  # Asset directory placeholder
│
├── requirements.txt
└── README.md                       # This file
```

---

## Installation

```bash
# 1. Navigate to the project directory
cd signspeak-mini-demo

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt
```

---

## How to Run

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`.

**Try the live application:** [SignSpeak – Live Demo](https://audio-to-sign-system.streamlit.app/)

---

## Example Inputs

### English

```text
I am going to the hospital
Hello how are you
Good morning friend
I want to eat food
Thank you doctor
```

### Telugu

```text
నేను ఆసుపత్రికి వెళ్తున్నాను
నేను సంతోషంగా ఉన్నాను
నాకు సహాయం కావాలి
```

### Japanese

```text
私は病院に行きます
私は幸せです
助けてください
```

---

## Backend Stages Explained

### 1. Language Detection (`language_detector.py`)

Uses Unicode character ranges to identify the input language:

- **Telugu**: Unicode block U+0C00–U+0C7F
- **Japanese**: Hiragana (U+3040–U+309F), Katakana (U+30A0–U+30FF), CJK Ideographs (U+4E00–U+9FFF)
- **English**: Basic Latin letters (A–Z, a–z)

The module counts characters in each script range and picks the dominant language.

### 2. Translation (`translator.py`)

Looks up the input text in a predefined JSON dictionary (`translation_dataset.json`).

If the input is English, it passes through unchanged. If the input matches a Telugu or Japanese entry, the corresponding English translation is returned.

### 3. Tokenization (`tokenizer.py`)

Performs basic NLP preprocessing on the English text:

1. Convert to lowercase
2. Remove punctuation using regex
3. Split on whitespace
4. Filter empty tokens

### 4. Sign Mapping (`sign_mapper.py`)

Each token is looked up in the sign dictionary (`sign_dictionary.json`):

- **Match found** → Marked as `sign` with the uppercase gloss (e.g., `HOSPITAL`)
- **No match** → Marked as `fallback` with a warning indicator

### 5. Pipeline Orchestration (`pipeline.py`)

Calls each stage in sequence and returns a comprehensive result dictionary containing all intermediate outputs.

---

## Research Architecture vs. Conference Demo

| Component | Full Research Architecture | Conference Mini Demo |
|---|---|---|
| Speech Input | Whisper ASR | Text input (UI only) |
| Language ID | Whisper / fastText | Unicode script analysis |
| Translation | Neural Machine Translation | Predefined dictionary (JSON) |
| Tokenization | spaCy / NLTK with lemmatization | Basic regex + split |
| Sign Mapping | Sign language corpus + ML matching | Local JSON dictionary |
| Rendering | 3D Avatar (Unity/Blender) | Emoji indicators (🤟 / ❓) |

This mini demo demonstrates the **pipeline concept and data flow** — not the ML models or 3D rendering used in the full research system.

---

## Requirements

- Python 3.8+
- Streamlit ≥ 1.24.0
- No external APIs, no internet connection required
- Works completely offline

---

## License

Research demonstration prototype. Part of the SignSpeak research project.
