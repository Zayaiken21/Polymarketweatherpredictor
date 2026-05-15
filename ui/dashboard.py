import streamlit as st
from core.chat_state import init_chat, add_message
from services.llm_service import respond_with_voice
from core.voice_pipeline import process_voice_bytes

def clear_conversation():
    st.session_state.messages = []

def render_home():
    st.markdown(
        "<div class='card home-card'><h2 class='page-title'>Welcome</h2><p class='subtle'>Use the sidebar to move between chat, trading tools, and settings.</p></div>",
        unsafe_allow_html=True,
    )

def render_chat_and_voice():
    init_chat()

    for msg in st.session_state.messages[-40:]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_text = st.chat_input("Ask a question or command")
    if user_text:
        add_message("user", user_text)
        reply = respond_with_voice(
            user_text,
            history=st.session_state.messages[-10:],
            language=st.session_state.get("language", "en"),
            voice_on=st.session_state.get("voice_on", True),
        )
        add_message("assistant", reply)
        st.rerun()

    if "audio_input_key_counter" not in st.session_state:
        st.session_state.audio_input_key_counter = 0

    if st.session_state.get("voice_on", True):
        audio_key = f"audio_input_{st.session_state.audio_input_key_counter}"
        audio = st.audio_input(
            "Mic",
            sample_rate=16000,
            key=audio_key,
        )

        if audio:
            heard, reply, spoken = process_voice_bytes(
                audio.read(),
                history=st.session_state.messages[-10:],
                language=st.session_state.get("language", "en"),
                voice_on=st.session_state.get("voice_on", True),
            )
            add_message("user", heard)
            add_message("assistant", reply)

            st.write("Heard:", heard)
            st.write("Reply:", reply)

            if spoken:
                st.audio(spoken, format="audio/mp3")
            else:
                st.info("Voice playback is unavailable on this device right now, so the reply is shown in text.")

            st.session_state.audio_input_key_counter += 1
            st.rerun()

def render_stats():
    from storage.trades_store import get_recent_trades
    uid = st.session_state.get("user_id", "guest")
    trades = get_recent_trades(uid, 25)

    st.subheader("Trade History")
    if trades:
        st.dataframe(trades, use_container_width=True)
    else:
        st.info("No trades recorded yet.")