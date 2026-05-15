import io
from gtts import gTTS

def speak_text(text: str, language: str = "en"):
    if not text:
        return None

    try:
        mp3_fp = io.BytesIO()
        tts = gTTS(text=text, lang=language or "en")
        tts.write_to_fp(mp3_fp)
        return mp3_fp.getvalue()
    except Exception:
        return None