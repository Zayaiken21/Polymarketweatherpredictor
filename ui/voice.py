import streamlit as st
from core.voice_pipeline import process_voice_bytes
from core.chat_state import init_chat, add_message

def render_voice_mic():
    init_chat()
    st.subheader("Mic")
    audio = st.audio_input("Mic")
    if audio:
        data = audio.read()
        heard, reply = process_voice_bytes(data, history=st.session_state.messages, language=st.session_state.language)
        add_message("user", heard)
        add_message("assistant", reply)
        st.write("Heard:", heard)
        st.write("Reply:", reply)