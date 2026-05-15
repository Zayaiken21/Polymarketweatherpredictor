import logging

logger = logging.getLogger("tts_service")

def speak_text(text, language="en"):
    text = (text or "").strip()
    if not text:
        return False
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return True
    except Exception:
        logger.exception("TTS failed")
        return False