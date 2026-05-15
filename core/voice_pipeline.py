from services.stt_service import transcribe_audio
from services.llm_service import respond_with_voice
from services.tts_service import speak_text

def process_voice_bytes(audio_bytes, history=None, language="en", voice_on=True):
    transcript = transcribe_audio(audio_bytes, language=language) or ""
    reply = respond_with_voice(
        transcript,
        history=history or [],
        language=language,
        voice_on=voice_on,
    )
    spoken = speak_text(reply, language=language) if voice_on and reply else None
    return transcript, reply, spoken