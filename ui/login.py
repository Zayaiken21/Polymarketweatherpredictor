import os
import streamlit as st
from auth.admin_auth import verify_ceo_password
from storage.settings_store import save_display_name

def _get_ceo_password():
    try:
        if "CEO_PASSWORD" in st.secrets:
            return st.secrets["CEO_PASSWORD"]
    except Exception:
        pass
    return os.getenv("CEO_PASSWORD", "ceo1")

def login_box():
    st.title("Sign in")

    role = st.selectbox("Role", ["CEO", "User"], key="login_role")
    credential = st.text_input("Password or token", type="password", key="login_credential")

    if st.button("Login", use_container_width=True, key="login_button"):
        if role == "CEO":
            expected = _get_ceo_password()
            if verify_ceo_password(credential, expected):
                st.session_state.logged_in = True
                st.session_state.role = "CEO"
                st.session_state.user_id = "ceo"
                st.session_state.display_name = "CEO"
                save_display_name("ceo", "CEO")
                st.rerun()
            else:
                st.error("Invalid CEO password.")
        else:
            if credential.strip():
                st.session_state.logged_in = True
                st.session_state.role = "User"
                st.session_state.user_id = credential.strip()
                st.session_state.display_name = credential.strip()
                save_display_name(st.session_state.user_id, st.session_state.display_name)
                st.rerun()
            else:
                st.error("Enter a token or password.")