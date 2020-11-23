from service2.app import app
from flask_testing import TestCase

from flask import url_for,


class TestBase(TestCase):
    def create_app(self):
        return app


class TestService2(TestBase):
    def test_random_country(self):
        response = self.client.get(url_for('random_country'))
        self.assert200(response)
        self.assertIn(b'country_name', response.data)
        self.assertIn(b'country_language', response.data)
