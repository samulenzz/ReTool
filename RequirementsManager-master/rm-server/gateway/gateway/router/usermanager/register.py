from flask import request

from gateway.app import app
from gateway.http_client import usermanager_http_client
from gateway.utils.handle_api import handle_request_response


@app.route('/register', methods=['POST'])
@handle_request_response
def register():
    body = request.json
    status_code, resp_body = usermanager_http_client.post(
        endpoint='register', json=body
    )

    return status_code, resp_body
