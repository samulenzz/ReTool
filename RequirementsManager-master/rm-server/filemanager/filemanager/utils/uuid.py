import uuid

def generate_uuid() -> str:
    return uuid.uuid1().hex