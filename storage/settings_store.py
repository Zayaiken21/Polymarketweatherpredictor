import json
from pathlib import Path

SETTINGS_DIR = Path("data")
SETTINGS_FILE = SETTINGS_DIR / "settings.json"

def _load_all():
    if not SETTINGS_FILE.exists():
        return {}
    try:
        return json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}

def _save_all(data):
    SETTINGS_DIR.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

def load_settings(user_id):
    data = _load_all()
    return data.get(str(user_id), {})

def save_settings(user_id, settings):
    data = _load_all()
    current = data.get(str(user_id), {})
    current.update(settings or {})
    data[str(user_id)] = current
    _save_all(data)

def save_display_name(user_id, display_name):
    save_settings(user_id, {"display_name": display_name})

def save_credentials(user_id, api_key=None, api_secret=None, user_address=None):
    payload = {}
    if api_key is not None:
        payload["poly_api_key"] = api_key
    if api_secret is not None:
        payload["poly_api_secret"] = api_secret
    if user_address is not None:
        payload["poly_wallet_address"] = user_address
    save_settings(user_id, payload)

def clear_session_data(user_id):
    data = _load_all()
    uid = str(user_id)
    if uid in data:
        for key in ("poly_api_key", "poly_api_secret", "poly_wallet_address"):
            data[uid].pop(key, None)
        _save_all(data)

def delete_user_data(user_id):
    data = _load_all()
    data.pop(str(user_id), None)
    _save_all(data)