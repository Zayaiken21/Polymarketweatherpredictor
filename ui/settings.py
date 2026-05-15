import streamlit as st

def render_settings():
    st.header("Settings")
    st.session_state.language = st.selectbox(
        "Language",
        ["en", "es"],
        index=0 if st.session_state.get("language", "en") == "en" else 1,
    )
    st.session_state.voice_on = st.checkbox("Voice enabled", value=st.session_state.get("voice_on", True))