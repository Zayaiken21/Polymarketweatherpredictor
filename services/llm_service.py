import os
import logging
from functools import lru_cache
from urllib.parse import urlparse
from dotenv import load_dotenv
import requests

load_dotenv()

logger = logging.getLogger("llm_service")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
LLM_PROVIDER = "ollama"

def _normalize_host(host):
    host = (host or "").strip()
    if not host:
        return "http://127.0.0.1:11434"
    if not host.startswith(("http://", "https://")):
        host = "http://" + host
    parsed = urlparse(host)
    if not parsed.netloc:
        return "http://127.0.0.1:11434"
    return host.rstrip("/")

@lru_cache(maxsize=1)
def _ollama_base():
    return _normalize_host(OLLAMA_HOST)

@lru_cache(maxsize=1)
def _ollama_ready():
    try:
        r = requests.get(f"{_ollama_base()}/api/tags", timeout=3)
        return r.ok
    except Exception:
        logger.exception("Ollama ping failed")
        return False

def _build_messages(prompt: str, history=None, language="en"):
    history = history or []
    messages = [
        {
            "role": "system",
            "content": (
                "You are Agent Cyclone. Reply in the user's language. "
                "Be accurate, concise, and helpful."
            ),
        }
    ]
    for msg in history[-12:]:
        role = msg.get("role", "user")
        if role not in ("user", "assistant", "system"):
            role = "user"
        content = str(msg.get("content", "")).strip()
        if content:
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": prompt})
    return messages

def _ask_ollama(prompt: str, history=None, language="en"):
    payload = {
        "model": OLLAMA_MODEL,
        "messages": _build_messages(prompt, history=history, language=language),
        "stream": False,
    }
    r = requests.post(f"{_ollama_base()}/api/chat", json=payload, timeout=(5, 60))
    r.raise_for_status()
    data = r.json()
    return (data.get("message", {}) or {}).get("content", "").strip() or "I couldn’t generate a response."

def generate_response(prompt: str, history=None, language="en"):
    prompt = (prompt or "").strip()
    if not prompt:
        return ""
    if _ollama_ready():
        try:
            return _ask_ollama(prompt, history=history, language=language)
        except Exception:
            logger.exception("Ollama generation failed")
            return "I’m having trouble generating a response right now."
    return "Ollama is not configured or not reachable."

def respond_with_voice(prompt: str, history=None, language="en", voice_on=True):
    reply = generate_response(prompt, history=history, language=language)
    if voice_on and reply:
        try:
            from services.tts_service import speak_text
            speak_text(reply, language=language)
        except Exception:
            logger.exception("Voice output failed")
    return reply