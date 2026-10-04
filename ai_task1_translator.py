"""
AI Task 1: Language Translation Tool - Horizon TechX
UI: Streamlit | API: Google Translate (via deep-translator) | Extra: text-to-speech

Run:  streamlit run ai_task1_translator.py
"""
import io

import streamlit as st
from deep_translator import GoogleTranslator

try:
    from gtts import gTTS
    HAS_TTS = True
except ImportError:
    HAS_TTS = False

# name -> language code
LANGUAGES = {
    "English": "en", "Hindi": "hi", "Marathi": "mr", "Gujarati": "gu",
    "Tamil": "ta", "Telugu": "te", "Kannada": "kn", "Bengali": "bn",
    "Urdu": "ur", "French": "fr", "German": "de", "Spanish": "es",
    "Italian": "it", "Japanese": "ja", "Korean": "ko",
    "Chinese (Simplified)": "zh-CN", "Arabic": "ar", "Russian": "ru",
}
MAX_CHARS = 4500  # Google Translate per-request limit is 5000


def translate_text(text, source_name, target_name):
    """Send text to the translation API and return translated text."""
    source = "auto" if source_name == "Auto-detect" else LANGUAGES[source_name]
    target = LANGUAGES[target_name]
    return GoogleTranslator(source=source, target=target).translate(text)


def text_to_speech(text, lang_code):
    """Return MP3 bytes for the given text."""
    buffer = io.BytesIO()
    gTTS(text=text, lang=lang_code.split("-")[0]).write_to_fp(buffer)
    return buffer.getvalue()


def main():
    st.set_page_config(page_title="Language Translator", page_icon="🌐")
    st.title("🌐 Language Translation Tool")
    st.caption("Horizon TechX - AI Internship | Task 1")

    col1, col2 = st.columns(2)
    source = col1.selectbox("From", ["Auto-detect"] + list(LANGUAGES), index=0)
    target = col2.selectbox("To", list(LANGUAGES), index=1)

    text = st.text_area("Enter text to translate", height=150, max_chars=MAX_CHARS)

    if st.button("Translate", type="primary"):
        if not text.strip():
            st.warning("Please enter some text first.")
        elif source == target:
            st.info("Source and target languages are the same.")
        else:
            try:
                with st.spinner("Translating..."):
                    st.session_state["result"] = translate_text(text, source, target)
                    st.session_state["target"] = target
            except Exception as err:
                st.error(f"Translation failed: {err}")

    result = st.session_state.get("result")
    if result:
        st.subheader("Translation")
        st.success(result)
        # st.code gives a built-in copy-to-clipboard button
        st.caption("Copy to clipboard:")
        st.code(result, language=None)

        if HAS_TTS and st.button("🔊 Listen"):
            try:
                audio = text_to_speech(result, LANGUAGES[st.session_state["target"]])
                st.audio(audio, format="audio/mp3")
            except Exception as err:
                st.error(f"Text-to-speech failed: {err}")


if __name__ == "__main__":
    main()
