from flask import request

from gateway.app import app
from gateway.utils.handle_api import (
    get_client_username, handle_request_response
)
from gateway.http_client import templatemanager_http_client


@app.route('/document/comments/wordcloud', methods=['GET'])
@handle_request_response
@get_client_username
def comments_wordcloud(client_username: str):
    args = request.args.to_dict()
    status_code, resp_body = templatemanager_http_client.get(
        'document/comments/wordcloud', client_username, params=args
    )
    return status_code, resp_body
