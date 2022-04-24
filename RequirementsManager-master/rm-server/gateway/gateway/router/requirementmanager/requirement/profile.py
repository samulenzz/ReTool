from flask import request

from gateway.app import app
from gateway.http_client import requirementmanager_http_client
from gateway.utils.handle_api import (
    get_client_username, handle_request_response
)


@app.route('/requirement/profile', methods=['GET'])
@handle_request_response
@get_client_username
def requirement_profile(client_username: str):
    args = request.args.to_dict()
    status_code, resp_body = requirementmanager_http_client.get(
        'requirement/profile', client_username, params=args
    )
    return status_code, resp_body
