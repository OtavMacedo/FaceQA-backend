import hashlib
import secrets


def generate_api_key():
    return secrets.token_hex(16)


def get_api_key_hash(api_key: str):
    return hashlib.sha256(api_key.encode()).hexdigest()
