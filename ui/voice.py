import streamlit as st
from core.voice_pipeline import process_voice_bytes
from core.chat_state import init_chat, add_message

def render_voice_mic():
    init_chat()
    st.subheader("Mic")
    audio = st.audio_input("Mic", sample_rate=16000)

    if audio is not None:
        data = audio.read()
        heard, reply, spoken = process_voice_bytes(
            data,
            history=st.session_state.messages,
            language=st.session_state.language,
            voice_on=True,
        )

        add_message("user", heard)
        add_message("assistant", reply)

        st.write("Heard:", heard)
        st.write("Reply:", reply)

        audio_bytes = spoken.get("audio_bytes") if isinstance(spoken, dict) else None
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")