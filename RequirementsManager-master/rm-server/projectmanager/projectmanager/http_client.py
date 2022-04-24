from urllib.parse import urljoin, quote

import requests

from projectmanager.config import REQUIREMENT_MANAGER_URL


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


class RequirementManagerHttpClient(HttpClient):
    def requirement_archive_create(self, project_id: str, version: str):
        body = {
            'project_id': project_id,
            'version': version,
        }

        status_code, resp_body = self.post(
            'requirement/archive/create', 'PROJECT_MANAGER', json=body
        )
        if status_code != 200:
            raise RuntimeError('Create Archive Requirement Failed!')


requirementmanager_http_client = RequirementManagerHttpClient(REQUIREMENT_MANAGER_URL)
