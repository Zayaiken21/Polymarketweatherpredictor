import streamlit as st
from storage.tokens_store import list_tokens

def apply_style():
    st.markdown(
        """
        <style>
        :root {
            --bg: #f8fbff;
            --panel: #ffffff;
            --panel-soft: #f1f7ff;
            --panel-soft-2: #eaf3ff;
            --text: #1f2937;
            --muted: #627084;
            --accent: #75aee6;
            --accent-2: #dbeafe;
            --border: rgba(31, 41, 55, 0.08);
        }
        html, body, [class*="css"] {
            background: linear-gradient(180deg, #fbfdff 0%, #f6faff 100%) !important;
            color: var(--text) !important;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: visible;}
        .block-container {
            padding-top: 1.35rem !important;
            padding-bottom: 1.5rem !important;
            max-width: 100% !important;
        }
        .card, .login-card, .home-card {
            background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 18px 20px;
            box-shadow: 0 10px 28px rgba(85, 125, 165, 0.09);
            color: var(--text);
            width: 100%;
        }
        .login-title, .top-title, .page-title {
            text-align: center;
            font-weight: 800;
            line-height: 1.1;
            color: var(--text);
            word-break: break-word;
            margin: 0;
        }
        .login-title {font-size: clamp(1.35rem, 2vw, 1.85rem);}
        .top-title, .page-title {font-size: clamp(1.25rem, 2.1vw, 1.9rem);}
        .subtle {
            color: var(--muted);
            text-align: center;
            font-size: clamp(0.92rem, 1.1vw, 1rem);
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffffff 0%, #f4f8ff 100%);
            border-right: 1px solid var(--border);
        }
        [data-testid="stSidebar"] * {
            color: var(--text) !important;
        }
        .stRadio > div {
            gap: 0.25rem;
        }
        h1, h2, h3, h4, h5, h6, p, label, span, div {
            overflow-wrap: anywhere;
        }
        .stButton > button {
            background: linear-gradient(180deg, #7ab3ea 0%, #69a4e0 100%);
            color: #fff;
            border: none;
            border-radius: 12px;
        }
        .stButton > button:hover {
            filter: brightness(0.99);
        }
        .stTextInput input, .stSelectbox div[data-baseweb="select"], .stChatInput textarea {
            background: #fff !important;
            color: var(--text) !important;
        }
        .status-pill {
            display: inline-block;
            padding: 0.35rem 0.7rem;
            border-radius: 999px;
            background: var(--accent-2);
            color: var(--text);
            font-size: 0.9rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_header():
    st.markdown(
        """
        <div class="card" style="margin-top:0.15rem;">
            <div class="top-title">Agent Cyclone - Poly Market Bot</div>
            <div class="subtle">Dropz Universal, Inc</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar_summary():
    if not st.session_state.get("logged_in"):
        return
    with st.sidebar:
        st.write(f"Signed in as: **{st.session_state.get('display_name') or st.session_state.get('role', 'Guest')}**")
        st.write(f"Language: **{st.session_state.get('language', 'en')}**")
        st.divider()
        if st.session_state.get("poly_status_ts"):
            import time
            if time.time() - st.session_state.poly_status_ts < 4:
                st.info("Connected account loaded.")
            else:
                st.session_state.pop("poly_status_ts", None)

def show_active_tokens_preview():
    tokens = list_tokens()
    if not tokens:
        return
    st.sidebar.markdown("**Active tokens**")
    for item in tokens[:5]:
        st.sidebar.write(item["owner_name"] or item["token"])