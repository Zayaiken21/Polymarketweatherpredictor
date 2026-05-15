import streamlit as st
from storage.settings_store import save_credentials

def render_poly_api():
    st.header("Poly Api")

    api_key = st.text_input("API Key", value=st.session_state.get("poly_api_key", ""), type="password", key="poly_api_key_input")
    api_secret = st.text_input("API Secret", value=st.session_state.get("poly_api_secret", ""), type="password", key="poly_api_secret_input")

    if st.button("Check Balance", use_container_width=True):
        st.session_state.poly_api_key = api_key.strip()
        st.session_state.poly_api_secret = api_secret.strip()

        if not api_key.strip() or not api_secret.strip():
            st.error("API key and secret are required.")
            return

        if st.session_state.get("user_id"):
            save_credentials(
                st.session_state.user_id,
                api_key=api_key.strip(),
                api_secret=api_secret.strip(),
            )

        try:
            from services.polymarket_service import get_balance_snapshot
            st.session_state.poly_balance_result = get_balance_snapshot(
                api_key=api_key.strip(),
                api_secret=api_secret.strip(),
            )
        except Exception as e:
            st.session_state.poly_balance_result = {"status": "error", "error": str(e)}

    result = st.session_state.get("poly_balance_result")
    if result:
        st.subheader("Balance")
        if result.get("status") == "ok" and result.get("balance") is not None:
            st.write(_format_usd_balance(result.get("balance")))
        else:
            st.error("Unable to read balance.")

def _format_usd_balance(balance):
    if balance is None:
        return "USD balance unavailable"
    if isinstance(balance, (int, float)):
        return f"${balance:,.2f}"
    if isinstance(balance, str):
        try:
            return f"${float(balance):,.2f}"
        except Exception:
            return balance
    if isinstance(balance, dict):
        for key in ("balance", "usd", "usdBalance", "available", "availableBalance", "cash", "value", "buyingPower"):
            val = balance.get(key)
            if isinstance(val, (int, float)):
                return f"${val:,.2f}"
            if isinstance(val, str):
                try:
                    return f"${float(val):,.2f}"
                except Exception:
                    pass
        return str(balance)
    return str(balance)