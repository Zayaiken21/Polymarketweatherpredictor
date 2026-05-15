from storage.db import get_conn

def save_token(token: str, role: str = "client", owner_name: str | None = None):
    with get_conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO tokens(token, role, owner_name, active) VALUES (?, ?, ?, 1)",
            (token, role, owner_name),
        )
        conn.commit()

def update_token_owner(token: str, owner_name: str | None):
    with get_conn() as conn:
        conn.execute("UPDATE tokens SET owner_name=? WHERE token=?", (owner_name, token))
        conn.commit()

def revoke_token(token: str):
    with get_conn() as conn:
        conn.execute("UPDATE tokens SET active=0 WHERE token=?", (token,))
        conn.commit()

def revoke_all_tokens():
    with get_conn() as conn:
        conn.execute("UPDATE tokens SET active=0")
        conn.commit()

def list_tokens():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM tokens WHERE active=1 ORDER BY created_at DESC").fetchall()
    return [dict(r) for r in rows]