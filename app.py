import streamlit as st
from streamlit_mic_recorder import mic_recorder

from audio.stt import speech_to_text
from audio.tts import text_to_speech
from utils.language import normalize_language

from rag.rag_engine import rag_answer



st.set_page_config(
    page_title="Creation Hospital AI Concierge",
    layout="centered",
)

st.title("🏥 Creation Hospital AI Concierge")
st.caption("Speak or type in English, Hindi, or Spanish")

# Chat memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Render chat history
for role, message in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").write(message)
    else:
        st.chat_message("assistant").write(message)

# Text input chatbot
user_text = st.chat_input("Type your question here...")

if user_text:
    st.session_state.chat_history.append(("user", user_text))

    with st.spinner("Searching hospital information..."):
        bot_response = rag_answer(user_text)

    st.session_state.chat_history.append(("assistant", bot_response))
    st.rerun()


# Voice input
audio = mic_recorder(
    start_prompt="🎙️ Speak",
    stop_prompt="⏹️ Stop",
    key="recorder",
)

if audio:
    with st.spinner("Listening..."):
        transcript, detected_language = speech_to_text(audio["bytes"])

    if transcript:
        st.session_state.chat_history.append(("user", transcript))

        with st.spinner("Searching hospital information..."):
            bot_response = rag_answer(transcript)

        st.session_state.chat_history.append(("assistant", bot_response))

        tts_language = normalize_language(detected_language)
        audio_mp3 = text_to_speech(bot_response, tts_language)

        st.audio(audio_mp3, format="audio/mp3")
        st.rerun()
