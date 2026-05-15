import streamlit as st

def init_session():
    defaults = {
        "logged_in": False,
        "role": None,
        "user_id": None,
        "display_name": "",
        "client_name": "",
        "language": "en",
        "voice_on": True,
        "messages": [],
        "generated_tokens": [],
        "audio_input_key_counter": 0,
        "poly_api_key": "",
        "poly_api_secret": "",
        "poly_balance_result": None,
        "poly_ping_result": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v