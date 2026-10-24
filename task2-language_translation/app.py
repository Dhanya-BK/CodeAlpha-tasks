"""CodeAlpha Task 1 - Language Translation Tool
Streamlit UI + Google Translate (deep-translator) + gTTS text-to-speech."""
import html
import io
import time

import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS

LANGUAGES = {
    "English": "en", "Hindi": "hi", "Kannada": "kn", "Tamil": "ta", "Telugu": "te",
    "Malayalam": "ml", "Marathi": "mr", "Bengali": "bn", "Gujarati": "gu", "Urdu": "ur",
    "French": "fr", "German": "de", "Spanish": "es", "Italian": "it", "Portuguese": "pt",
    "Russian": "ru", "Japanese": "ja", "Korean": "ko", "Chinese (Simplified)": "zh-CN",
    "Arabic": "ar",
}
QUICK_PHRASES = ["How are you?", "Thank you very much", "Where is the bus stand?", "Good morning"]
MAX_CHARS = 5000

st.set_page_config(page_title="Lingua - Translator", page_icon="🌐", layout="centered")

# ---------- styling ----------
st.markdown(
    """
    <style>
    .hero {text-align:center; padding: 0.5rem 0 1rem 0;}
    .hero h1 {
        font-size: 2.6rem; font-weight: 800; margin-bottom: 0;
        background: linear-gradient(90deg, #6C63FF, #00C9A7);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero p {opacity: 0.7; margin-top: 0.2rem;}
    .result-card {
        background: rgba(108, 99, 255, 0.10);
        border-left: 5px solid #6C63FF;
        border-radius: 12px; padding: 1rem 1.2rem; margin: 0.6rem 0;
        font-size: 1.25rem; line-height: 1.6;
    }
    .result-label {font-size: 0.8rem; letter-spacing: 1px; opacity: 0.6; text-transform: uppercase;}
    div.stButton > button {border-radius: 10px;}
    </style>
    <div class="hero">
        <h1>🌐 Lingua</h1>
        <p>Translate between 20 languages instantly - CodeAlpha AI Internship, Task 1</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- state ----------
st.session_state.setdefault("src", "Auto-detect")
st.session_state.setdefault("tgt_sel", "Kannada")
st.session_state.setdefault("text", "")
st.session_state.setdefault("history", [])


def swap_languages():
    if st.session_state.src == "Auto-detect":
        st.session_state.swap_warn = True
        return
    st.session_state.src, st.session_state.tgt_sel = st.session_state.tgt_sel, st.session_state.src
    if "result" in st.session_state:  # move the translation into the input box
        st.session_state.text = st.session_state.result


def use_phrase(p):
    st.session_state.text = p


def translate_with_retry(text, source, target, tries=3):
    """Google sometimes rate-limits; retry a few times with a growing pause."""
    last_error = None
    for i in range(tries):
        try:
            return GoogleTranslator(source=source, target=target).translate(text), None
        except Exception as e:  # noqa: BLE001
            last_error = e
            time.sleep(1.5 * (i + 1))
    return None, last_error


# ---------- sidebar: history ----------
with st.sidebar:
    st.header("🕘 Recent translations")
    if not st.session_state.history:
        st.caption("Nothing yet - translate something!")
    for h in st.session_state.history:
        with st.expander(f"{h['src']} → {h['tgt']}"):
            st.write(h["text"])
            st.success(h["result"])
    if st.session_state.history and st.button("Clear history"):
        st.session_state.history = []
        st.rerun()

# ---------- language pickers ----------
c1, c2, c3 = st.columns([5, 1, 5])
c1.selectbox("From", ["Auto-detect"] + list(LANGUAGES), key="src")
c2.markdown("<div style='height:1.9rem'></div>", unsafe_allow_html=True)
c2.button("⇄", on_click=swap_languages, help="Swap languages", use_container_width=True)
c3.selectbox("To", list(LANGUAGES), key="tgt_sel")

if st.session_state.pop("swap_warn", False):
    st.info("Pick a specific source language to use the swap button.")

# ---------- input ----------
st.text_area("Enter text", key="text", height=150, max_chars=MAX_CHARS,
             placeholder="Type or paste text here...")
st.caption(f"{len(st.session_state.text)} / {MAX_CHARS} characters")

st.caption("Quick phrases:")
cols = st.columns(len(QUICK_PHRASES))
for col, phrase in zip(cols, QUICK_PHRASES):
    col.button(phrase, key=f"qp_{phrase}", on_click=use_phrase, args=(phrase,), use_container_width=True)

# ---------- translate ----------
if st.button("Translate", type="primary", use_container_width=True):
    text = st.session_state.text.strip()
    if not text:
        st.warning("Please enter some text.")
    elif st.session_state.src == st.session_state.tgt_sel:
        st.warning("Source and target languages are the same.")
    else:
        source = "auto" if st.session_state.src == "Auto-detect" else LANGUAGES[st.session_state.src]
        target = LANGUAGES[st.session_state.tgt_sel]
        with st.spinner("Translating..."):
            result, error = translate_with_retry(text, source, target)
        if result:
            st.session_state.result = result
            st.session_state.result_lang = target
            st.session_state.history.insert(0, {
                "src": st.session_state.src, "tgt": st.session_state.tgt_sel,
                "text": text, "result": result,
            })
            st.session_state.history = st.session_state.history[:10]
            st.session_state.pop("audio", None)
        else:
            st.error(
                "Translation failed after 3 tries. Google may be rate-limiting your network - "
                f"wait a minute or switch networks.\n\nDetails: {error}"
            )

# ---------- output ----------
if "result" in st.session_state:
    st.markdown(
        f"<div class='result-label'>Translation → {html.escape(st.session_state.tgt_sel)}</div>"
        f"<div class='result-card'>{html.escape(st.session_state.result)}</div>",
        unsafe_allow_html=True,
    )
    st.code(st.session_state.result, language=None)  # built-in copy button
    if st.button("🔊 Listen"):
        try:
            buf = io.BytesIO()
            gTTS(st.session_state.result, lang=st.session_state.result_lang).write_to_fp(buf)
            st.session_state.audio = buf.getvalue()
        except Exception as e:  # noqa: BLE001
            st.error(f"Text-to-speech not available for this language: {e}")
    if "audio" in st.session_state:
        st.audio(st.session_state.audio, format="audio/mp3")