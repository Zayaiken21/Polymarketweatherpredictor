import os
import streamlit as st
from dotenv import load_dotenv
from auth.admin_auth import verify_ceo_password
from storage.settings_store import save_display_name

load_dotenv()

def _get_ceo_password():
    try:
        if "CEO_PASSWORD" in st.secrets:
            return st.secrets["CEO_PASSWORD"]
    except Exception:
        pass
    return os.getenv("CEO_PASSWORD", "ceo1")