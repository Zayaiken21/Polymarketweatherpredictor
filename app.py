import logging
import streamlit as st
from pathlib import Path

from storage.db import init_db
from auth.session_manager import init_session
from storage.settings_store import load_settings, clear_session_data
from ui.shell import apply_style, render_header
from ui.login import login_box
from ui.navigation import render_menu
from ui.dashboard import render_home, render_chat_and_voice, render_stats
from ui.poly_api import render_poly_api
from ui.settings import render_settings
from ui.admin import render_admin
from core.module_loader import auto_discover

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

APP_ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="Agent Cyclone - Poly Market Bot", layout="wide")
logger.info("App starting")
init_db()
init_session()
auto_discover(APP_ROOT)
logger.info("Auto-discovery complete")
apply_style()
render_header()

if not st.session_state.logged_in:
    login_box()
else:
    saved = load_settings(st.session_state.user_id)

    if not st.session_state.get("language"):
        st.session_state.language = saved.get("language", "en")

    if not st.session_state.get("display_name"):
        st.session_state.display_name = saved.get("display_name") or st.session_state.role

    with st.sidebar:
        page = render_menu()
        st.divider()
        st.write(f"Signed in as: **{st.session_state.display_name}**")
        st.write(f"Language: **{st.session_state.language}**")
        st.divider()

        if st.button("Logout", use_container_width=True, key="logout_btn"):
            uid = st.session_state.user_id
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.user_id = None
            st.session_state.display_name = ""
            st.session_state.messages = []
            st.session_state.voice_on = True
            st.session_state.generated_tokens = []
            st.session_state.audio_input_key_counter = 0
            st.session_state.pop("poly_api_key", None)
            st.session_state.pop("poly_api_secret", None)
            st.session_state.pop("poly_balance_result", None)
            st.session_state.pop("poly_ping_result", None)
            if uid:
                clear_session_data(uid)
            st.rerun()

    if page == "Home":
        render_home()
    elif page == "Chat":
        render_chat_and_voice()
    elif page == "Trade History":
        render_stats()
    elif page == "Poly Api":
        render_poly_api()
    elif page == "Settings":
        render_settings()
        if st.session_state.role == "CEO":
            st.divider()
            render_admin()