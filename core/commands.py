from core.parser import normalize_command

def is_language_command(text: str) -> bool:
    t = normalize_command(text)
    return t.startswith("language ")

def parse_language(text: str) -> str:
    return normalize_command(text).replace("language ", "").strip()