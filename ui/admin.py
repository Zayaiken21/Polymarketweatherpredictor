import math
import streamlit as st
from auth.client_tokens import generate_tokens
from storage.tokens_store import save_token, list_tokens, revoke_token, revoke_all_tokens, update_token_owner

PAGE_SIZE = 5

def render_admin():
    st.subheader("Token Manager")

    if "token_page" not in st.session_state:
        st.session_state.token_page = 1

    with st.form("token_generate_form", clear_on_submit=True):
        owner_name = st.text_input("Client name", key="token_owner_name", placeholder="Client name")
        submitted = st.form_submit_button("Generate token", use_container_width=True)

    if submitted:
        token = generate_tokens(1)[0]
        save_token(token, "client", owner_name.strip() or None)
        st.rerun()

    st.divider()
    st.write("Active tokens")

    tokens = list_tokens()
    total_pages = max(1, math.ceil(len(tokens) / PAGE_SIZE))
    st.session_state.token_page = min(max(1, st.session_state.token_page), total_pages)
    page_tokens = tokens[(st.session_state.token_page - 1) * PAGE_SIZE : st.session_state.token_page * PAGE_SIZE]

    for i, item in enumerate(page_tokens):
        cols = st.columns([6, 4, 1])
        cols[0].write(item.get("owner_name") or item["token"])

        edit_key = f"owner_{st.session_state.token_page}_{i}_{item['token']}"
        current_name = item.get("owner_name") or ""

        edited_name = cols[1].text_input(
            "Client name",
            value=current_name,
            key=edit_key,
            label_visibility="collapsed",
        )

        if edited_name != current_name:
            update_token_owner(item["token"], edited_name.strip() or None)
            st.rerun()

        if cols[2].button("✕", key=f"revoke_{st.session_state.token_page}_{i}_{item['token']}"):
            revoke_token(item["token"])
            st.rerun()

    a, b, c = st.columns([1, 2, 1])
    with a:
        if st.button("Prev", disabled=st.session_state.token_page <= 1, key="tokens_prev_btn"):
            st.session_state.token_page -= 1
            st.rerun()
    with b:
        st.markdown(f"<div style='text-align:center;'>Page {st.session_state.token_page} / {total_pages}</div>", unsafe_allow_html=True)
    with c:
        if st.button("Next", disabled=st.session_state.token_page >= total_pages, key="tokens_next_btn"):
            st.session_state.token_page += 1
            st.rerun()

    if st.button("Cancel all", use_container_width=True, key="cancel_all_tokens_btn"):
        revoke_all_tokens()
        st.rerun()