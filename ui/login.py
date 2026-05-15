import streamlit as st
from auth.admin_auth import verify_ceo_password
from storage.settings_store import save_display_name, load_settings
from storage.tokens_store import get_token_owner

def login_box():
    st.title("Sign in")

    with st.form("login_form", clear_on_submit=False):
        role = st.selectbox("Role", ["CEO", "User"], key="login_role")
        credential = st.text_input("Password or token", type="password", key="login_credential")
        submitted = st.form_submit_button("Login")

    if submitted:
        if role == "CEO":
            if verify_ceo_password(credential):
                st.session_state.logged_in = True
                st.session_state.role = "CEO"
                st.session_state.user_id = "ceo"
                st.session_state.client_name = "CEO"
                st.session_state.display_name = "CEO"
                save_display_name("ceo", "CEO")
                st.rerun()
            else:
                st.error("Invalid CEO password.")
        else:
            token = credential.strip()
            if token:
                owner_name = get_token_owner(token)
                saved = load_settings(token)
                resolved = owner_name or saved.get("display_name") or "Client"

                st.session_state.logged_in = True
                st.session_state.role = "User"
                st.session_state.user_id = token
                st.session_state.token = token
                st.session_state.client_name = resolved
                st.session_state.display_name = resolved
                save_display_name(token, resolved)
                st.rerun()
            else:
                st.error("Enter a token or password.")