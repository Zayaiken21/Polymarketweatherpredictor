from storage.db import get_conn

def add_trade(user_id, market, side, amount, result, pnl):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO trades(user_id, market, side, amount, result, pnl) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, market, side, amount, result, pnl),
        )
        conn.commit()

def get_recent_trades(user_id, limit=25):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM trades WHERE user_id=? ORDER BY id DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
    return [dict(r) for r in rows]