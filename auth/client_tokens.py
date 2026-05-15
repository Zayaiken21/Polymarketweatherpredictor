import secrets
import string

def generate_tokens(count=1, length=15):
    alphabet = string.ascii_uppercase + string.digits
    return [
        "".join(secrets.choice(alphabet) for _ in range(length))
        for _ in range(count)
    ]