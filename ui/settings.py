import streamlit as st
from storage.settings_store import save_settings

def render_settings():
    st.header("Settings")

    current_lang = st.session_state.get("language", "en")
    current_voice = st.session_state.get("voice_on", True)

    new_lang = st.selectbox("Language", ["en", "es"], index=0 if current_lang == "en" else 1)
    new_voice = st.toggle("Voice enabled" if current_voice else "Voice disabled", value=current_voice)

    st.session_state.language = new_lang
    st.session_state.voice_on = new_voice

    if st.button("Save Settings", use_container_width=True):
        save_settings(
            st.session_state.user_id,
            {
                "language": new_lang,
                "voice_on": new_voice,
                "display_name": st.session_state.get("display_name", ""),
            },
        )
        st.success("Settings saved.")