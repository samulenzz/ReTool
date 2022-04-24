from typing import Dict
from urllib.parse import urljoin, quote

import requests

from gateway.config import (
    USER_MANAGER_URL, PROJECT_MANAGER_URL, REQUIREMENT_MANAGER_URL,FILE_MANAGER_URL,TEMPLATE_MANAGET_URL
)

DEFAULT_TIMEOUT = 60


class HttpClient:
    def __init__(self, url: str):
        if not url.endswith('/'):
            url = url + '/'
        self.url = url

    def _request(self, endpoint: str, method: str, client_username: str, **kwargs):
        headers = {}
        if client_username:
            # 对中文用户名进行编码
            headers = {'Client-Username': quote(client_username)}

        resp = requests.request(
            method=method,
            url=urljoin(self.url, endpoint),
            headers=headers,
            timeout=DEFAULT_TIMEOUT,
            **kwargs
        )
        return resp.status_code, resp.json()

    def post(self, endpoint: str, client_username: str = None, **kwargs):
        return self._request(endpoint, 'POST', client_username, **kwargs)
    
    def get(self, endpoint: str, client_username: str = None, **kwargs):
        return self._request(endpoint, 'GET', client_username, **kwargs)

    def put(self, endpoint: str, client_username: str = None, **kwargs):
        return self._request(endpoint, 'PUT', client_username, **kwargs)

    def delete(self, endpoint: str, client_username: str = None, **kwargs):
        return self._request(endpoint, 'DELETE', client_username, **kwargs)




usermanager_http_client = HttpClient(USER_MANAGER_URL)
projectmanager_http_client = HttpClient(PROJECT_MANAGER_URL)
requirementmanager_http_client = HttpClient(REQUIREMENT_MANAGER_URL)
filemanager_http_client = HttpClient(FILE_MANAGER_URL)
templatemanager_http_client = HttpClient(TEMPLATE_MANAGET_URL)