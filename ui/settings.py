import streamlit as st
from storage.settings_store import save_settings
from ui.dashboard import clear_conversation

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

    if st.button("Clear Conversation", use_container_width=True):
        clear_conversation()
        st.session_state.clear_chat_notice = "Conversation cleared."
        st.rerun()

    if st.session_state.get("clear_chat_notice"):
        st.success(st.session_state.clear_chat_notice)
        st.session_state.clear_chat_notice = None