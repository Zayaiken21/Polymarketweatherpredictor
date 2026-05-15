import streamlit as st
from i18n.translations import tr

def render_menu():
    lang = st.session_state.get("language", "en")

    pages = [
        ("Home", tr("home", lang)),
        ("Chat", tr("chat", lang)),
        ("Trade History", tr("trades", lang)),
        ("Poly Api", tr("poly_api", lang)),
        ("Settings", tr("settings", lang)),
    ]

    option_keys = [p[0] for p in pages]
    labels = {p[0]: p[1] for p in pages}

    return st.radio(
        "Navigation",
        option_keys,
        format_func=lambda key: labels.get(key, key),
        key="sidebar_page",
        label_visibility="collapsed",
    )