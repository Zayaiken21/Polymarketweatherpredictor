from storage.db import get_conn

def save_poly_account(user_id: str, api_key: str, api_secret: str, user_address: str | None = None):
    with get_conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO poly_accounts(user_id, api_key, api_secret, user_address, updated_at) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
            (user_id, api_key, api_secret, user_address),
        )
        conn.commit()

def load_poly_account(user_id: str):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT api_key, api_secret, user_address FROM poly_accounts WHERE user_id=?",
            (user_id,),
        ).fetchone()
    return dict(row) if row else None