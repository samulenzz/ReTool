import time
from dataclasses import dataclass


@dataclass
class Token:
    username: str
    token_value: str
    retire_timestamp: int = None

    def __post_init__(self):
        if not self.retire_timestamp:
            self.retire_timestamp = int(time.time()) + 10800


class TokenStorage:
    def __init__(self):
        self.tokens = {}
    
    def add_token(self, token: Token):
        self.tokens[token.token_value] = token
    
    def delete_token(self, token: Token):
        self.tokens.pop(token.token_value)

    def get_username(self, token_value) -> str:
        token = self.tokens.get(token_value, None)
        # Token不存在，直接返回
        if not token:
            return None
        # 如果Token过期，删除并返回
        if token.retire_timestamp < int(time.time()):
            self.delete_token(token)
            return None
        return token.username


token_storage = TokenStorage()
