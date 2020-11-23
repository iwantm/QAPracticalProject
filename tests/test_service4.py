from service4.app import app
from flask_testing import TestCase
from unittest.mock import patch
import json
from flask import url_for


class TestBase(TestCase):
    def create_app(self):
        return app


class TestService4(TestBase):
    def test_output(self):
        with patch('requests.get') as g:
            g.return_value.json.return_value = {
                "names": ["Federica", "Desideria"]}
            response = self.client.post(url_for('random_name'), data=json.dumps({
                                        "country_language": "ita", "gender": "f"}), content_type='application/json')
            self.assertIn(b'first_name', response.data)
            self.assertIn(b'last_name', response.data)
            self.assertIn(b'Federica', response.data)
            self.assertIn(b'Desideria', response.data)
            self.assert200
