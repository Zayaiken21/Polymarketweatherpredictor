import sqlite3
from pathlib import Path

DB_PATH = Path("output/db/app.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def _ensure_column(conn, table, column, coltype):
    cols = [r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    if column not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {coltype}")

def init_db():
    with get_conn() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            role TEXT,
            display_name TEXT,
            language TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            ts TEXT DEFAULT CURRENT_TIMESTAMP,
            market TEXT,
            side TEXT,
            amount REAL,
            result TEXT,
            pnl REAL
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS tokens (
            token TEXT PRIMARY KEY,
            role TEXT,
            owner_name TEXT,
            active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS poly_accounts (
            user_id TEXT PRIMARY KEY,
            api_key TEXT,
            api_secret TEXT,
            user_address TEXT,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")
        _ensure_column(conn, "users", "display_name", "TEXT")
        _ensure_column(conn, "tokens", "owner_name", "TEXT")
        _ensure_column(conn, "poly_accounts", "user_address", "TEXT")
        conn.commit()