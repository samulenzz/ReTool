from hashlib import sha256


def encrypt_password(raw_password: str) -> str:
    return sha256(raw_password.encode('utf-8')).hexdigest()


def verify_password(raw_password: str, encrypted_password: str) -> bool:
    return encrypt_password(raw_password) == encrypted_password
