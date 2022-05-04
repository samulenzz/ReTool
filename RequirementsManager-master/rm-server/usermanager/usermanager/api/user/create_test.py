import json
import unittest

import requests

from projectmanager.api.project.create import META_SUCCESS
from usermanager.api.user.create import META_ERROR
from usermanager.utils.handle_api import META_NO_ACCESS

url = "http://39.101.187.244:8080/user/create"


class TestCreate(unittest.TestCase):

    def test_create_successful(self):
        headers = {"Client-Username": "admin"}
        payload = {"username": "liuzehua", "password": "123456"}
        r = requests.post(url, headers=headers, json=payload)
        self.assertEqual(r.status_code, 200)
        results = json.loads(r.content)
        self.assertEqual(results['meta'], META_SUCCESS)

    def test_system_role(self):
        headers = {"Client-Username": "liuzehua"}
        payload = {"username": "liuzehua", "password": "123456"}
        r = requests.post(url, headers=headers, json=payload)
        self.assertEqual(r.status_code, 200)
        results = json.loads(r.content)
        self.assertEqual(results['meta'], META_NO_ACCESS)

    def test_username_exist(self):
        headers = {"Client-Username": "admin"}
        payload = {"username": "admin", "password": "123456"}
        r = requests.post(url, headers=headers, json=payload)
        self.assertEqual(r.status_code, 200)
        results = json.loads(r.content)
        self.assertEqual(results['meta'], META_ERROR)


if __name__ == '__main__':
    unittest.main()
