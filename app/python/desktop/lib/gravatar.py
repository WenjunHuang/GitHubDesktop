import hashlib


def generate_gravatar_url(email: str, size: int = 60) -> str:
    input = email.strip().lower()
    hash = hashlib.md5()
    hash.update(email.encode('utf-8'))
    hash = hash.hexdigest()


    return f"https://www.gravatar.com/avatar/{hash}?s={size}"
