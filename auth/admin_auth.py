import os
import hmac
import streamlit as st

def get_ceo_password():
    try:
        if "CEO_PASSWORD" in st.secrets:
            return st.secrets["CEO_PASSWORD"]
    except Exception:
        pass
    return os.getenv("CEO_PASSWORD", "")

def verify_ceo_password(entered: str):
    expected = get_ceo_password()
    return hmac.compare_digest((entered or "").strip(), (expected or "").strip())