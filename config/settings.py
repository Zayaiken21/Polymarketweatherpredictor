import os
from dotenv import load_dotenv
from config.constants import APP_NAME, DEFAULT_MODEL, DEFAULT_LANGUAGE

load_dotenv()

class AppSettings:
    app_name = os.getenv("APP_NAME", APP_NAME)
    ceo_password = os.getenv("CEO_PASSWORD", "ceo1")
    ollama_model = os.getenv("OLLAMA_MODEL", DEFAULT_MODEL)
    default_language = os.getenv("DEFAULT_LANGUAGE", DEFAULT_LANGUAGE)

settings = AppSettings()