import base64
import os


def generate_token() -> str:
    return base64.b64encode(os.urandom(32)).decode()
