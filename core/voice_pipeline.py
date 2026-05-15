from services.stt_service import transcribe_audio
from services.llm_service import generate_response
from services.tts_service import speak_text

def process_voice_bytes(audio_bytes, history=None, language="en", voice_on=True):
    transcript = transcribe_audio(audio_bytes, language=language) or ""
    reply = generate_response(transcript, history=history or [], language=language)
    spoken = {"text": reply, "played": False}

    if voice_on and reply:
        try:
            speak_text(reply, language=language)
            spoken["played"] = True
        except Exception:
            spoken["played"] = False

    return transcript, reply, spoken