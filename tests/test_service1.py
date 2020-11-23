from service1.app import app
from flask_testing import TestCase

from unittest.mock import patch

from flask import url_for
import requests_mock

serv2 = "http://localhost:5001"
serv3 = "http://localhost:5002"


class TestBase(TestCase):
    def create_app(self):
        return app


class TestService1(TestBase):
    def test_frontend(self):
        with requests_mock.mock() as g:
            with patch("requests.post") as n:
                g.get(serv2, json={
                    "country_name": "Wales",
                    "country_language": "wel"
                })
                g.get(serv3, json={"gender": "m"})
                n.return_value.json.return_value = {"first_name": "Iwan",
                                                    "last_name": "Moreton"}
                response = self.client.get(url_for('index'))
                print(response.data)
                self.assert200
                self.assertIn(b'Iwan', response.data)
                self.assertIn(b'Moreton', response.data)
                self.assertIn(b'male', response.data)
                self.assertIn(b'Wales', response.data)
