import streamlit as st

def init_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "audio_input_key_counter" not in st.session_state:
        st.session_state.audio_input_key_counter = 0
    if "voice_on" not in st.session_state:
        st.session_state.voice_on = True

def add_message(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})

def clear_chat():
    st.session_state.messages = []