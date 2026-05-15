import math
import streamlit as st
from auth.client_tokens import generate_tokens
from storage.tokens_store import save_token, list_tokens, revoke_token, revoke_all_tokens, update_token_owner

PAGE_SIZE = 5

def render_admin():
    st.subheader("Token Manager")

    if "token_page" not in st.session_state:
        st.session_state.token_page = 1

    owner_name = st.text_input("Client name", key="token_owner_name", placeholder="Client name")

    if st.button("Generate token", use_container_width=True, key="gen_token_btn"):
        token = generate_tokens(1)[0]
        save_token(token, "client", owner_name or None)
        st.rerun()

    st.divider()
    st.write("Active tokens")

    tokens = list_tokens()
    total_pages = max(1, math.ceil(len(tokens) / PAGE_SIZE))
    st.session_state.token_page = min(max(1, st.session_state.token_page), total_pages)
    page_tokens = tokens[(st.session_state.token_page - 1) * PAGE_SIZE : st.session_state.token_page * PAGE_SIZE]

    for i, item in enumerate(page_tokens):
        cols = st.columns([6, 4, 1])
        cols[0].write(item["token"])
        new_name = cols[1].text_input(
            "Client name",
            value=item.get("owner_name") or "",
            key=f"owner_{st.session_state.token_page}_{i}_{item['token']}",
            label_visibility="collapsed",
        )
        if new_name != (item.get("owner_name") or ""):
            update_token_owner(item["token"], new_name or None)
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