import logging
from functools import lru_cache

import ollama

from config.settings import settings

logger = logging.getLogger("llm_service")
_client = None

def _clean_host(host: str) -> str:
    host = (host or "").strip()
    if not host or host == "http://your-ollama-server:11434":
        return "http://127.0.0.1:11434"
    return host

def get_client():
    global _client
    if _client is None:
        _client = ollama.Client(host=_clean_host(settings.ollama_host))
    return _client

@lru_cache(maxsize=1)
def ollama_available():
    try:
        get_client().list()
        return True
    except Exception:
        logger.exception("Ollama availability check failed")
        return False

def _system_prompt():
    return (
        "You are Poly Market Bot, an AI assistant for the Polymarket weather predictor app. "
        "Your name is Poly Market Bot. "
        "You help the user read market data, explain predictions, summarize signals, and answer clearly. "
        "Be concise, intelligent, and accurate. "
        "If you do not know something, say so plainly."
    )

def _build_messages(prompt: str, history=None, language="en"):
    history = history or []
    messages = [{"role": "system", "content": _system_prompt()}]
    for msg in history[-20:]:
        role = msg.get("role", "user")
        if role not in ("user", "assistant", "system"):
            role = "user"
        content = str(msg.get("content", "")).strip()
        if content:
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": prompt})
    return messages

def generate_response(prompt: str, history=None, language="en") -> str:
    prompt = (prompt or "").strip()
    if not prompt:
        return ""

    if not ollama_available():
        return f"Ollama is not reachable at {_clean_host(settings.ollama_host)}."

    try:
        resp = get_client().chat(
            model=settings.ollama_model,
            messages=_build_messages(prompt, history=history, language=language),
        )
        return resp["message"]["content"]
    except Exception:
        logger.exception("Ollama chat failed")
        return "I’m having trouble generating a response right now."

def respond_with_voice(prompt: str, history=None, language="en", voice_on=True):
    reply = generate_response(prompt, history=history, language=language)
    if voice_on and reply:
        try:
            from services.tts_service import speak_text
            speak_text(reply, language=language)
        except Exception:
            logger.exception("Voice output failed")
    return reply