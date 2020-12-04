from service3.app import app
from flask_testing import TestCase

from flask import url_for


class TestBase(TestCase):
    def create_app(self):
        return app


class TestService3(TestBase):
    def test_random_gender(self):
        response = self.client.get(url_for('random_gender'))
        self.assert200(response)
        self.assertIn(b'gender', response.data)
        self.assertFalse(True)
