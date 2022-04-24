from urllib.parse import unquote

from flask import request


def get_client_username():
    raw_client_username = request.headers.get('Client-Username')
    return unquote(raw_client_username)
