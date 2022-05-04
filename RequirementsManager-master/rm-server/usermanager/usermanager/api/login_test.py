import json
import unittest
import requests

from usermanager.api.login import META_SUCCESS, META_ERROR

url = "http://39.101.187.244:8080/login"


class TestLogin(unittest.TestCase):

    def test_username_not_exist(self):
        payload = {"username": "liuzh", "password": "123456"}
        r = requests.post(url, json=payload)
        self.assertEqual(r.status_code, 200)
        results = json.loads(r.content)
        self.assertEqual(results['meta'], META_ERROR)

    def test_password_wrong(self):
        payload = {"username": "admin", "password": "1234567"}
        r = requests.post(url, json=payload)
        self.assertEqual(r.status_code, 200)
        results = json.loads(r.content)
        self.assertEqual(results['meta'], META_ERROR)

    def test_login_successful(self):
        payload = {"username": "admin", "password": "123456"}
        r = requests.post(url, json=payload)
        self.assertEqual(r.status_code, 200)
        results = json.loads(r.content)
        self.assertEqual(results['meta'], META_SUCCESS)


if __name__ == '__main__':
    unittest.main()
