import io
from gtts import gTTS

def speak_text(text: str, language: str = "en"):
    if not text:
        return None

    try:
        fp = io.BytesIO()
        tts = gTTS(text=text, lang=language or "en")
        tts.write_to_fp(fp)
        return fp.getvalue()
    except Exception:
        return None