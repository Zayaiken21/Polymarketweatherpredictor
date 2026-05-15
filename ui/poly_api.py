import streamlit as st

def render_poly_api():
    st.header("Poly Api")

    api_key = st.text_input(
        "API Key",
        value=st.session_state.get("poly_api_key", ""),
        type="password",
        key="poly_api_key_input",
    )

    api_secret = st.text_input(
        "API Secret",
        value=st.session_state.get("poly_api_secret", ""),
        type="password",
        key="poly_api_secret_input",
    )

    if st.button("Check Balance", use_container_width=True):
        st.session_state.poly_api_key = api_key.strip()
        st.session_state.poly_api_secret = api_secret.strip()

        if not api_key.strip() or not api_secret.strip():
            st.error("API key and secret are required.")
            return

        try:
            from services.polymarket_service import get_balance_snapshot, ping_polymarket
            st.session_state.poly_ping_result = ping_polymarket()
            st.session_state.poly_balance_result = get_balance_snapshot(
                api_key=api_key.strip(),
                api_secret=api_secret.strip(),
            )
        except Exception as e:
            st.session_state.poly_balance_result = {"status": "error", "error": str(e)}

    result = st.session_state.get("poly_balance_result")
    if result:
        st.subheader("Balance")
        if result.get("status") == "ok":
            st.write(_format_usd_balance(result.get("balance")))
        else:
            st.error("Unable to read balance.")

    with st.expander("Debug", expanded=False):
        st.write("Saved API key:", bool(st.session_state.get("poly_api_key")))
        st.write("Saved API secret:", bool(st.session_state.get("poly_api_secret")))
        st.write("Ping:", st.session_state.get("poly_ping_result", {}))
        st.write("Balance raw:", st.session_state.get("poly_balance_result", {}))

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
    return str(balance)