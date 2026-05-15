import base64
import hashlib
import hmac
import logging
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger("poly_service")
CLOB_API = "https://clob.polymarket.com"

def _session():
    s = requests.Session()
    retry = Retry(
        total=2,
        connect=2,
        read=2,
        backoff_factor=0.25,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST", "DELETE", "PUT"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s

def _auth_headers(api_key: str, api_secret: str, api_passphrase: str, method: str, path: str):
    ts = str(int(time.time()))
    msg = f"{ts}{method.upper()}{path}"
    sig = hmac.new(api_secret.encode(), msg.encode(), hashlib.sha256).digest()
    return {
        "POLY_API_KEY": api_key,
        "POLY_PASSPHRASE": api_passphrase,
        "POLY_SIGNATURE": base64.b64encode(sig).decode(),
        "POLY_TIMESTAMP": ts,
        "Content-Type": "application/json",
    }

def _ok_credentials(api_key, api_secret, api_passphrase):
    return bool(api_key and api_secret and api_passphrase)

def ping_polymarket(timeout=5):
    urls = [
        f"{CLOB_API}/auth/api-key",
        f"{CLOB_API}/api-key",
        f"{CLOB_API}/",
    ]
    for url in urls:
        try:
            r = _session().get(url, timeout=timeout)
            logger.info("Polymarket ping url=%s status=%s", url, r.status_code)
            if r.status_code < 500:
                return {"ok": True, "url": url, "status_code": r.status_code, "text": r.text[:200]}
        except Exception:
            logger.exception("Polymarket ping failed url=%s", url)
    return {"ok": False, "status_code": 404, "text": "No usable endpoint returned a non-5xx response"}

def get_balance_snapshot(api_key=None, api_secret=None, api_passphrase=None, timeout=8):
    logger.info(
        "Snapshot requested has_api=%s has_secret=%s has_passphrase=%s",
        bool(api_key),
        bool(api_secret),
        bool(api_passphrase),
    )
    if not _ok_credentials(api_key, api_secret, api_passphrase):
        return {"status": "not_connected", "balance": None, "raw": None}

    attempts = [
        ("GET", "/auth/api-key"),
        ("GET", "/auth/derive-api-key"),
        ("GET", "/balances"),
        ("GET", "/balance"),
        ("GET", "/me"),
    ]

    last = None
    for method, path in attempts:
        try:
            headers = _auth_headers(api_key, api_secret, api_passphrase, method, path)
            url = f"{CLOB_API}{path}"
            logger.info("Requesting balance method=%s path=%s", method, path)

            r = _session().request(method, url, headers=headers, timeout=timeout)
            last = r
            logger.info("Balance response status=%s path=%s", r.status_code, path)

            if r.status_code in (401, 403):
                return {"status": "unauthorized", "balance": None, "raw": r.text}
            if r.status_code == 404:
                continue

            r.raise_for_status()
            data = r.json() if "application/json" in r.headers.get("content-type", "") else {"raw": r.text}
            balance = _extract_usd(data)
            return {"status": "ok", "balance": balance, "raw": data}
        except Exception:
            logger.exception("Balance attempt failed path=%s", path)
            continue

    return {"status": "endpoint_not_found", "balance": None, "raw": getattr(last, "text", None)}

def _extract_usd(payload):
    if payload is None:
        return None
    if isinstance(payload, (int, float)):
        return float(payload)
    if isinstance(payload, str):
        try:
            return float(payload)
        except Exception:
            return None
    if isinstance(payload, list):
        for item in payload:
            v = _extract_usd(item)
            if v is not None:
                return v
        return None
    if isinstance(payload, dict):
        for key in ("balance", "usd", "usdBalance", "available", "availableBalance", "cash", "value", "buyingPower"):
            if key in payload:
                v = _extract_usd(payload.get(key))
                if v is not None:
                    return v
        for key in ("data", "result", "account", "portfolio", "balances"):
            if key in payload:
                v = _extract_usd(payload.get(key))
                if v is not None:
                    return v
    return None