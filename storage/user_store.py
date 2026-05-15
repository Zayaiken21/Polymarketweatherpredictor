from storage.db import get_conn

def load_user_profile(user_id: str):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
    return dict(row) if row else None

def save_user_profile(user_id: str, profile: dict):
    with get_conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO users(user_id, role, language) VALUES (?, ?, ?)",
            (user_id, profile.get("role"), profile.get("language", "en")),
        )
        conn.commit()