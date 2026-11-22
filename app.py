"""
SignSpeak — Mini Backend Demonstrator  (v2 — Enhanced)
=======================================================
Conference-demo prototype demonstrating the core backend pipeline of
the SignSpeak research project with animated stage progression,
color-coded tokens, gloss comparison, and per-stage timing.

Run with:
    streamlit run app.py
"""

import streamlit as st
import json
import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))

from backend.pipeline import process_input


# ─────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SignSpeak — Mini Backend Demonstrator",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ─────────────────────────────────────────────
# CSS — Dark theme + magenta + new improvements
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    /* ── Global ── */
    html, body, .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0d0d1a 0%, #150a26 50%, #0d0d1a 100%);
        color: #e8e8f0;
    }

    /* ── Header ── */
    .main-header { text-align: center; padding: 2rem 0 0.4rem 0; }
    .main-header h1 {
        font-size: 2.8rem;
        background: linear-gradient(120deg, #ff2d95 0%, #c850c0 50%, #ff6fd8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
    }
    .main-header .subtitle {
        font-size: 1.05rem;
        color: #b0a0c8;
        font-weight: 400;
        letter-spacing: 0.3px;
    }
    .disclaimer {
        text-align: center;
        font-size: 0.78rem;
        color: #7a6a9a;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(200,80,192,0.15);
        border-radius: 8px;
        padding: 0.55rem 1.2rem;
        margin: 0.8rem auto 1.4rem auto;
        max-width: 760px;
    }

    /* ── Pipeline flow ── */
    .pipeline-flow {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        gap: 0;
        margin: 0.5rem 0 1rem 0;
    }
    .pipeline-stage {
        background: rgba(200,80,192,0.1);
        border: 1px solid rgba(200,80,192,0.25);
        padding: 0.45rem 0.9rem;
        border-radius: 8px;
        font-size: 0.78rem;
        font-weight: 600;
        color: #d8c8f0;
        text-align: center;
        transition: all 0.3s ease;
    }
    .pipeline-stage.active {
        background: rgba(255,45,149,0.2);
        border-color: #ff2d95;
        color: #ffffff;
        box-shadow: 0 0 12px rgba(255,45,149,0.35);
        transform: scale(1.08);
    }
    .pipeline-stage.done {
        background: rgba(74,222,128,0.1);
        border-color: rgba(74,222,128,0.4);
        color: #4ade80;
    }
    .pipeline-arrow { color: #ff2d95; font-size: 1.1rem; padding: 0 0.25rem; }

    /* ── Step cards ── */
    .step-card {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(200,80,192,0.18);
        border-radius: 12px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 0.9rem;
        transition: border-color 0.3s;
    }
    .step-card:hover { border-color: rgba(200,80,192,0.35); }
    .step-card h3 { color: #ff2d95; font-size: 1rem; margin-bottom: 0.4rem; font-weight: 700; }
    .step-card .label {
        font-size: 0.7rem;
        color: #9080b0;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 0.35rem;
    }

    /* ── Token pills (color-coded) ── */
    .token-pill-sign {
        display: inline-block;
        background: rgba(74,222,128,0.12);
        border: 1px solid rgba(74,222,128,0.35);
        color: #d0fce8;
        padding: 0.28rem 0.7rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.88rem;
    }
    .token-pill-fallback {
        display: inline-block;
        background: rgba(251,191,36,0.12);
        border: 1px solid rgba(251,191,36,0.35);
        color: #fde68a;
        padding: 0.28rem 0.7rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.88rem;
    }
    .token-legend {
        display: flex;
        gap: 1rem;
        align-items: center;
        margin-top: 0.5rem;
        font-size: 0.78rem;
        color: #9080b0;
    }
    .legend-dot-sign { width:10px;height:10px;border-radius:50%;background:#4ade80;display:inline-block;margin-right:4px; }
    .legend-dot-fb   { width:10px;height:10px;border-radius:50%;background:#fbbf24;display:inline-block;margin-right:4px; }

    /* ── Mapping table ── */
    .sign-row {
        display: flex;
        align-items: center;
        padding: 0.38rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.04);
    }
    .sign-token  { flex: 1; font-family: 'JetBrains Mono', monospace; color: #c0b8d8; font-size:0.9rem; }
    .sign-icon   { flex: 0.6; text-align: center; font-size: 1.25rem; }
    .sign-gloss  { flex: 1.2; font-weight: 600; font-size:0.9rem; }
    .sign-type-sign     { color: #4ade80; flex:1; font-size:0.85rem; }
    .sign-type-fallback { color: #fbbf24; flex:1; font-size:0.85rem; }
    .sign-timing { flex: 0.8; text-align:right; font-size:0.73rem; color:#6a5a8a; font-family: 'JetBrains Mono', monospace; }

    /* ── Gloss comparison ── */
    .gloss-compare {
        display: flex;
        gap: 1.5rem;
        margin-top: 0.6rem;
    }
    .gloss-box {
        flex: 1;
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(200,80,192,0.12);
        border-radius: 10px;
        padding: 0.8rem 1rem;
    }
    .gloss-box .gloss-label {
        font-size: 0.7rem;
        color: #9080b0;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.4rem;
    }
    .gloss-box .gloss-text {
        font-size: 0.95rem;
        color: #e8e8f0;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1.6;
    }
    .gloss-box .gloss-sequence {
        font-size: 1rem;
        color: #c850c0;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        line-height: 1.8;
    }

    /* ── Sequence bar ── */
    .sequence-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        align-items: center;
        padding: 0.9rem 1rem;
        background: rgba(255,255,255,0.02);
        border-radius: 10px;
        margin-top: 0.5rem;
    }
    .seq-item-sign {
        background: rgba(200,80,192,0.12);
        border: 1px solid rgba(200,80,192,0.28);
        padding: 0.38rem 0.75rem;
        border-radius: 8px;
        font-size: 0.9rem;
    }
    .seq-item-fallback {
        background: rgba(251,191,36,0.08);
        border: 1px solid rgba(251,191,36,0.25);
        padding: 0.38rem 0.75rem;
        border-radius: 8px;
        font-size: 0.9rem;
    }
    .seq-arrow { color: #ff2d95; font-size: 1rem; font-weight: bold; }

    /* ── Timing badge ── */
    .timing-badge {
        display: inline-block;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 0.15rem 0.6rem;
        font-size: 0.72rem;
        font-family: 'JetBrains Mono', monospace;
        color: #9080b0;
        margin-left: 0.5rem;
        vertical-align: middle;
    }
    .timing-total {
        background: rgba(200,80,192,0.12);
        border-color: rgba(200,80,192,0.25);
        color: #ff2d95;
    }

    /* ── Architecture boxes ── */
    .arch-box {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        font-size: 0.84rem;
    }
    .arch-box h4 { margin-bottom: 0.5rem; font-size: 0.88rem; }
    .arch-box .arch-row {
        padding: 0.2rem 0;
        color: #c0b8d8;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
    }
    .arch-box .arch-arrow { color: #ff2d95; margin: 0 0.3rem; }

    /* ── Misc ── */
    div[data-testid="stExpander"] {
        background: rgba(255,255,255,0.015);
        border: 1px solid rgba(200,80,192,0.1);
        border-radius: 10px;
    }
    .stMetric { background: rgba(255,255,255,0.03); border-radius: 8px; padding: 0.5rem; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🤟 SignSpeak — Mini Backend Demonstrator</h1>
    <div class="subtitle">Multilingual Voice-to-Sign Language Translation Pipeline · v2 Enhanced</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="disclaimer">
    ⚠️ Simplified <strong>offline</strong> prototype demonstrating the backend pipeline
    of the SignSpeak research paper. Not the full research implementation.
    No external APIs or internet connection required.
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Animated Pipeline Flow (state-aware)
# ─────────────────────────────────────────────
STAGES = ["📥 INPUT", "🌐 DETECT", "🔄 TRANSLATE", "✂️ TOKENIZE", "🤟 SIGN MAP", "📤 OUTPUT"]

def render_pipeline(active_index: int = -1, done_count: int = 0):
    parts = []
    for i, s in enumerate(STAGES):
        if i < done_count:
            cls = "done"
        elif i == active_index:
            cls = "active"
        else:
            cls = ""
        parts.append(f'<div class="pipeline-stage {cls}">{s}</div>')
        if i < len(STAGES) - 1:
            parts.append('<span class="pipeline-arrow">→</span>')
    st.markdown(
        f'<div class="pipeline-flow">{"".join(parts)}</div>',
        unsafe_allow_html=True
    )

pipeline_placeholder = st.empty()
with pipeline_placeholder:
    render_pipeline()

st.markdown("---")


# ─────────────────────────────────────────────
# Sample Sentences
# ─────────────────────────────────────────────
SAMPLE_SENTENCES = {
    "English — \"I am going to the hospital\"":   "I am going to the hospital",
    "English — \"Hello how are you\"":            "Hello how are you",
    "English — \"Good morning friend\"":          "Good morning friend",
    "English — \"I want to eat food\"":           "I want to eat food",
    "English — \"Thank you doctor\"":             "Thank you doctor",
    "English — \"I am sick\"":                    "I am sick",
    "English — \"I need medicine\"":              "I need medicine",
    "English — \"I will come tomorrow\"":         "I will come tomorrow",
    "Telugu — \"నేను ఆసుపత్రికి వెళ్తున్నాను\"": "నేను ఆసుపత్రికి వెళ్తున్నాను",
    "Telugu — \"నేను సంతోషంగా ఉన్నాను\"":       "నేను సంతోషంగా ఉన్నాను",
    "Telugu — \"నాకు సహాయం కావాలి\"":           "నాకు సహాయం కావాలి",
    "Telugu — \"నేను నీళ్ళు తాగుతున్నాను\"":    "నేను నీళ్ళు తాగుతున్నాను",
    "Japanese — \"私は病院に行きます\"":           "私は病院に行きます",
    "Japanese — \"私は幸せです\"":                "私は幸せです",
    "Japanese — \"助けてください\"":              "助けてください",
    "Japanese — \"水を飲んでいます\"":            "水を飲んでいます",
}


# ─────────────────────────────────────────────
# Input Section
# ─────────────────────────────────────────────
col_input, col_config = st.columns([2, 1])

with col_input:
    st.markdown("### 📝 Enter Speech / Text")
    sample_choice = st.selectbox(
        "Quick-load a sample sentence:",
        ["(Type your own below)"] + list(SAMPLE_SENTENCES.keys()),
        index=0,
    )
    default_text = SAMPLE_SENTENCES.get(sample_choice, "")
    user_input = st.text_area(
        "Input text:",
        value=default_text,
        height=95,
        placeholder="Type or select a sample sentence above…",
    )

with col_config:
    st.markdown("### ⚙️ Settings")
    language_option = st.selectbox(
        "Demo Language:",
        ["Auto Detect", "English", "Telugu", "Japanese"],
        index=0,
    )
    animate_toggle = st.toggle("Animate pipeline stages", value=True)
    st.markdown("""
    <div style="font-size:0.76rem; color:#9080b0; margin-top:0.5rem;">
        <strong>Green pill</strong> = matched sign<br>
        <strong>Yellow pill</strong> = fallback (no sign found)<br>
        Toggle animation for live demos.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Process Button
# ─────────────────────────────────────────────
st.markdown("")
process_clicked = st.button("🚀  Process Input", use_container_width=True, type="primary")


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def animate_stage(placeholder, active_idx, done_count, delay=0.45):
    """Update the pipeline flow diagram to highlight a stage."""
    if animate_toggle:
        with placeholder:
            render_pipeline(active_index=active_idx, done_count=done_count)
        time.sleep(delay)


# ─────────────────────────────────────────────
# Results
# ─────────────────────────────────────────────
if process_clicked:
    if not user_input or not user_input.strip():
        st.warning("Please enter some text or select a sample sentence.")
        st.stop()

    raw = user_input.strip()

    # ── Animated pipeline run ──────────────────
    timings = {}

    # Stage 0 — Input
    animate_stage(pipeline_placeholder, 0, 0, delay=0.4)

    # Stage 1 — Language Detection
    animate_stage(pipeline_placeholder, 1, 1, delay=0.5)
    t0 = time.perf_counter()
    from backend.language_detector import detect_language
    detection = detect_language(raw, language_option)
    timings["detection"] = (time.perf_counter() - t0) * 1000

    # Stage 2 — Translation
    animate_stage(pipeline_placeholder, 2, 2, delay=0.5)
    t0 = time.perf_counter()
    from backend.translator import translate_to_english
    translation = translate_to_english(raw, detection["language"])
    timings["translation"] = (time.perf_counter() - t0) * 1000

    # Stage 3 — Tokenization
    animate_stage(pipeline_placeholder, 3, 3, delay=0.5)
    t0 = time.perf_counter()
    from backend.tokenizer import tokenize
    tokenization = None
    if translation["found"]:
        tokenization = tokenize(translation["english_text"])
    timings["tokenization"] = (time.perf_counter() - t0) * 1000

    # Stage 4 — Sign Mapping
    animate_stage(pipeline_placeholder, 4, 4, delay=0.5)
    t0 = time.perf_counter()
    from backend.sign_mapper import map_tokens_to_signs
    sign_mapping = None
    if tokenization:
        sign_mapping = map_tokens_to_signs(tokenization["tokens"])
    timings["sign_mapping"] = (time.perf_counter() - t0) * 1000

    # Stage 5 — Output (all done)
    animate_stage(pipeline_placeholder, -1, 6, delay=0.3)

    total_ms = sum(timings.values())

    st.markdown("---")

    # ── Timing summary bar ─────────────────────
    st.markdown(
        f"**Pipeline complete** "
        f'<span class="timing-badge timing-total">⏱ Total: {total_ms:.2f} ms</span>',
        unsafe_allow_html=True
    )
    t_cols = st.columns(4)
    stage_labels = [
        ("🌐 Detection",   timings["detection"]),
        ("🔄 Translation", timings["translation"]),
        ("✂️ Tokenize",    timings["tokenization"]),
        ("🤟 Sign Map",    timings["sign_mapping"]),
    ]
    for col, (label, ms) in zip(t_cols, stage_labels):
        col.metric(label, f"{ms:.2f} ms")

    st.markdown("")

    # ── Step 1: Language Detection ─────────────
    st.markdown(f"""
    <div class="step-card">
        <div class="label">Language Detection — Simplified Demo Logic
            <span class="timing-badge">{timings['detection']:.2f} ms</span>
        </div>
        <h3>Step 1 — Language Detection</h3>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Detected Language", detection["language"])
    c2.metric("Method", detection["method"])
    c3.metric("Confidence", detection["confidence"])

    # ── Step 2: Translation ────────────────────
    st.markdown(f"""
    <div class="step-card">
        <div class="label">Translation — Mini Demo Dictionary
            <span class="timing-badge">{timings['translation']:.2f} ms</span>
        </div>
        <h3>Step 2 — English Representation</h3>
    </div>
    """, unsafe_allow_html=True)

    if not translation["found"]:
        st.error("Translation unavailable in demo dataset.")
        st.caption(
            "The input is not in the predefined mini-dictionary. "
            "Try one of the sample sentences from the dropdown."
        )
        st.stop()

    st.success(f"**English text:** {translation['english_text']}")
    st.caption(f"Method: {translation['method']}")

    # ── Step 3: Tokenization ───────────────────
    st.markdown(f"""
    <div class="step-card">
        <div class="label">NLP Tokenization
            <span class="timing-badge">{timings['tokenization']:.2f} ms</span>
        </div>
        <h3>Step 3 — Tokenization <small style="font-weight:400; font-size:0.82rem; color:#9080b0;">
            (color = sign match prediction)</small></h3>
    </div>
    """, unsafe_allow_html=True)

    # Pre-check each token for coloring
    with open(os.path.join(os.path.dirname(__file__), "data", "sign_dictionary.json"), encoding="utf-8") as _f:
        _dict = json.load(_f)

    pills_html = ""
    for tok in tokenization["tokens"]:
        cls = "token-pill-sign" if tok in _dict else "token-pill-fallback"
        pills_html += f'<span class="{cls}">{tok}</span> '

    st.markdown(pills_html, unsafe_allow_html=True)
    st.markdown("""
    <div class="token-legend">
        <span><span class="legend-dot-sign"></span>Sign available</span>
        <span><span class="legend-dot-fb"></span>Will use fallback</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption(f"Token count: {tokenization['count']}")

    # ── Step 4: Sign Mapping ───────────────────
    st.markdown(f"""
    <div class="step-card">
        <div class="label">Sign Language Mapping + Fallback Handling
            <span class="timing-badge">{timings['sign_mapping']:.2f} ms</span>
        </div>
        <h3>Step 4 — Sign Mapping</h3>
    </div>
    """, unsafe_allow_html=True)

    sm = sign_mapping

    # Header row
    table_rows = """
    <div class="sign-row" style="border-bottom:2px solid rgba(200,80,192,0.2); font-weight:700; color:#b0a0c8; padding-bottom:0.4rem;">
        <div class="sign-token">Token</div>
        <div class="sign-icon">Icon</div>
        <div class="sign-gloss">Gloss</div>
        <div style="flex:1; font-size:0.85rem;">Type</div>
        <div class="sign-timing">ms</div>
    </div>"""

    per_token_ms = timings["sign_mapping"] / max(len(sm["mappings"]), 1)
    for m in sm["mappings"]:
        type_class = "sign-type-sign" if m["type"] == "sign" else "sign-type-fallback"
        type_label = "✅ Sign" if m["type"] == "sign" else "⚠️ Fallback"
        table_rows += f"""
        <div class="sign-row">
            <div class="sign-token">{m['token']}</div>
            <div class="sign-icon">{m['icon']}</div>
            <div class="sign-gloss">{m['gloss']}</div>
            <div class="{type_class}">{type_label}</div>
            <div class="sign-timing">{per_token_ms:.3f}</div>
        </div>"""

    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.02); border-radius:10px; padding:0.8rem;">
        {table_rows}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    m_cols = st.columns(3)
    m_cols[0].metric("Total Tokens", tokenization["count"])
    m_cols[1].metric("✅ Signs Matched", sm["sign_count"])
    m_cols[2].metric("⚠️ Fallbacks", sm["fallback_count"])

    if sm["fallback_count"] > 0:
        st.info(
            "💡 **Fallback indicators** preserve information flow when a sign asset "
            "is unavailable. They do **not** represent sign-language translations. "
            "The full research system uses a larger sign corpus to minimise fallbacks."
        )

    # ── Gloss Comparison Table ─────────────────
    st.markdown("#### 📊 Gloss Comparison")

    original_words = " · ".join(tokenization["tokens"])
    gloss_sequence = "  →  ".join(
        f"{m['icon']} {m['gloss']}" for m in sm["mappings"]
    )
    sign_only_gloss = "  →  ".join(
        m["gloss"] for m in sm["mappings"] if m["type"] == "sign"
    )

    st.markdown(f"""
    <div class="gloss-compare">
        <div class="gloss-box">
            <div class="gloss-label">Original Tokens</div>
            <div class="gloss-text">{original_words}</div>
        </div>
        <div class="gloss-box">
            <div class="gloss-label">Full Gloss Sequence (with fallbacks)</div>
            <div class="gloss-sequence">{gloss_sequence}</div>
        </div>
        <div class="gloss-box">
            <div class="gloss-label">Sign-Only Gloss</div>
            <div class="gloss-sequence" style="color:#4ade80;">{sign_only_gloss}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # ── Step 5: Final Sequence ─────────────────
    st.markdown("""
    <div class="step-card"><h3>Step 5 — Final Sign Sequence</h3></div>
    """, unsafe_allow_html=True)

    seq_parts = []
    for i, m in enumerate(sm["mappings"]):
        cls = "seq-item-sign" if m["type"] == "sign" else "seq-item-fallback"
        seq_parts.append(f'<span class="{cls}">{m["icon"]} {m["gloss"]}</span>')
        if i < len(sm["mappings"]) - 1:
            seq_parts.append('<span class="seq-arrow"> → </span>')

    st.markdown(
        f'<div class="sequence-bar">{"".join(seq_parts)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── Backend Processing View ────────────────
    with st.expander("🔍  View Backend Processing Log", expanded=False):
        st.markdown("#### Complete Intermediate Pipeline Outputs")
        st.caption("Every value produced at each stage of the backend pipeline.")
        st.markdown("---")

        st.markdown("**Raw Input:**")
        st.code(raw, language=None)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Detected Language:**")
            st.code(detection["language"])
            st.markdown("**Detection Method:**")
            st.code(detection["method"])
        with col_b:
            st.markdown("**Translated English Text:**")
            st.code(translation["english_text"])
            st.markdown("**Translation Method:**")
            st.code(translation["method"])

        st.markdown("**Tokens:**")
        st.code(json.dumps(tokenization["tokens"], indent=2), language="json")

        st.markdown("**Mapping Results:**")
        for m in sm["mappings"]:
            label = "🤟 SIGN" if m["type"] == "sign" else "❓ FALLBACK"
            st.text(f"  {m['token']:15s}  →  {label}")

        st.markdown("**Full Mapping JSON:**")
        mapping_json = [
            {"token": m["token"], "type": m["type"], "gloss": m["gloss"]}
            for m in sm["mappings"]
        ]
        st.code(json.dumps(mapping_json, indent=2), language="json")

        st.markdown("**Stage Timings (ms):**")
        timing_json = {k: f"{v:.3f} ms" for k, v in timings.items()}
        timing_json["TOTAL"] = f"{total_ms:.3f} ms"
        st.code(json.dumps(timing_json, indent=2), language="json")

    # ── Architecture comparison ────────────────
    with st.expander("📐  Research Architecture vs. Conference Demo", expanded=False):
        col_r, col_d = st.columns(2)

        with col_r:
            st.markdown("""
            <div class="arch-box">
                <h4>🔬 Full Research Architecture</h4>
                <div class="arch-row">🎙️ Audio Input (Microphone)</div>
                <div class="arch-row"><span class="arch-arrow">↓</span> Whisper ASR (Speech-to-Text)</div>
                <div class="arch-row"><span class="arch-arrow">↓</span> fastText / Whisper Language ID</div>
                <div class="arch-row"><span class="arch-arrow">↓</span> Neural Machine Translation</div>
                <div class="arch-row"><span class="arch-arrow">↓</span> spaCy / NLTK (Lemmatization)</div>
                <div class="arch-row"><span class="arch-arrow">↓</span> Sign Language Corpus Mapping</div>
                <div class="arch-row"><span class="arch-arrow">↓</span> 3D Avatar Rendering (Unity)</div>
            </div>
            """, unsafe_allow_html=True)

        with col_d:
            st.markdown("""
            <div class="arch-box">
                <h4>🎯 Conference Mini Demo</h4>
                <div class="arch-row">⌨️ Text Input (Streamlit UI)</div>
                <div class="arch-row"><span class="arch-arrow">↓</span> Unicode Script Analysis</div>
                <div class="arch-row"><span class="arch-arrow">↓</span> User selection / heuristics</div>
                <div class="arch-row"><span class="arch-arrow">↓</span> JSON Dictionary Lookup</div>
                <div class="arch-row"><span class="arch-arrow">↓</span> Regex Tokenization</div>
                <div class="arch-row"><span class="arch-arrow">↓</span> Local Sign Dictionary (80 words)</div>
                <div class="arch-row"><span class="arch-arrow">↓</span> Emoji Gloss + Fallback Display</div>
            </div>
            """, unsafe_allow_html=True)

        st.caption(
            "This mini demo proves the **pipeline concept and data-flow logic** — "
            "not the ML models or 3D avatar of the full research system."
        )


# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#6a5a8a; font-size:0.77rem; padding:0.8rem 0;">
    <strong>SignSpeak</strong> — AI-Powered Multilingual Voice-to-Sign Language Translation
    Using a 3D Sign Language Avatar<br>
    Mini Backend Demonstrator v2 · Conference Prototype · Fully Offline
</div>
""", unsafe_allow_html=True)
