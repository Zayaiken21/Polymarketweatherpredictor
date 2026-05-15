import json
from pathlib import Path

TOKENS_FILE = Path("data/tokens.json")

def _load():
    if not TOKENS_FILE.exists():
        return []
    try:
        return json.loads(TOKENS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []

def _save(items):
    TOKENS_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKENS_FILE.write_text(json.dumps(items, indent=2), encoding="utf-8")

def list_tokens():
    return _load()

def save_token(token, token_type="client", owner_name=None):
    items = _load()
    for item in items:
        if item.get("token") == token:
            item["token_type"] = token_type
            item["owner_name"] = owner_name or ""
            _save(items)
            return
    items.append({"token": token, "token_type": token_type, "owner_name": owner_name or ""})
    _save(items)

def update_token_owner(token, owner_name):
    items = _load()
    for item in items:
        if item.get("token") == token:
            item["owner_name"] = owner_name or ""
            break
    _save(items)

def revoke_token(token):
    items = [x for x in _load() if x.get("token") != token]
    _save(items)

def revoke_all_tokens():
    _save([])