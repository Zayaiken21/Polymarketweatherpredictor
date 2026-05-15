import secrets
import string
from config.constants import TOKEN_LENGTH

_ALLOWED = string.ascii_letters + string.digits

def generate_token(length=TOKEN_LENGTH):
    return "".join(secrets.choice(_ALLOWED) for _ in range(length))

def generate_tokens(count=1):
    count = max(1, int(count))
    return [generate_token() for _ in range(count)]