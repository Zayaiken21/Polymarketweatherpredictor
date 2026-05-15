import secrets
import string

ALPHABET = string.ascii_letters + string.digits

def generate_tokens(count=1, length=15):
    return ["".join(secrets.choice(ALPHABET) for _ in range(length)) for _ in range(count)]