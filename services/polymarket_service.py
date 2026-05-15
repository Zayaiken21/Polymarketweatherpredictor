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
DATA_API = "https://data-api.polymarket.com"
BRIDGE_API = "https://bridge.polymarket.com"

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

def _auth_headers(api_key: str, api_secret: str, method: str, path: str):
    ts = str(int(time.time() * 1000))
    msg = f"{ts}{method.upper()}{path}"
    sig = hmac.new(api_secret.encode(), msg.encode(), hashlib.sha256).digest()
    return {
        "X-PM-Access-Key": api_key,
        "X-PM-Timestamp": ts,
        "X-PM-Signature": base64.b64encode(sig).decode(),
        "Content-Type": "application/json",
    }

def _ok_credentials(api_key, api_secret):
    return bool(api_key and api_secret)

def ping_polymarket(timeout=5):
    checks = [
        f"{CLOB_API}/health",
        f"{CLOB_API}/api/health",
        f"{CLOB_API}/v1/health",
    ]
    for url in checks:
        try:
            r = _session().get(url, timeout=timeout)
            logger.info("Polymarket ping url=%s status=%s", url, r.status_code)
            if r.ok:
                return {"ok": True, "url": url, "status_code": r.status_code, "text": r.text[:200]}
        except Exception as e:
            logger.exception("Polymarket ping failed url=%s", url)
    return {"ok": False, "status_code": 404, "text": "No health endpoint returned 200"}

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

def get_portfolio_balance(api_key=None, api_secret=None, timeout=8):
    if not _ok_credentials(api_key, api_secret):
        logger.warning("Balance requested without credentials")
        return {"status": "not_connected", "balance": None, "raw": None}

    attempts = [
        ("GET", "/v1/portfolio/balance"),
        ("GET", "/v1/balance"),
        ("POST", "/v1/portfolio/positions/balance"),
    ]

    last = None
    for method, path in attempts:
        try:
            headers = _auth_headers(api_key, api_secret, method, path)
            url = f"{CLOB_API}{path}"
            logger.info("Requesting balance method=%s path=%s", method, path)

            if method == "GET":
                r = _session().get(url, headers=headers, timeout=timeout)
            else:
                r = _session().post(url, headers=headers, json={}, timeout=timeout)

            last = r
            logger.info("Balance response status=%s path=%s", r.status_code, path)

            if r.status_code in (401, 403):
                return {"status": "unauthorized", "balance": None, "raw": r.text}
            if r.status_code == 404:
                continue

            r.raise_for_status()
            data = r.json()
            balance = _extract_usd(data)
            return {"status": "ok", "balance": balance, "raw": data}
        except Exception:
            logger.exception("Balance attempt failed path=%s", path)
            continue

    return {"status": "endpoint_not_found", "balance": None, "raw": getattr(last, "text", None)}

def get_balance_snapshot(api_key=None, api_secret=None, timeout=8):
    logger.info("Snapshot requested has_api=%s has_secret=%s", bool(api_key), bool(api_secret))
    balance_result = get_portfolio_balance(api_key, api_secret, timeout=timeout)
    return {
        "status": balance_result.get("status"),
        "balance": balance_result.get("balance"),
        "raw": balance_result.get("raw"),
    }