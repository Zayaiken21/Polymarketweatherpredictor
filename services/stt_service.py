import tempfile
from pathlib import Path

def transcribe_audio(audio_bytes: bytes, language: str = "en") -> str:
    try:
        import speech_recognition as sr
    except Exception:
        return ""

    recognizer = sr.Recognizer()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        with sr.AudioFile(tmp_path) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio, language=language)
    except Exception:
        return ""
    finally:
        try:
            Path(tmp_path).unlink(missing_ok=True)
        except Exception:
            pass