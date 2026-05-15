import json
from pathlib import Path

TOKENS_FILE = Path("data/tokens.json")

def _load_all():
    if not TOKENS_FILE.exists():
        return []
    try:
        data = json.loads(TOKENS_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []

def _save_all(tokens):
    TOKENS_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKENS_FILE.write_text(json.dumps(tokens, indent=2), encoding="utf-8")

def save_token(token, token_type="client", owner_name=None):
    tokens = _load_all()
    tokens.append({
        "token": token,
        "type": token_type,
        "owner_name": owner_name or None,
    })
    _save_all(tokens)

def list_tokens():
    return _load_all()

def revoke_token(token):
    tokens = [t for t in _load_all() if t.get("token") != token]
    _save_all(tokens)

def revoke_all_tokens():
    _save_all([])

def update_token_owner(token, owner_name):
    tokens = _load_all()
    for item in tokens:
        if item.get("token") == token:
            item["owner_name"] = owner_name or None
            break
    _save_all(tokens)

def get_token_owner(token):
    for item in _load_all():
        if item.get("token") == token:
            return item.get("owner_name")
    return None