import io
from gtts import gTTS

def speak_text(text: str, language: str = "en"):
    if not text:
        return None

    fp = io.BytesIO()
    tts = gTTS(text=text, lang=language or "en")
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()