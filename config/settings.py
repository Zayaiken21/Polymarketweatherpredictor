import os
from dotenv import load_dotenv
from config.constants import APP_NAME, DEFAULT_MODEL, DEFAULT_LANGUAGE

load_dotenv(override=True)

class AppSettings:
    def __init__(self):
        self.app_name = os.getenv("APP_NAME", APP_NAME)
        self.ceo_password = os.getenv("CEO_PASSWORD", "ceo1")
        self.ollama_model = os.getenv("OLLAMA_MODEL", DEFAULT_MODEL)
        self.default_language = os.getenv("DEFAULT_LANGUAGE", DEFAULT_LANGUAGE)
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
        self.ollama_api_key = os.getenv("OLLAMA_API_KEY", "")

settings = AppSettings()